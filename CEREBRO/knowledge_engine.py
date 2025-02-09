import networkx as nx
from CEREBRO.text_processor import normalizar_texto, nlp
from GNN.predict import predecir_nueva_conexion

def calcular_peso_dinamico(nodo1, nodo2, grafo):
    """Calcula el peso de una relación basado en embeddings y conexiones previas."""
    if nodo1 not in grafo or nodo2 not in grafo:
        return 1  # Peso base si no existen en el grafo

    conexiones_comunes = set(grafo.neighbors(nodo1)).intersection(set(grafo.neighbors(nodo2)))
    refuerzo_conexiones = len(conexiones_comunes) * 0.1

    doc1, doc2 = nlp(nodo1), nlp(nodo2)
    refuerzo_embedding = doc1.similarity(doc2) if doc1.vector_norm > 0 and doc2.vector_norm > 0 else 0

    return 1 + refuerzo_conexiones + (refuerzo_embedding if refuerzo_embedding > 0.7 else 0)

def reforzar_conexion(nodo1, nodo2, grafo, incremento=0.5):
    """Aumenta el peso de una relación cuando se usa o se aprende una nueva conexión."""
    if grafo.has_edge(nodo1, nodo2):
        grafo[nodo1][nodo2]["peso"] += incremento
    else:
        grafo.add_edge(nodo1, nodo2, peso=incremento)

def buscar_relacion_mas_cercana(nodo, grafo):
    """Busca la mejor relación usando embeddings."""
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

def encadenamiento_de_pensamiento(nodo_inicio, nodo_destino, grafo, modelo_gnn, A, X, nodo_a_idx, max_pasos=3):
    """Busca una ruta lógica entre dos conceptos y genera una explicación, usando GNN si es necesario."""
    nodo_inicio = normalizar_texto(nodo_inicio)
    nodo_destino = normalizar_texto(nodo_destino)

    if nodo_inicio not in grafo or nodo_destino not in grafo:
        mejor_relacion = buscar_relacion_mas_cercana(nodo_inicio, grafo)
        if mejor_relacion:
            reforzar_conexion(nodo_inicio, mejor_relacion, grafo)
            return f"⚠️ No tenía información sobre '{nodo_inicio}', pero ahora lo conecté con '{mejor_relacion}' automáticamente."

        return f"⚠️ No encontré una relación fuerte para '{nodo_inicio}' y '{nodo_destino}'."

    try:
        ruta = nx.shortest_path(grafo, source=nodo_inicio, target=nodo_destino)
        if len(ruta) <= max_pasos:
            return f"🔎 '{nodo_inicio}' está relacionado con '{nodo_destino}' a través de: {' → '.join(ruta)}."
        
        # 🔥 Aquí se usa la GNN para predecir una posible relación si la conexión es demasiado indirecta
        print(f"⚠️ '{nodo_inicio}' y '{nodo_destino}' están conectados, pero la relación es demasiado indirecta.")
        return f"Intentando predecir una relación con la GNN..."

    except nx.NetworkXNoPath:
        # 🚀 Si no hay conexión, usamos la GNN para predecir si debería haber una
        print(f"⚠️ No hay conexión directa entre '{nodo_inicio}' y '{nodo_destino}', usando la GNN...")
        probabilidad_conexion = predecir_nueva_conexion(modelo_gnn, nodo_inicio, nodo_destino, A, X, nodo_a_idx)

        if float(probabilidad_conexion.split(': ')[1]) > 0.7:  # Si la predicción es alta, conectamos los nodos
            reforzar_conexion(nodo_inicio, nodo_destino, grafo)
            return f"🔮 La GNN predijo una relación entre '{nodo_inicio}' y '{nodo_destino}', ahora están conectados."

        return f"⚠️ No había conexión clara entre '{nodo_inicio}' y '{nodo_destino}', y la GNN tampoco predijo una fuerte relación."
