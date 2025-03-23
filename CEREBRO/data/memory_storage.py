import json
import os

class MemoryStorage:
    """
    📌 Módulo de almacenamiento de memoria en CEREBRO.
    - Gestiona recuerdos y experiencias previas.
    """

    def __init__(self, storage_path="data/memory_data.json"):
        self.storage_path = storage_path
        self.memory = {}
        self.load_memory()

    def load_memory(self):
        """📂 Carga la memoria desde un archivo JSON."""
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, "r", encoding="utf-8") as file:
                    self.memory = json.load(file)
                print("✅ Memoria de experiencias cargada con éxito.")
            except Exception as e:
                print(f"⚠️ Error al cargar la memoria: {e}")
        else:
            print("⚠️ No se encontró un archivo de memoria. Se inicia uno nuevo.")

    def save_memory(self):
        """💾 Guarda la memoria en un archivo JSON."""
        try:
            with open(self.storage_path, "w", encoding="utf-8") as file:
                json.dump(self.memory, file, indent=4)
            print("✅ Memoria guardada correctamente.")
        except Exception as e:
            print(f"⚠️ Error al guardar la memoria: {e}")

    def store_experience(self, key, value):
        """📌 Almacena una experiencia específica en la memoria."""
        if key not in self.memory:
            self.memory[key] = []
        self.memory[key].append(value)
        print(f"🧠 Nueva experiencia almacenada en {key}: {value}")
        self.save_memory()

    def retrieve_experience(self, key):
        """📌 Recupera experiencias almacenadas relacionadas con una clave."""
        return self.memory.get(key, [])
