import networkx as nx
import json
import spacy
import unicodedata

class MemoryManager:
    """
    📌 Gestión del acceso y almacenamiento en memoria de CEREBRO.
    Administra el grafo de conceptos y memoria, permitiendo la evolución dinámica del conocimiento.
    """
    
    def __init__(self, memory_file="data/memory_graph.json"):
        self.memory_file = memory_file
        self.graph = nx.Graph()
        self.nlp = spacy.load("es_core_news_md")
        self.load_memory()
    
    def load_memory(self):
        """Carga el grafo de memoria desde un archivo JSON."""
        try:
            with open(self.memory_file, "r", encoding="utf-8") as file:
                data = json.load(file)
                self.graph = nx.node_link_graph(data)
            print("📂 Memoria cargada con éxito.")
        except FileNotFoundError:
            print("⚠️ No se encontró un archivo de memoria. Se inicia uno nuevo.")
    
    def save_memory(self):
        """Guarda el estado actual del grafo de memoria en un archivo JSON."""
        with open(self.memory_file, "w", encoding="utf-8") as file:
            json.dump(nx.node_link_data(self.graph), file, indent=4)
        print("💾 Memoria guardada correctamente.")
    
    def normalize_text(self, text):
        """Convierte el texto a minúsculas y elimina tildes."""
        text = text.lower().strip()
        return ''.join(c for c in unicodedata.normalize('NFKD', text) if not unicodedata.combining(c))
    
    def calculate_dynamic_weight(self, concept1, concept2):
        """Calcula el peso de una relación basado en embeddings y conexiones previas."""
        if concept1 not in self.graph or concept2 not in self.graph:
            return 1.0  # Peso base si no existen en el grafo

        common_neighbors = set(self.graph.neighbors(concept1)).intersection(set(self.graph.neighbors(concept2)))
        reinforcement_factor = len(common_neighbors) * 0.1

        doc1, doc2 = self.nlp(concept1), self.nlp(concept2)
        embedding_similarity = doc1.similarity(doc2) if doc1.vector_norm > 0 and doc2.vector_norm > 0 else 0

        return 1.0 + reinforcement_factor + (embedding_similarity if embedding_similarity > 0.7 else 0)
    
    def add_memory(self, concept1, concept2, weight=1.0):
        """Agrega una nueva conexión de memoria entre dos conceptos con peso dinámico."""
        concept1, concept2 = self.normalize_text(concept1), self.normalize_text(concept2)
        
        if not self.graph.has_node(concept1):
            self.graph.add_node(concept1, tipo="concepto")
        if not self.graph.has_node(concept2):
            self.graph.add_node(concept2, tipo="concepto")
        
        weight = self.calculate_dynamic_weight(concept1, concept2)
        if self.graph.has_edge(concept1, concept2):
            self.graph[concept1][concept2]["peso"] += weight
        else:
            self.graph.add_edge(concept1, concept2, peso=weight)
        
        print(f"✅ Memoria actualizada: {concept1} ↔ {concept2} (Peso: {weight})")
        self.save_memory()
    
    def get_related_concepts(self, concept, threshold=0.5):
        """Devuelve los conceptos más relacionados a un nodo dado según el peso."""
        concept = self.normalize_text(concept)
        if concept not in self.graph:
            return []
        relations = [(n, d["peso"]) for n, d in self.graph[concept].items() if d["peso"] >= threshold]
        return sorted(relations, key=lambda x: x[1], reverse=True)
    
    def reinforce_memory(self, concept1, concept2, increment=0.2):
        """Aumenta el peso de una relación cuando la conexión es relevante."""
        concept1, concept2 = self.normalize_text(concept1), self.normalize_text(concept2)
        
        if self.graph.has_edge(concept1, concept2):
            self.graph[concept1][concept2]["peso"] += increment
            print(f"🔄 Refuerzo de conexión: {concept1} ↔ {concept2} (+{increment})")
        else:
            print(f"⚠️ No existe una relación previa entre {concept1} y {concept2}.")
        self.save_memory()