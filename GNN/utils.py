import numpy as np
import tensorflow as tf
import networkx as nx
from CEREBRO.text_processor import  nlp

def convertir_grafo_para_gnn(grafo):
    """Convierte el grafo de NetworkX a un formato compatible con TensorFlow/Spektral"""
    nodos = list(grafo.nodes)
    nodo_a_idx = {nodo: idx for idx, nodo in enumerate(nodos)}

    # Matriz de adyacencia y embeddings de nodos
    A = nx.to_numpy_array(grafo, nodelist=nodos)
    X = np.array([nlp(nodo).vector for nodo in nodos])

    # Convertir a tensores
    A = tf.convert_to_tensor(A, dtype=tf.float32)
    X = tf.convert_to_tensor(X, dtype=tf.float32)

    return A, X, nodo_a_idx
