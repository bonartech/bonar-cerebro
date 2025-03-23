import numpy as np
from learning.gnn_model import entrenar_gnn
import tensorflow as tf

from core.memory_manager import MemoryManager
from core.consciousness_engine import ConsciousnessEngine

MODEL_PATH = "models/gnn_model.h5"

class Predictor:
    """
    📌 Predictor de nuevas relaciones en los grafos de CEREBRO.
    Usa Graph Neural Networks (GNNs) para inferir conexiones no existentes.
    """

    def __init__(self, memory_manager: MemoryManager, consciousness_engine: ConsciousnessEngine):
        self.memory_manager = memory_manager
        self.consciousness_engine = consciousness_engine
        self.model = self.load_model()  # 🔥 Cargar modelo al inicializar

    def load_model(self):
        """
        📌 Carga el modelo GNN entrenado desde el servicio.
        """
        model = entrenar_gnn(load_only=True)  # 🔥 Cargar sin reentrenar
        model.load_weights(MODEL_PATH)
        return model

    def predict_relationship(self, nodo1, nodo2):
        """
        📌 Predice la probabilidad de que exista una relación entre dos nodos.
        """
        if nodo1 not in self.memory_manager.graph or nodo2 not in self.memory_manager.graph:
            return 0.0  # No hay datos para hacer la predicción

        emb1 = self.get_embedding(nodo1)
        emb2 = self.get_embedding(nodo2)

        distancia = np.linalg.norm(emb1 - emb2)
        probabilidad = 1 / (1 + distancia)  # Inversa de la distancia como probabilidad

        return round(probabilidad, 4)

    def get_embedding(self, nodo):
        """
        📌 Obtiene el embedding de un nodo en la GNN.
        """
        features = np.array([self.memory_manager.get_node_features(nodo)])
        emb = self.model.predict(features)[0]
        return emb

    def suggest_new_connections(self, threshold=0.75):
        """
        📌 Busca pares de nodos con alta probabilidad de conexión y los sugiere.
        """
        nodos = list(self.memory_manager.graph.nodes)
        nuevas_conexiones = []

        for i, nodo1 in enumerate(nodos):
            for nodo2 in nodos[i+1:]:
                prob = self.predict_relationship(nodo1, nodo2)
                if prob >= threshold:
                    nuevas_conexiones.append((nodo1, nodo2, prob))

        return sorted(nuevas_conexiones, key=lambda x: x[2], reverse=True)

    def reinforce_prediction(self, nodo1, nodo2, feedback):
        """
        📌 Ajusta la probabilidad de relación entre dos nodos según el feedback humano.
        - Si `feedback` es positivo, refuerza la relación.
        - Si `feedback` es negativo, debilita la relación.
        """
        if nodo1 not in self.memory_manager.graph or nodo2 not in self.memory_manager.graph:
            return "⚠️ No se pueden reforzar relaciones que no existen en la memoria."

        ajuste = 0.1 if feedback == "positivo" else -0.1
        self.memory_manager.reinforce_memory(nodo1, nodo2, ajuste)
        self.consciousness_engine.evaluate_action(nodo1, nodo2, feedback)

        return f"🔄 Relación '{nodo1}' ↔ '{nodo2}' ajustada según el feedback ({feedback})."
