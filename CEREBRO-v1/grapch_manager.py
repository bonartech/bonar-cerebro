import networkx as nx
import os
import pickle

GRAFO_FILENAME = "data/grafo_cerebro.pkl"

def cargar_grafo():
    """Carga el grafo desde un archivo si existe y lo devuelve."""
    global grafo
    if os.path.exists(GRAFO_FILENAME):
        try:
            with open(GRAFO_FILENAME, "rb") as f:
                grafo = pickle.load(f)
            print("📂 Grafo cargado con éxito.")
        except (EOFError, pickle.UnpicklingError):
            print("⚠️ Archivo del grafo vacío o corrupto. Creando un nuevo grafo.")
            grafo = nx.Graph()
    else:
        print("⚠️ No se encontró un grafo previo. Creando uno nuevo.")
        grafo = nx.Graph()
    
    return grafo  # ✅ Ahora `cargar_grafo()` devuelve el grafo


def guardar_grafo(grafo):
    """Guarda el grafo en un archivo para persistencia."""
    with open(GRAFO_FILENAME, "wb") as f:
        pickle.dump(grafo, f)


def mostrar_grafo(grafo):
    """Muestra los nodos y conexiones del grafo generado."""
    print("\n🔍 **Nodos en el Grafo:**")
    for nodo in grafo.nodes:
        print(f"- {nodo} (Tipo: {grafo.nodes[nodo]['tipo']})")

    print("\n🔗 **Conexiones:**")
    for nodo1, nodo2, data in grafo.edges(data=True):
        print(f"- {nodo1} ↔ {nodo2} (Peso: {data['peso']:.2f})")