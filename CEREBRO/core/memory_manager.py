import networkx as nx
import json
import os


class MemoryManager:
    """
    📌 Gestión del acceso y almacenamiento en memoria de CEREBRO.
    - Administra el grafo de conceptos.
    - Mantiene su propia estructura separada de `MemoryStorage`.
    """

    def __init__(self, memory_file="data/memory_graph.json"):
        self.memory_file = memory_file
        self.graph = nx.Graph()
        self.load_memory()
        

    def load_memory(self):
        """📂 Carga el grafo de memoria desde un archivo JSON."""
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, "r", encoding="utf-8") as file:
                    data = json.load(file)
                    self.graph = nx.node_link_graph(data)
                print("✅ Grafo de memoria cargado con éxito.")
            except Exception as e:
                print(f"⚠️ Error al cargar el grafo de memoria: {e}")
        else:
            print("⚠️ No se encontró un archivo de memoria. Se inicia un grafo nuevo.")

    def save_memory(self):
        """💾 Guarda el estado actual del grafo de memoria en un archivo JSON."""
        try:
            with open(self.memory_file, "w", encoding="utf-8") as file:
                json.dump(nx.node_link_data(self.graph), file, indent=4)
            print("✅ Grafo de memoria guardado correctamente.")
        except Exception as e:
            print(f"⚠️ Error al guardar el grafo de memoria: {e}")

    def add_memory(self, concepto1, concepto2, peso=1.0):
        """📌 Agrega una nueva conexión entre dos conceptos en el grafo."""
        if not self.graph.has_node(concepto1):
            self.graph.add_node(concepto1, tipo="concepto")
        if not self.graph.has_node(concepto2):
            self.graph.add_node(concepto2, tipo="concepto")

        if self.graph.has_edge(concepto1, concepto2):
            self.graph[concepto1][concepto2]["peso"] += peso
        else:
            self.graph.add_edge(concepto1, concepto2, peso=peso)

        print(f"✅ Memoria actualizada: {concepto1} ↔ {concepto2} (Peso: {peso})")
        self.save_memory()

    def get_related_concepts(self, concepto, threshold=0.5):
        """📌 Devuelve los conceptos más relacionados a un nodo dado según el peso."""
        if concepto not in self.graph:
            return []
        relaciones = [(n, d["peso"]) for n, d in self.graph[concepto].items() if d["peso"] >= threshold]
        return sorted(relaciones, key=lambda x: x[1], reverse=True)

    def reinforce_memory(self, concepto1, concepto2, incremento=0.2):
        """📌 Aumenta el peso de una relación en el grafo."""
        if self.graph.has_edge(concepto1, concepto2):
            self.graph[concepto1][concepto2]["peso"] += incremento
            print(f"🔄 Refuerzo de conexión: {concepto1} ↔ {concepto2} (+{incremento})")
        else:
            print(f"⚠️ No existe una relación previa entre {concepto1} y {concepto2}.")
        self.save_memory()

    def get_graph(self):
        """📌 Devuelve el grafo de memoria como un objeto NetworkX."""
        if not self.graph.nodes:
            print("⚠️ El grafo está vacío.")
        return self.graph  # ✅ Devolvemos el grafo directamente


