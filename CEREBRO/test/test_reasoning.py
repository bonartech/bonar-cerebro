import unittest
from core.reasoning import ReasoningEngine

class TestReasoning(unittest.TestCase):
    def setUp(self):
        self.engine = ReasoningEngine()

    def test_basic_reasoning(self):
        result = self.engine.process_query("¿Qué es el fuego?")
        self.assertIsInstance(result, str)
        self.assertNotEqual(result, "")

if __name__ == "__main__":
    unittest.main()
