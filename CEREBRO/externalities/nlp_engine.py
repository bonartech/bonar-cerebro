import spacy
import unicodedata

class NLPEngine:
    """
    📌 Módulo de Procesamiento de Lenguaje Natural (NLP) para CEREBRO.
    - Normaliza texto.
    - Extrae entidades y conceptos clave.
    - Genera embeddings de palabras.
    """

    def __init__(self, model="es_core_news_md"):
        """
        📌 Inicializa el motor NLP cargando el modelo de spaCy.
        - `es_core_news_md` es un modelo en español con embeddings de 300 dimensiones.
        """
        try:
            self.nlp = spacy.load(model)
            print(f"✅ NLP Engine cargado con el modelo: {model}")
        except Exception as e:
            print(f"⚠️ Error al cargar el modelo NLP: {e}")

    def normalize_text(self, text):
        """
        📌 Normaliza texto convirtiéndolo a minúsculas y eliminando tildes.
        """
        text = text.lower().strip()
        return ''.join(c for c in unicodedata.normalize('NFKD', text) if not unicodedata.combining(c))

    def extract_keywords(self, text):
        """
        📌 Extrae palabras clave de un texto.
        - Se enfoca en sustantivos y nombres propios.
        """
        doc = self.nlp(text)
        return [token.lemma_ for token in doc if token.pos_ in ["NOUN", "PROPN"]]

    def get_embedding(self, text):
        """
        📌 Obtiene el embedding de una palabra o texto completo.
        - Si el texto no tiene embedding, devuelve un vector de ceros.
        """
        doc = self.nlp(text)
        return doc.vector if doc.vector_norm > 0 else [0.0] * 300

    def analyze_sentiment(self, text):
        """
        📌 Evalúa el sentimiento del texto en función de su estructura y palabras clave.
        - Se puede mejorar con modelos preentrenados específicos.
        """
        doc = self.nlp(text)
        score = sum([token.sentiment for token in doc]) / len(doc) if len(doc) > 0 else 0
        return round(score, 4)

    def process_text(self, text):
        """
        📌 Procesa el texto aplicando normalización y extracción de palabras clave.
        """
        text = self.normalize_text(text)
        keywords = self.extract_keywords(text)
        return " ".join(keywords) if keywords else text  # Si no hay keywords, usa el texto normalizado.
