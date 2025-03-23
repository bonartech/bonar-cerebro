import tensorflow as tf
from keras import Model
from keras import layers

from spektral.layers import GCNConv
import networkx as nx
import numpy as np

class GrafoNeuronal(Model):
    def __init__(self, input_dim, hidden_dim=32):
        super(GrafoNeuronal, self).__init__()
        self.conv1 = GCNConv(hidden_dim, activation="relu")
        self.conv2 = GCNConv(hidden_dim, activation="relu")
        self.fc = layers.Dense(1, activation="sigmoid")

    def call(self, inputs, training=False):
        X, A = inputs

        # 🚨 Validación antes de procesar
        if tf.reduce_any(tf.math.is_nan(X)):
            raise ValueError("❌ Error: `X` contiene valores NaN.")
        if tf.reduce_any(tf.math.is_nan(A)):
            raise ValueError("❌ Error: `A` contiene valores NaN.")

        X = self.conv1([X, A])
        X = self.conv2([X, A])
        return self.fc(X)

def convertir_grafo_para_gnn(grafo, nlp):
    """Convierte el grafo de NetworkX a un formato compatible con Spektral (TensorFlow)."""

    nodos = list(grafo.nodes)
    nodo_a_idx = {nodo: idx for idx, nodo in enumerate(nodos)}

    if not nodos:
        raise ValueError("❌ Error: El grafo está vacío, no se puede convertir para la GNN.")

    # ✅ Generar embeddings iniciales con spaCy
    X = np.array([
        nlp(nodo).vector if nlp(nodo).vector_norm > 0 else np.zeros((300,))
        for nodo in nodos
    ])

    # 🚨 Verificación: ¿X está vacío o tiene valores NaN?
    if X.size == 0 or np.isnan(X).any():
        raise ValueError("❌ Error: `X` contiene valores NaN o está vacío.")

    # ✅ Convertir la matriz de adyacencia correctamente
    A = nx.to_numpy_array(grafo, nodelist=nodos, dtype=np.float32)

    # 🚨 Verificación: ¿A está vacío o tiene valores NaN?
    if A.size == 0 or np.isnan(A).any():
        raise ValueError("❌ Error: `A` contiene valores NaN o está vacío.")

    # ✅ Convertir a Tensores de TensorFlow
    A = tf.convert_to_tensor(A, dtype=tf.float32)
    X = tf.convert_to_tensor(X, dtype=tf.float32)

    print("✅ Grafo convertido para TensorFlow y Spektral")
    print(f"📊 X shape: {X.shape}, A shape: {A.shape}")
    print(f"📊 X sample: {X.numpy()[:3]}")  # Imprimir las primeras 3 filas para verificar
    print(f"📊 A sample: {A.numpy()[:3]}")  # Imprimir las primeras 3 filas para verificar
    return A, X, nodo_a_idx


def entrenar_gnn(A, X, epochs=50, lr=0.01):
    """Entrena la GNN usando Spektral."""
    modelo = GrafoNeuronal(input_dim=X.shape[1], hidden_dim=32)
    modelo.compile(optimizer=tf.keras.optimizers.Adam(lr), loss="mse")

    for epoch in range(epochs):
        with tf.GradientTape() as tape:
            salida = modelo([X, A], training=True)
            loss = tf.reduce_mean(tf.square(salida - A))  # Función de pérdida MSE

        gradientes = tape.gradient(loss, modelo.trainable_variables)
        modelo.optimizer.apply_gradients(zip(gradientes, modelo.trainable_variables))

        if epoch % 10 == 0:
            print(f"🔄 Epoch {epoch}/{epochs} - Pérdida: {loss.numpy():.4f}")

    print("✅ GNN entrenada con éxito")
    return modelo

def predecir_nueva_conexion(modelo, nodo1, nodo2, A, X, nodo_a_idx):
    """Usa la GNN para predecir la fuerza de conexión entre dos nodos."""
    if nodo1 not in nodo_a_idx or nodo2 not in nodo_a_idx:
        return f"⚠️ '{nodo1}' o '{nodo2}' no existen en el grafo."

    idx1, idx2 = nodo_a_idx[nodo1], nodo_a_idx[nodo2]

    # ✅ Asegurar que el modelo está en modo evaluación
    modelo.trainable = False
    salida = modelo([X, A])

    emb1, emb2 = salida[idx1], salida[idx2]
    distancia = np.linalg.norm(emb1.numpy() - emb2.numpy())

    return f"🔮 Predicción de relación '{nodo1}' ↔ '{nodo2}': {1 / (1 + distancia):.4f}"
