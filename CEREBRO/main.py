import os
import time
from core.memory_manager import MemoryManager
from core.consciousness_engine import ConsciousnessEngine
from core.reasoning import ReasoningEngine
from learning.reinforcement_learning import ReinforcementLearning
from learning.predictor import Predictor
from externalities.nlp_engine import NLPEngine
from core.feedback_loop import FeedbackLoop
from config.settings import Settings
from learning.train_gnn import generate_model  # 🔥 Importamos la función de entrenamiento de GNN

def main():
    """
    🎯 Punto de entrada de CEREBRO.
    - Carga la memoria y conciencia.
    - Inicia el motor de razonamiento y el predictor de relaciones.
    - Procesa las consultas del usuario utilizando memoria, conciencia y NLP.
    """
    print("🧠 CEREBRO: Sistema de Razonamiento y Conciencia")

    # 📂 Verificar y entrenar el modelo GNN si no existe
    MODEL_PATH = "models/gnn_model.h5"
    if not os.path.exists(MODEL_PATH):
        print("⚙️ No se encontró el modelo GNN. Generando uno nuevo...")
        generate_model()  # 🔥 Entrenamos la GNN si no está guardada
    else:
        print(f"✅ Modelo GNN encontrado en {MODEL_PATH}.")

    # 🔹 Cargar módulos principales con manejo de errores
    try:
        print("📂 Cargando memoria y conciencia...")
        memory = MemoryManager()
        consciousness = ConsciousnessEngine()
        reasoning = ReasoningEngine()
        learning_agent = ReinforcementLearning()
        predictor = Predictor(memory, consciousness)
        feedback_loop = FeedbackLoop()
        nlp = NLPEngine()

        print("✅ Memoria y conciencia listas.")
    except Exception as e:
        print(f"❌ Error al cargar los módulos principales: {e}")
        return  # Detener ejecución en caso de fallo crítico

    # 🔹 Definir identidad inicial si no está presente
    if "identidad" not in consciousness.graph:
        consciousness.add_identity_attribute("identidad", "CEREBRO - IA basada en conciencia y razonamiento")

    num_interacciones = 0

    while True:
        try:
            query = input("\n🔍 Ingresa una pregunta (o 'salir' para terminar): ").strip()
            if query.lower() == "salir":
                print("👋 Saliendo del sistema...")
                memory.save_memory()
                consciousness.save_consciousness()
                feedback_loop.save_feedback()
                break

            print("🤔 Procesando...")

            # 🔹 1. Preprocesar la consulta con NLP
            clean_query = nlp.normalize_text(query)

            # 🔹 2. Consultar RL antes de responder
            if learning_agent.evaluar_accion(clean_query, "respuesta") < 0:
                print("⚠️ He dado malas respuestas en el pasado sobre esto. Intentaré mejorar mi respuesta.")

            # 🔹 3. Verificar la conciencia antes de responder
            if consciousness.should_restrict_response(clean_query):
                print("🧠 CEREBRO: No puedo responder a eso según mi conciencia.")
                continue



            # 🔹 5. Generar respuesta usando motor de razonamiento
            reasoning_response = reasoning.process_query(clean_query)

            print(f"🧠 CEREBRO: {reasoning_response}")

            # 🔹 8. Pedir feedback y ajustar aprendizaje
            feedback = input("📊 ¿Esta respuesta fue útil? (sí/no): ").strip().lower()
            if feedback == "no":
                learning_agent.actualizar_q_value(clean_query, "respuesta", -1.0, "nuevo_estado", ["mejorar"])
                consciousness.evaluate_decision(clean_query, -1.0)
                print("🔄 Ajustando comportamiento basado en feedback negativo...")
                consciousness.adjust_behavior()
            else:
                learning_agent.actualizar_q_value(clean_query, "respuesta", 1.0, "nuevo_estado", ["mejorar"])
                consciousness.evaluate_decision(clean_query, 1.0)

            # 🔹 9. Registrar feedback en el sistema
            feedback_loop.registrar_experiencia(clean_query, feedback)

            # 🔹 10. Reflexionar sobre decisiones pasadas después de 3 interacciones
            num_interacciones += 1
            if num_interacciones % 3 == 0:
                print("🔄 Reflexionando sobre experiencias pasadas...")
                reasoning.reflexionar()

            time.sleep(1)

        except Exception as e:
            print(f"❌ Error durante la ejecución de la interacción: {e}")
            continue  # Para evitar que el programa se cierre si hay errores en la interacción


if __name__ == "__main__":
    main()
