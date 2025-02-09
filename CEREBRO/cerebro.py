import networkx as nx
import spacy
import pickle
import os
import unicodedata

import numpy as np
import networkx as nx
import spektral
import tensorflow as tf

from GNN.model import GrafoNeuronal
# Cargar modelo de lenguaje con embeddings semánticos y lematización
nlp = spacy.load("es_core_news_md")

# Nombre del archivo donde se guardará el grafo
GRAFO_FILENAME = "grafo_cerebro.pkl"



def convertir_grafo_para_gnn():
    """Convierte el grafo de NetworkX a un formato compatible con Spektral (TensorFlow)"""
    global grafo

    # Asignar IDs numéricos a cada nodo
    nodos = list(grafo.nodes)
    nodo_a_idx = {nodo: idx for idx, nodo in enumerate(nodos)}

    # Crear matriz de adyacencia y atributos de nodos
    A = nx.to_numpy_array(grafo, nodelist=nodos)  # Matriz de adyacencia
    X = np.array([nlp(nodo).vector for nodo in nodos])  # Embeddings de nodos con spaCy

    # Convertir a formato TensorFlow
    A = tf.convert_to_tensor(A, dtype=tf.float32)
    X = tf.convert_to_tensor(X, dtype=tf.float32)

    print("✅ Grafo convertido para TensorFlow y Spektral")
    return A, X, nodo_a_idx

def entrenar_gnn(A, X, epochs=50, lr=0.01):
    modelo = GrafoNeuronal(input_dim=X.shape[1], hidden_dim=32)
    modelo.compile(optimizer=tf.keras.optimizers.Adam(lr), loss="mse")

    for epoch in range(epochs):
        loss = modelo.train_on_batch([X, A], A)  # Aprender conexiones
        if epoch % 10 == 0:
            print(f"🔄 Epoch {epoch}/{epochs} - Pérdida: {loss:.4f}")

    print("✅ GNN entrenada con éxito")
    return modelo

def predecir_nueva_conexion(modelo, nodo1, nodo2, A, X, nodo_a_idx):
    """Usa la GNN para predecir la fuerza de conexión entre dos nodos"""
    if nodo1 not in nodo_a_idx or nodo2 not in nodo_a_idx:
        return f"⚠️ '{nodo1}' o '{nodo2}' no existen en el grafo."

    idx1, idx2 = nodo_a_idx[nodo1], nodo_a_idx[nodo2]

    emb1, emb2 = modelo([X, A])[idx1], modelo([X, A])[idx2]
    distancia = np.linalg.norm(emb1.numpy() - emb2.numpy())

    return f"🔮 Predicción de relación '{nodo1}' ↔ '{nodo2}': {1 / (1 + distancia):.4f}"


def normalizar_texto(texto):
    """Convierte el texto a minúsculas, elimina tildes y caracteres especiales."""
    texto = texto.lower().strip()
    texto = ''.join(c for c in unicodedata.normalize('NFKD', texto) if not unicodedata.combining(c))
    return texto

def guardar_grafo():
    """Guarda el grafo en un archivo para persistencia."""
    with open(GRAFO_FILENAME, "wb") as f:
        pickle.dump(grafo, f)

def cargar_grafo():
    """Carga el grafo desde un archivo si existe y valida que todos los nodos tengan un tipo."""
    global grafo
    if os.path.exists(GRAFO_FILENAME):
        try:
            with open(GRAFO_FILENAME, "rb") as f:
                grafo = pickle.load(f)
            print("📂 Grafo cargado con éxito.")

            # 🔥 Asegurar que todos los nodos tengan el atributo 'tipo'
            for nodo in grafo.nodes:
                if 'tipo' not in grafo.nodes[nodo]:
                    grafo.nodes[nodo]['tipo'] = "concepto"

            # Guardar el grafo actualizado
            guardar_grafo()

        except (EOFError, pickle.UnpicklingError):
            print("⚠️ Archivo del grafo vacío o corrupto. Creando un nuevo grafo.")
            grafo = nx.Graph()
    else:
        print("⚠️ No se encontró un grafo previo. Creando uno nuevo.")
        grafo = nx.Graph()

# Cargar el grafo al iniciar el programa
cargar_grafo()

def calcular_peso_dinamico(nodo1, nodo2):
    """Calcula el peso de una relación basado en embeddings y conexiones previas."""
    if nodo1 not in grafo or nodo2 not in grafo:
        return 1  # Peso base

    conexiones_comunes = set(grafo.neighbors(nodo1)).intersection(set(grafo.neighbors(nodo2)))
    refuerzo_conexiones = len(conexiones_comunes) * 0.1

    doc1, doc2 = nlp(nodo1), nlp(nodo2)
    
    # Verificar si ambos nodos tienen embeddings válidos
    if doc1.vector_norm > 0 and doc2.vector_norm > 0:
        refuerzo_embedding = doc1.similarity(doc2)
    else:
        refuerzo_embedding = 0  # No aplicar refuerzo si no hay embeddings

    return 1 + refuerzo_conexiones + (refuerzo_embedding if refuerzo_embedding > 0.7 else 0)

