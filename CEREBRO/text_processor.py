import spacy
import unicodedata

from CEREBRO.knowledge_engine import calcular_peso_dinamico

nlp = spacy.load("es_core_news_md")

def normalizar_texto(texto):
    """Convierte el texto a minúsculas y elimina tildes."""
    texto = texto.lower().strip()
    return ''.join(c for c in unicodedata.normalize('NFKD', texto) if not unicodedata.combining(c))

def procesar_texto_y_construir_grafo(texto, grafo):
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

                    peso_relacion = calcular_peso_dinamico(nodo_actual, nodo_vecino, grafo)

                    if grafo.has_edge(nodo_actual, nodo_vecino):
                        grafo[nodo_actual][nodo_vecino]["peso"] += peso_relacion
                    else:
                        grafo.add_edge(nodo_actual, nodo_vecino, peso=peso_relacion)

    return nodos_creados
