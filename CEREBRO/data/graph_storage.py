import networkx as nx
import json
import os

class GraphStorage:
    """
    📌 Módulo de almacenamiento de grafos en CEREBRO.
    - Guarda y carga grafos en formato JSON.
    - Soporta múltiples grafos (conceptos, conciencia).
    """

    def __init__(self, storage_path="data/graph_data.json"):
        self.storage_path = storage_path
        self.graph = nx.Graph()
        self.load_graph()

    def load_graph(self):
        """📂 Carga el grafo desde un archivo JSON."""
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, "r", encoding="utf-8") as file:
                    data = json.load(file)
                    self.graph = nx.node_link_graph(data)
                print("✅ Grafo cargado con éxito.")
            except Exception as e:
                print(f"⚠️ Error al cargar el grafo: {e}")
        else:
            print("⚠️ No se encontró un archivo de grafo. Se inicia uno nuevo.")

    def save_graph(self):
        """💾 Guarda el estado actual del grafo en un archivo JSON."""
        try:
            with open(self.storage_path, "w", encoding="utf-8") as file:
                json.dump(nx.node_link_data(self.graph), file, indent=4)
            print("✅ Grafo guardado correctamente.")
        except Exception as e:
            print(f"⚠️ Error al guardar el grafo: {e}")

    def add_connection(self, nodo1, nodo2, peso=1.0):
        """📌 Agrega o refuerza una conexión entre dos nodos."""
        if not self.graph.has_node(nodo1):
            self.graph.add_node(nodo1, tipo="concepto")
        if not self.graph.has_node(nodo2):
            self.graph.add_node(nodo2, tipo="concepto")

        if self.graph.has_edge(nodo1, nodo2):
            self.graph[nodo1][nodo2]["peso"] += peso
        else:
            self.graph.add_edge(nodo1, nodo2, peso=peso)

        print(f"🔗 Conexión añadida: {nodo1} ↔ {nodo2} (Peso: {peso})")
        self.save_graph()

    def get_connections(self, nodo):
        """📌 Devuelve todas las conexiones de un nodo."""
        if nodo in self.graph:
            return [(n, self.graph[nodo][n]["peso"]) for n in self.graph[nodo]]
        return []

