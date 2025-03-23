import unittest
from learning.reinforcement_learning import ReinforcementAgent

class TestLearning(unittest.TestCase):
    def setUp(self):
        self.agent = ReinforcementAgent()

    def test_learn_action(self):
        self.agent.learn("decir la verdad", 1.0)
        q_value = self.agent.get_q_value("decir la verdad")
        self.assertGreater(q_value, 0)

if __name__ == "__main__":
    unittest.main()