def procesar_texto_y_construir_grafo(texto):
    """Extrae conceptos clave y crea un grafo de conocimiento basado en relaciones del texto."""
    doc = nlp(texto)
    nodos_creados = set()

    for token in doc:
        if token.pos_ in ["NOUN", "PROPN"]:  
            nodo_actual = normalizar_texto(token.lemma_)

            if nodo_actual not in grafo:
                grafo.add_node(nodo_actual, tipo="concepto")
                nodos_creados.add(nodo_actual)

            for vecino in token.sent:
                if vecino.lemma_.lower() != nodo_actual and vecino.pos_ in ["NOUN", "PROPN"]:
                    nodo_vecino = normalizar_texto(vecino.lemma_)
                    if nodo_vecino not in grafo:
                        grafo.add_node(nodo_vecino, tipo="concepto")
                        nodos_creados.add(nodo_vecino)

                    peso_relacion = calcular_peso_dinamico(nodo_actual, nodo_vecino)

                    if grafo.has_edge(nodo_actual, nodo_vecino):
                        grafo[nodo_actual][nodo_vecino]["peso"] += peso_relacion
                    else:
                        grafo.add_edge(nodo_actual, nodo_vecino, peso=peso_relacion)

    guardar_grafo()
    return nodos_creados

def reforzar_conexion(nodo1, nodo2, incremento=0.5):
    """Aumenta el peso de una relación cuando se usa o se aprende una nueva conexión."""
    if grafo.has_edge(nodo1, nodo2):
        grafo[nodo1][nodo2]["peso"] += incremento
    else:
        grafo.add_edge(nodo1, nodo2, peso=incremento)
    guardar_grafo()

def buscar_relacion_mas_cercana(nodo):
    """Busca la mejor relación usando embeddings sin preguntar al usuario."""
    nodo = normalizar_texto(nodo)
    if nodo not in grafo:
        return None

    max_similitud = 0.0
    mejor_relacion = None

    for otro_nodo in grafo.nodes:
        if otro_nodo == nodo:
            continue
        similitud = nlp(nodo).similarity(nlp(otro_nodo))
        if similitud > max_similitud:
            max_similitud = similitud
            mejor_relacion = otro_nodo

    return mejor_relacion if max_similitud > 0.7 else None

def encadenamiento_de_pensamiento(nodo_inicio, nodo_destino, max_pasos=3):
    """Busca una ruta lógica entre dos conceptos y genera una explicación."""
    nodo_inicio = normalizar_texto(nodo_inicio)
    nodo_destino = normalizar_texto(nodo_destino)

    if nodo_inicio not in grafo or nodo_destino not in grafo:
        mejor_relacion = buscar_relacion_mas_cercana(nodo_inicio)
        if mejor_relacion:
            reforzar_conexion(nodo_inicio, mejor_relacion)
            return f"⚠️ No tenía información sobre '{nodo_inicio}', pero ahora lo conecté con '{mejor_relacion}' automáticamente."

        return f"⚠️ No encontré una relación fuerte para '{nodo_inicio}' y '{nodo_destino}'."

    try:
        ruta = nx.shortest_path(grafo, source=nodo_inicio, target=nodo_destino)
        if len(ruta) <= max_pasos:
            return f"🔎 '{nodo_inicio}' está relacionado con '{nodo_destino}' a través de: {' → '.join(ruta)}."
        return f"⚠️ '{nodo_inicio}' y '{nodo_destino}' están conectados, pero la relación es demasiado indirecta."
    except nx.NetworkXNoPath:
        mejor_relacion = buscar_relacion_mas_cercana(nodo_inicio)
        if mejor_relacion:
            reforzar_conexion(nodo_inicio, mejor_relacion)
            return f"⚠️ '{nodo_inicio}' no tenía conexión, pero ahora está relacionado con '{mejor_relacion}'."
        return f"⚠️ No había conexión clara entre '{nodo_inicio}' y '{nodo_destino}', y no encontré una relación fuerte."

def mostrar_grafo():
    """Muestra los nodos y conexiones del grafo generado."""
    print("\n🔍 **Nodos en el Grafo:**")
    for nodo in grafo.nodes:
        print(f"- {nodo} (Tipo: {grafo.nodes[nodo]['tipo']})")

    print("\n🔗 **Conexiones:**")
    for nodo1, nodo2, data in grafo.edges(data=True):
        print(f"- {nodo1} ↔ {nodo2} (Peso: {data['peso']:.2f})")

# 🚀 Ahora la IA aprenderá relaciones automáticamente sin necesidad de preguntar siempre
texto_real = "El tigre es un felino carnívoro de gran tamaño que habita en Asia."
procesar_texto_y_construir_grafo(texto_real)
mostrar_grafo()
