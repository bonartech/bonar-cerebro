import tensorflow as tf

try:
    from tensorflow.keras.models import Model
    from tensorflow.keras.layers import Dense, Dropout
    print("✅ Módulos de Keras están correctamente instalados en TensorFlow.")
except ImportError as e:
    print(f"❌ Error: {e}")
