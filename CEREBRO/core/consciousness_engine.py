import networkx as nx
import json

class ConsciousnessEngine:
    """
    📌 Motor de Conciencia de CEREBRO.
    Gestiona la identidad de la IA y su capacidad de autoevaluación.
    """

    def __init__(self, consciousness_file="data/consciousness_graph.json"):
        self.consciousness_file = consciousness_file
        self.graph = nx.Graph()
        self.load_consciousness()

    def load_consciousness(self):
        """Carga el grafo de conciencia desde un archivo JSON."""
        try:
            with open(self.consciousness_file, "r", encoding="utf-8") as file:
                data = json.load(file)
                self.graph = nx.node_link_graph(data)
            print("📂 Conciencia cargada con éxito.")
        except FileNotFoundError:
            print("⚠️ No se encontró un archivo de conciencia. Se inicia uno nuevo.")

    def save_consciousness(self):
        """Guarda el estado actual del grafo de conciencia en un archivo JSON."""
        with open(self.consciousness_file, "w", encoding="utf-8") as file:
            json.dump(nx.node_link_data(self.graph), file, indent=4)
        print("💾 Conciencia guardada correctamente.")

    def add_identity_attribute(self, atributo, valor):
        """Agrega o actualiza un atributo de identidad en la conciencia."""
        if not self.graph.has_node(atributo):
            self.graph.add_node(atributo, tipo="atributo", valor=valor)
        else:
            self.graph.nodes[atributo]["valor"] = valor
        print(f"✅ Identidad actualizada: {atributo} = {valor}")
        self.save_consciousness()

    def evaluate_decision(self, decision, impacto):
        """Registra cómo una decisión afectó a la IA."""
        if not self.graph.has_node(decision):
            self.graph.add_node(decision, tipo="decisión", impacto=impacto)
        else:
            self.graph.nodes[decision]["impacto"] += impacto
        print(f"📊 Evaluación de decisión: {decision} (Impacto: {impacto})")
        self.save_consciousness()

    def adjust_behavior(self):
        """Ajusta el comportamiento en función de experiencias pasadas."""
        decisiones = [(n, d["impacto"]) for n, d in self.graph.nodes(data=True) if d.get("tipo") == "decisión"]
        decisiones.sort(key=lambda x: x[1], reverse=True)  
        
        if decisiones:
            print("🧠 Reflexión sobre decisiones previas:")
            for decision, impacto in decisiones[:5]:  
                print(f" - {decision}: Impacto {impacto}")

    def relate_identity_to_decision(self, atributo, decision, peso=1.0):
        """Relaciona un atributo de identidad con una decisión."""
        if not self.graph.has_node(atributo) or not self.graph.has_node(decision):
            print(f"⚠️ No se puede relacionar {atributo} y {decision} porque uno de ellos no existe.")
            return
        
        if self.graph.has_edge(atributo, decision):
            self.graph[atributo][decision]["peso"] += peso
        else:
            self.graph.add_edge(atributo, decision, peso=peso)

        print(f"🔗 Relación creada: {atributo} ↔ {decision} (Peso: {peso})")
        self.save_consciousness()

    def should_restrict_response(self, text):
        """
        📌 Evalúa si la consulta del usuario debe restringirse según la conciencia de la IA.
        - Busca si el texto contiene términos que la IA ha aprendido a evitar.
        """
        restricted_words = [n for n, d in self.graph.nodes(data=True) if d.get("tipo") == "restricción"]
        
        for word in restricted_words:
            if word.lower() in text.lower():
                print(f"🚨 Restricción activada: {word}")
                return True  # No responder si la palabra está en la lista de restricciones
        
        return False

    def get_concept_info(self, concepto):
        """
        📌 Recupera la información almacenada en la conciencia sobre un concepto.
        - Devuelve atributos relacionados con la identidad y evaluaciones previas.
        """
        if concepto not in self.graph:
            return f"🤖 No tengo información sobre '{concepto}' en mi conciencia."

        info = self.graph.nodes[concepto]
        relaciones = list(self.graph.neighbors(concepto))
        impacto = info.get("impacto", "No evaluado")

        respuesta = f"🧠 En mi conciencia, '{concepto}' tiene estas características:\n"
        respuesta += f"🔹 Impacto: {impacto}\n"
        
        if relaciones:
            respuesta += f"🔗 Está relacionado con: {', '.join(relaciones)}"

        return respuesta