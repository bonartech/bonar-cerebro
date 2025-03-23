import networkx as nx
from core.memory_manager import MemoryManager
from core.consciousness_engine import ConsciousnessEngine

class ReasoningEngine:
    """
    📌 Módulo de razonamiento de CEREBRO.
    Analiza información de la memoria y la conciencia para tomar decisiones informadas.
    """

    def __init__(self):
        self.memory = MemoryManager()
        self.consciousness = ConsciousnessEngine()

    def inferir_relacion(self, concepto1, concepto2):
        """Intenta determinar la relación entre dos conceptos utilizando la memoria."""
        if concepto1 not in self.memory.graph or concepto2 not in self.memory.graph:
            return f"⚠️ No tengo suficiente información para relacionar '{concepto1}' con '{concepto2}'."

        try:
            ruta = nx.shortest_path(self.memory.graph, source=concepto1, target=concepto2)
            return f"🔎 '{concepto1}' está relacionado con '{concepto2}' a través de: {' → '.join(ruta)}."
        except nx.NetworkXNoPath:
            return f"⚠️ No hay una relación directa entre '{concepto1}' y '{concepto2}'."

    def evaluar_decision(self, decision):
        """Evalúa una decisión basada en la conciencia y experiencias previas."""
        impacto = self.consciousness.graph.nodes.get(decision, {}).get("impacto", 0)
        
        if impacto > 0:
            return f"✅ La decisión '{decision}' ha sido evaluada como positiva (Impacto: {impacto})."
        elif impacto < 0:
            return f"⚠️ La decisión '{decision}' ha tenido consecuencias negativas (Impacto: {impacto})."
        else:
            return f"❓ No hay información suficiente para evaluar la decisión '{decision}'."
        
    def generar_respuesta(self, consulta):
        """📌 Genera una respuesta combinando memoria y conciencia."""
        memoria_info = self.memory.get_related_concepts(consulta)
        conciencia_info = self.consciousness.get_concept_info(consulta)

        partes_respuesta = []
        if memoria_info:
            partes_respuesta.append(f"📚 En mi memoria, '{consulta}' se relaciona con: " + ", ".join([c[0] for c in memoria_info]))
        if conciencia_info:
            partes_respuesta.append(conciencia_info)

        if not partes_respuesta:
            return "🤖 No tengo suficiente información. ¿Podrías enseñármelo?"

        return "\n".join(partes_respuesta)


    def reflexionar(self):
        """Reflexiona sobre las decisiones pasadas y ajusta el razonamiento."""
        print("🧠 Reflexión en proceso...")
        self.consciousness.adjust_behavior()
        print("✅ Reflexión completada.")

    def process_query(self, query):
        """
        📌 Procesa una consulta del usuario y genera una respuesta basada en la memoria y la conciencia.
        """
        query = query.lower().strip()

        # 🔎 Verificar si la consulta es sobre una relación entre conceptos
        palabras = query.split()
        if "es" in palabras and len(palabras) == 3:
            concepto1, _, concepto2 = palabras
            return self.inferir_relacion(concepto1, concepto2)

        # 🔍 Evaluar si es una pregunta de decisión
        if query.startswith("qué pasa si"):
            decision = query.replace("qué pasa si", "").strip()
            return self.evaluar_decision(decision)

        # 🔬 Generar respuesta basada en memoria
        return self.generar_respuesta(query)