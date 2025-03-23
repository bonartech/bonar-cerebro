class Hyperparameters:
    """
    📌 Parámetros de entrenamiento para GNN y Reinforcement Learning en CEREBRO.
    - Controla el aprendizaje del sistema.
    - Ajusta la eficiencia del modelo de razonamiento.
    """

    # 📈 Configuración de la GNN
    GNN_INPUT_DIM = 300  # Dimensión del embedding de nodos
    GNN_HIDDEN_DIM = 64  # Tamaño de la capa oculta
    GNN_OUTPUT_DIM = 32  # Dimensión de salida
    GNN_LR = 0.005  # Learning rate de la GNN
    GNN_EPOCHS = 50  # Número de épocas de entrenamiento
    GNN_BATCH_SIZE = 32  # Tamaño del batch para entrenar

    # 🎯 Configuración del Reinforcement Learning (RL)
    RL_DISCOUNT_FACTOR = 0.95  # Factor de descuento para RL (gamma)
    RL_LEARNING_RATE = 0.01  # Learning rate del agente
    RL_EXPLORATION_DECAY = 0.995  # Decadencia de la exploración
    RL_MIN_EPSILON = 0.01  # Valor mínimo de exploración
    RL_MAX_MEMORY_SIZE = 10000  # Capacidad máxima de memoria de experiencias
    RL_BATCH_SIZE = 64  # Tamaño del batch en el entrenamiento de RL

    @classmethod
    def display_hyperparameters(cls):
        """📌 Muestra los hiperparámetros del sistema."""
        print(f"📈 Hiperparámetros de CEREBRO:")
        print(f"   🧠 GNN - Input Dim: {cls.GNN_INPUT_DIM}, Hidden Dim: {cls.GNN_HIDDEN_DIM}, Output Dim: {cls.GNN_OUTPUT_DIM}")
        print(f"   🔧 GNN - Learning Rate: {cls.GNN_LR}, Epochs: {cls.GNN_EPOCHS}, Batch Size: {cls.GNN_BATCH_SIZE}")
        print(f"   🎯 RL - Discount Factor: {cls.RL_DISCOUNT_FACTOR}, Learning Rate: {cls.RL_LEARNING_RATE}")
        print(f"   🔄 RL - Exploration Decay: {cls.RL_EXPLORATION_DECAY}, Min Epsilon: {cls.RL_MIN_EPSILON}")
        print(f"   🧠 RL - Memory Size: {cls.RL_MAX_MEMORY_SIZE}, Batch Size: {cls.RL_BATCH_SIZE}")


