import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Dropout
from spektral.layers import GCNConv, GlobalSumPool
from spektral.data import Graph, Dataset
from spektral.data.loaders import DisjointLoader
import networkx as nx
import numpy as np
from scipy.sparse import coo_matrix


# 📌 Configuración de la GNN
N_HIDDEN = 32
N_LABELS = 1
LEARNING_RATE = 0.01
BATCH_SIZE = 1
EPOCHS = 50


class CustomGCNConv(GCNConv):
    """
    📌 Subclase de GCNConv para forzar la inferencia de salida.
    """
    def compute_output_shape(self, input_shape):
        """
        📌 Calcula la forma de salida correctamente antes de `call()`.
        """
        feature_shape, adj_shape = input_shape
        return feature_shape  # 🔥 La salida tiene la misma forma que la entrada


def construir_modelo(input_dim):
    """
    📌 Construye y devuelve una instancia del modelo GNN.
    """
    inputs_x = tf.keras.Input(shape=(input_dim,))
    inputs_a = tf.keras.Input(shape=(None, None), sparse=True)
    inputs_i = tf.keras.Input(shape=(None,), dtype=tf.int64)

    x = CustomGCNConv(N_HIDDEN, activation="relu")([inputs_x, inputs_a])
    x = CustomGCNConv(N_HIDDEN, activation="relu")([x, inputs_a])
    x = GlobalSumPool()([x, inputs_i])
    x = Dropout(0.5)(x)
    outputs = Dense(N_LABELS, activation="sigmoid")(x)

    model = Model(inputs=[inputs_x, inputs_a, inputs_i], outputs=outputs)
    model.compile(optimizer=tf.keras.optimizers.Adam(LEARNING_RATE),
                  loss="binary_crossentropy", metrics=["accuracy"])
    return model


class CEREBRODataset(Dataset):
    """
    📌 Dataset personalizado para Spektral.
    Convierte el grafo de CEREBRO en un formato compatible con Spektral.
    """
    def __init__(self, memory_manager, get_embedding, **kwargs):
        self.memory_manager = memory_manager  # ✅ Ahora es un `MemoryManager`
        self.get_embedding = get_embedding
        super().__init__(**kwargs)

    def read(self):
        """📌 Convierte el grafo de memoria en una estructura compatible con Spektral."""
        grafo = self.memory_manager.get_graph()  # ✅ Ahora sí es un `MemoryManager`
        return [self.convertir_grafo_para_gnn(grafo)]  

    def convertir_grafo_para_gnn(self, grafo):
        """
        📌 Convierte un grafo de NetworkX a un formato compatible con Spektral.
        """
        nodos = list(grafo.nodes)
        if not nodos:
            raise ValueError("❌ Error: El grafo está vacío, no se puede convertir.")

        nodo_a_idx = {nodo: idx for idx, nodo in enumerate(nodos)}
        X = np.array([self.get_embedding(nodo) for nodo in nodos])

        # 🔥 Convertimos a matriz dispersa en formato COO
        A = nx.to_numpy_array(grafo, nodelist=nodos, dtype=np.float32)
        A_sparse = coo_matrix(A)

        return Graph(x=X, a=A_sparse)




def entrenar_gnn(memory_manager, get_embedding):
    """
    📌 Entrena la GNN asegurando la conversión correcta de los grafos.
    """
    dataset = CEREBRODataset(memory_manager, get_embedding)  # ✅ Pasamos `MemoryManager`
    
    sample_graph = dataset.read()[0]  # ✅ Tomamos un grafo convertido
    model = construir_modelo(sample_graph.x.shape[1])  # 📌 Usa la dimensión correcta

    loader = DisjointLoader(dataset, batch_size=BATCH_SIZE, shuffle=True)
    
    print(f"🏋️ Iniciando entrenamiento...")

    for batch in loader:
        if not isinstance(batch, (tuple, list)) or len(batch) != 3:
            raise ValueError(f"❌ Error: Formato de batch inesperado, recibió {type(batch)}")
        
        X, A, I = batch

        # 🔥 🔥 **Aquí convertimos `A` a `SparseTensor` correctamente**
        if isinstance(A, np.ndarray):
            A = coo_matrix(A)  # Convertir `A` en matriz dispersa

        if not isinstance(A, tf.SparseTensor):
            A = tf.sparse.SparseTensor(
                indices=np.array([A.row, A.col]).T,
                values=A.data.astype(np.float32),
                dense_shape=A.shape
            )

        A = tf.sparse.reorder(A)  # 🔥 IMPORTANTE: Reordenar `SparseTensor`

        # 🔥 Debug antes de entrenar
        print(f"📌 Debug - Batch: X.shape={X.shape}, A.shape={A.dense_shape}, I.shape={I.shape}")

        model.fit([X, A, I], epochs=EPOCHS, steps_per_epoch=loader.steps_per_epoch)

    print("✅ GNN entrenada con éxito")
    return model
