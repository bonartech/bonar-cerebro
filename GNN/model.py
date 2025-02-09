import tensorflow as tf
from tensorflow.keras import Model
from tensorflow.keras.layers import Dense
import spektral
from spektral.layers import GCNConv

class GrafoNeuronal(Model):
    def __init__(self, input_dim, hidden_dim=32):
        super(GrafoNeuronal, self).__init__()
        self.conv1 = GCNConv(hidden_dim, activation="relu")
        self.conv2 = GCNConv(hidden_dim, activation="relu")
        self.fc = Dense(1, activation="sigmoid")  # Para predecir conexiones

    def call(self, inputs):
        X, A = inputs  # Nodos y matriz de adyacencia
        X = self.conv1([X, A])
        X = self.conv2([X, A])
        return X  # Retorna embeddings de los nodos

def convertir_grafo_para_gnn(grafo, nlp):
    """Convierte el grafo de NetworkX a un formato compatible con Spektral (TensorFlow)."""
    nodos = list(grafo.nodes)
    nodo_a_idx = {nodo: idx for idx, nodo in enumerate(nodos)}

    # Crear matriz de adyacencia y atributos de nodos
    A = nx.to_numpy_array(grafo, nodelist=nodos)
    X = np.array([nlp(nodo).vector for nodo in nodos])  # Embeddings con spaCy

    # Convertir a tensores de TensorFlow
    A = tf.convert_to_tensor(A, dtype=tf.float32)
    X = tf.convert_to_tensor(X, dtype=tf.float32)

    print("✅ Grafo convertido para TensorFlow y Spektral")
    return A, X, nodo_a_idx

def entrenar_gnn(A, X, epochs=50, lr=0.01):
    """Entrena la GNN usando la matriz de adyacencia y los embeddings."""
    modelo = GrafoNeuronal(input_dim=X.shape[1])
    modelo.compile(optimizer=tf.keras.optimizers.Adam(lr), loss="mse")

    for epoch in range(epochs):
        loss = modelo.train_on_batch([X, A], A)  # Aprender conexiones
        if epoch % 10 == 0:
            print(f"🔄 Epoch {epoch}/{epochs} - Pérdida: {loss:.4f}")

    print("✅ GNN entrenada con éxito")
    return modelo

def predecir_nueva_conexion(modelo, nodo1, nodo2, A, X, nodo_a_idx):
    """Usa la GNN para predecir la fuerza de conexión entre dos nodos."""
    if nodo1 not in nodo_a_idx or nodo2 not in nodo_a_idx:
        return f"⚠️ '{nodo1}' o '{nodo2}' no existen en el grafo."

    idx1, idx2 = nodo_a_idx[nodo1], nodo_a_idx[nodo2]

    emb1, emb2 = modelo([X, A])[idx1], modelo([X, A])[idx2]
    distancia = np.linalg.norm(emb1.numpy() - emb2.numpy())

    return f"🔮 Predicción de relación '{nodo1}' ↔ '{nodo2}': {1 / (1 + distancia):.4f}"
