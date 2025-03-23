from core.memory_manager import MemoryManager
from core.consciousness_engine import ConsciousnessEngine

class KnowledgeUpdater:
    """
    📌 Módulo de actualización del conocimiento de CEREBRO.
    Administra la evolución del conocimiento y la conciencia.
    """

    def __init__(self):
        self.memory = MemoryManager()
        self.consciousness = ConsciousnessEngine()

    def update_knowledge(self, concepto1, concepto2, impacto):
        """Actualiza el conocimiento y ajusta la conciencia según el impacto."""

        # 🔥 Se añade el conocimiento al grafo de memoria
        self.memory.add_memory(concepto1, concepto2, peso=abs(impacto))

        # 🧠 Se registra la evaluación en la conciencia
        if impacto > 0:
            self.consciousness.add_consciousness(concepto1, "positivo", peso=impacto)
        else:
            self.consciousness.add_consciousness(concepto1, "negativo", peso=abs(impacto))

        print(f"🔄 Conocimiento actualizado: {concepto1} ↔ {concepto2} (Impacto: {impacto})")

