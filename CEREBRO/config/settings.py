import os

class Settings:
    """
    📌 Configuración general del sistema CEREBRO.
    - Define rutas de almacenamiento.
    - Configura parámetros básicos de operación.
    - Permite personalización mediante variables de entorno.
    """

    # 📂 Rutas de almacenamiento
    MEMORY_STORAGE_PATH = os.getenv("MEMORY_STORAGE_PATH", "data/memory_data.json")
    GRAPH_STORAGE_PATH = os.getenv("GRAPH_STORAGE_PATH", "data/graph_data.json")

    # 🔧 Configuración del procesador de lenguaje natural
    NLP_MODEL = os.getenv("NLP_MODEL", "es_core_news_md")  # Modelo de spaCy

    # 📊 Configuración de logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")  # INFO, DEBUG, ERROR

    # 💾 Configuración de persistencia
    AUTO_SAVE_INTERVAL = int(os.getenv("AUTO_SAVE_INTERVAL", "30"))  # Guardado automático cada X segundos

    @classmethod
    def display_settings(cls):
        """📌 Muestra la configuración actual del sistema."""
        print(f"🔧 Configuración del sistema CEREBRO:")
        print(f"   📂 Ruta de almacenamiento de memoria: {cls.MEMORY_STORAGE_PATH}")
        print(f"   📂 Ruta de almacenamiento de grafos: {cls.GRAPH_STORAGE_PATH}")
        print(f"   🧠 Modelo NLP en uso: {cls.NLP_MODEL}")
        print(f"   📝 Nivel de logging: {cls.LOG_LEVEL}")
        print(f"   💾 Guardado automático cada {cls.AUTO_SAVE_INTERVAL} segundos")


