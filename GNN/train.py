import tensorflow as tf

from GNN.model import GrafoNeuronal


def entrenar_gnn(A, X, epochs=50, lr=0.01):
    modelo = GrafoNeuronal(input_dim=X.shape[1])
    modelo.compile(optimizer=tf.keras.optimizers.Adam(lr), loss="mse")

    for epoch in range(epochs):
        loss = modelo.train_on_batch([X, A], A)
        if epoch % 10 == 0:
            print(f"🔄 Epoch {epoch}/{epochs} - Pérdida: {loss:.4f}")

    print("✅ GNN entrenada con éxito")
    return modelo
