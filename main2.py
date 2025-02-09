from CEREBRO.cerebro import (
    encadenamiento_de_pensamiento,
    cargar_grafo,
    reforzar_conexion,
    mostrar_grafo,
    guardar_grafo,
)
from GNN.model import convertir_grafo_para_gnn, entrenar_gnn



def menu():
    """Loop interactivo para el usuario."""
    global grafo  # Si `grafo` es una variable global en tu sistema, úsala aquí

    # 🔥 Cargar el grafo y entrenar la GNN antes de iniciar el menú
    cargar_grafo()
    A, X, nodo_a_idx = convertir_grafo_para_gnn()  # Convertimos el grafo para la GNN
    modelo_gnn = entrenar_gnn(A, X, epochs=50, lr=0.01)  # Entrenamos la GNN

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
            print(encadenamiento_de_pensamiento(nodo1, nodo2, grafo, modelo_gnn, A, X, nodo_a_idx))  # ✅ Pasamos los argumentos necesarios

        elif opcion == "2":
            nodo1 = input("🧠 Ingresa el primer concepto: ").strip().lower()
            nodo2 = input("🧠 Ingresa el segundo concepto: ").strip().lower()
            reforzar_conexion(nodo1, nodo2, grafo)  # ✅ Ahora `grafo` es un argumento explícito
            print(f"✅ '{nodo1}' ahora está conectado con '{nodo2}'.")

        elif opcion == "3":
            mostrar_grafo()

        elif opcion == "4":
            print("👋 Saliendo del sistema y guardando el grafo... 💾")
            guardar_grafo()
            break

        else:
            print("⚠️ Opción no válida. Intenta de nuevo.")

# **📌 Iniciar ciclo interactivo**
if __name__ == "__main__":
    menu()
