import unittest
from core.consciousness_engine import ConsciousnessEngine

class TestConsciousness(unittest.TestCase):
    def setUp(self):
        self.consciousness = ConsciousnessEngine()

    def test_update_consciousness(self):
        self.consciousness.update_consciousness("mentir", -1.0)
        score = self.consciousness.get_consciousness_score("mentir")
        self.assertLess(score, 0)

if __name__ == "__main__":
    unittest.main()
