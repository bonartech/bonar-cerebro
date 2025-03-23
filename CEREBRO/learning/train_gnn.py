import os
import networkx as nx
import numpy as np
from learning.gnn_model import entrenar_gnn
import tensorflow as tf
from core.memory_manager import MemoryManager
from externalities.nlp_engine import NLPEngine
 # 🔥 Importamos el servicio sin clases

def generate_model():
    MODEL_PATH = "models/gnn_model.h5"
    os.makedirs("models", exist_ok=True)

    if os.path.exists(MODEL_PATH):
        print(f"✅ Modelo GNN encontrado en {MODEL_PATH}, no es necesario regenerarlo.")
        return
    
    print("⚙️ Iniciando la generación del modelo GNN...")

    # 📚 Cargar memoria y NLP
    memory = MemoryManager()  # ✅ Pasamos el objeto MemoryManager, no `graphs`
    nlp = NLPEngine()

    print("🏋️ Entrenando la GNN con los datos convertidos...")
    model = entrenar_gnn(memory, nlp.get_embedding)  # ✅ Pasamos `memory`, no `graphs`

    # 📌 Guardar el modelo entrenado
    model.save_weights(MODEL_PATH)
    print(f"✅ Modelo GNN guardado en {MODEL_PATH}")
