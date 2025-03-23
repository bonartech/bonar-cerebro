
import tensorflow as tf
from CEREBRO.grapch_manager import cargar_grafo, guardar_grafo, mostrar_grafo
from CEREBRO.knowledge_engine import encadenamiento_de_pensamiento, reforzar_conexion,nlp
from GNN.model import convertir_grafo_para_gnn, entrenar_gnn


def menu():
    """Loop interactivo para el usuario."""
    global grafo  # Usar la variable global del grafo

    # 🔥 Cargar el grafo antes de procesar cualquier dato
    grafo = cargar_grafo()

    # 🚨 Verificación: ¿grafo está vacío?
    if not grafo or grafo.number_of_nodes() == 0:
        raise ValueError("❌ Error: El grafo no tiene nodos, no se puede entrenar la GNN.")

    # 🔥 Convertir el grafo antes de entrenar
    A, X, nodo_a_idx = convertir_grafo_para_gnn(grafo, nlp)

    # 🚨 Verificación: ¿X y A contienen valores válidos?
    if tf.reduce_any(tf.math.is_nan(X)):
        raise ValueError("❌ Error: X contiene valores NaN.")
    if tf.reduce_any(tf.math.is_nan(A)):
        raise ValueError("❌ Error: A contiene valores NaN.")

    modelo_gnn = entrenar_gnn(A, X, epochs=50, lr=0.01)

    while True:
        print("\n📌 **Menú Principal**")
        print("1️⃣ Consultar una relación")
        print("2️⃣ Aprender una nueva conexión")
        print("3️⃣ Ver el grafo actual")
        print("4️⃣ Salir")

        opcion = input("Selecciona una opción: ").strip()

        if opcion == "1":
            nodo1 = input("🔍 Ingresa el primer concepto: ").strip().lower()
            nodo2 = input("🔍 Ingresa el segundo concepto: ").strip().lower()
            print(encadenamiento_de_pensamiento(nodo1, nodo2, grafo, modelo_gnn, A, X, nodo_a_idx)) 

        elif opcion == "2":
            nodo1 = input("🧠 Ingresa el primer concepto: ").strip().lower()
            nodo2 = input("🧠 Ingresa el segundo concepto: ").strip().lower()
            reforzar_conexion(nodo1, nodo2, grafo)
            print(f"✅ '{nodo1}' ahora está conectado con '{nodo2}'.")

        elif opcion == "3":
            mostrar_grafo()

        elif opcion == "4":
            print("👋 Saliendo del sistema y guardando el grafo... 💾")
            guardar_grafo()
            break

        else:
            print("⚠️ Opción no válida. Intenta de nuevo.")