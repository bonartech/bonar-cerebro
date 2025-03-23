import json
import networkx as nx
from core.consciousness_engine import ConsciousnessEngine
from core.memory_manager import MemoryManager

class FeedbackLoop:
    """
    📌 Módulo de retroalimentación de CEREBRO.
    Evalúa interacciones, ajusta la conciencia y refuerza la memoria con nuevas experiencias.
    """

    def __init__(self, feedback_file="data/feedback_log.json"):
        self.feedback_file = feedback_file
        self.memory = MemoryManager()
        self.consciousness = ConsciousnessEngine()
        self.feedback_log = self.load_feedback()

    def load_feedback(self):
        """Carga el historial de retroalimentación desde un archivo JSON."""
        try:
            with open(self.feedback_file, "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            print("⚠️ No se encontró un historial de feedback. Se inicia uno nuevo.")
            return []

    def save_feedback(self):
        """Guarda el historial de retroalimentación en un archivo JSON."""
        with open(self.feedback_file, "w", encoding="utf-8") as file:
            json.dump(self.feedback_log, file, indent=4)
        print("💾 Historial de feedback guardado correctamente.")

    def registrar_experiencia(self, decision, resultado):
        """Registra una experiencia en la conciencia y la memoria."""
        impacto = self.consciousness.evaluar_impacto(resultado)

        # 🔹 Guardar en el historial
        experiencia = {"decision": decision, "resultado": resultado, "impacto": impacto}
        self.feedback_log.append(experiencia)
        self.save_feedback()

        # 🔥 Ajustar conciencia
        self.consciousness.ajustar_conciencia(decision, impacto)

        # 🔥 Reforzar memoria si el impacto fue positivo
        if impacto > 0:
            self.memory.reinforce_memory(decision, resultado, incremento=0.5)

        return f"✅ Feedback registrado: {decision} → {resultado} (Impacto: {impacto})"

    def ajustar_pesos(self):
        """Ajusta los pesos de las conexiones en la memoria y conciencia con base en feedback."""
        for experiencia in self.feedback_log:
            decision, resultado, impacto = experiencia["decision"], experiencia["resultado"], experiencia["impacto"]
            self.consciousness.ajustar_conciencia(decision, impacto)

            if impacto > 0:
                self.memory.reinforce_memory(decision, resultado, incremento=0.3)
            elif impacto < 0:
                self.memory.reinforce_memory(decision, resultado, incremento=-0.3)

        print("🔄 Pesos ajustados en la memoria y conciencia.")

    def reflexionar_sobre_experiencias(self):
        """Analiza experiencias previas para mejorar el razonamiento."""
        print("🧠 Reflexión en proceso...")
        self.ajustar_pesos()
        print("✅ Reflexión completada.")