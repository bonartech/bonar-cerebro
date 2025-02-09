import numpy as np

def predecir_nueva_conexion(modelo, nodo1, nodo2, A, X, nodo_a_idx):
    """Usa la GNN para predecir la fuerza de conexión entre dos nodos."""
    if nodo1 not in nodo_a_idx or nodo2 not in nodo_a_idx:
        return f"⚠️ '{nodo1}' o '{nodo2}' no existen en el grafo."

    idx1, idx2 = nodo_a_idx[nodo1], nodo_a_idx[nodo2]
    emb1, emb2 = modelo([X, A])[idx1], modelo([X, A])[idx2]
    distancia = np.linalg.norm(emb1.numpy() - emb2.numpy())

    return f"🔮 Predicción de relación '{nodo1}' ↔ '{nodo2}': {1 / (1 + distancia):.4f}"
