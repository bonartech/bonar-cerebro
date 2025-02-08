from cerebro import (
    encadenamiento_de_pensamiento,
    cargar_grafo,
    reforzar_conexion,
    mostrar_grafo,
    guardar_grafo,

)

def menu():
    """Loop interactivo para el usuario."""
    while True:
        cargar_grafo()
        print("\n📌 **Menú Principal**")
        print("1️⃣ Consultar una relación")
        print("2️⃣ Aprender una nueva conexión")
        print("3️⃣ Ver el grafo actual")
        print("4️⃣ Salir")

        opcion = input("Selecciona una opción: ").strip()

        if opcion == "1":
            nodo1 = input("🔍 Ingresa el primer concepto: ").strip().lower()
            nodo2 = input("🔍 Ingresa el segundo concepto: ").strip().lower()
            print(encadenamiento_de_pensamiento(nodo1, nodo2))

        elif opcion == "2":
            nodo1 = input("🧠 Ingresa el primer concepto: ").strip().lower()
            nodo2 = input("🧠 Ingresa el segundo concepto: ").strip().lower()
            reforzar_conexion(nodo1, nodo2)
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
