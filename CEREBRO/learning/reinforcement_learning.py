import numpy as np
import random
import json

class ReinforcementLearning:
    """
    📌 Aprendizaje por Refuerzo (RL) en CEREBRO.
    Permite ajustar el comportamiento en función de experiencias previas.
    """

    def __init__(self, rl_memory_file="data/rl_memory.json", learning_rate=0.1, discount_factor=0.9, exploration_rate=0.2):
        self.rl_memory_file = rl_memory_file
        self.learning_rate = learning_rate  # Qué tan rápido aprende
        self.discount_factor = discount_factor  # Cuánto valora experiencias pasadas
        self.exploration_rate = exploration_rate  # Probabilidad de probar algo nuevo
        self.q_table = {}  # Tabla de valores Q para decisiones
        self.load_rl_memory()

    def load_rl_memory(self):
        """Carga la memoria de refuerzo desde un archivo JSON."""
        try:
            with open(self.rl_memory_file, "r", encoding="utf-8") as file:
                self.q_table = json.load(file)
            print("📂 Memoria de refuerzo cargada con éxito.")
        except FileNotFoundError:
            print("⚠️ No se encontró un archivo de memoria de RL. Se inicia uno nuevo.")
            self.q_table = {}

    def save_rl_memory(self):
        """Guarda la tabla de valores Q en un archivo JSON."""
        with open(self.rl_memory_file, "w", encoding="utf-8") as file:
            json.dump(self.q_table, file, indent=4)
        print("💾 Memoria de refuerzo guardada correctamente.")

    def elegir_accion(self, estado, acciones):
        """
        📌 Elige una acción basada en la tabla de valores Q.
        Puede explorar (accion aleatoria) o explotar (accion con mejor recompensa).
        """
        if estado not in self.q_table:
            self.q_table[estado] = {accion: 0 for accion in acciones}

        if random.uniform(0, 1) < self.exploration_rate:
            return random.choice(acciones)  # Explorar acción nueva
        else:
            return max(self.q_table[estado], key=self.q_table[estado].get)  # Usar mejor acción conocida

    def actualizar_q_value(self, estado, accion, recompensa, nuevo_estado, acciones):
        """
        📌 Ajusta la tabla de valores Q según la recompensa obtenida.
        """
        if estado not in self.q_table:
            self.q_table[estado] = {accion: 0 for accion in acciones}

        if nuevo_estado not in self.q_table:
            self.q_table[nuevo_estado] = {accion: 0 for accion in acciones}

        mejor_futuro = max(self.q_table[nuevo_estado].values()) if self.q_table[nuevo_estado] else 0

        # Fórmula de actualización de Q-learning
        self.q_table[estado][accion] = self.q_table[estado][accion] + self.learning_rate * (
                recompensa + self.discount_factor * mejor_futuro - self.q_table[estado][accion])

        self.save_rl_memory()

    def evaluar_accion(self, estado, accion):
        """
        📌 Devuelve el valor actual de una acción en un estado dado.
        """
        if estado in self.q_table and accion in self.q_table[estado]:
            return self.q_table[estado][accion]
        return 0
    
    def learn(self, estado, recompensa):
        """
        📌 Aprende del estado y la recompensa dada.
        Se usa cuando se obtiene retroalimentación de la interacción.
        """
        if estado not in self.q_table:
            self.q_table[estado] = {}

        if "aprendizaje" not in self.q_table[estado]:
            self.q_table[estado]["aprendizaje"] = 0

        self.q_table[estado]["aprendizaje"] += recompensa
        self.save_rl_memory()
        print(f"🧠 Aprendizaje registrado para '{estado}' con recompensa: {recompensa}")