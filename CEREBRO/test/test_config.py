import unittest
from config.settings import Settings
from config.hyperparameters import Hyperparameters

class TestConfig(unittest.TestCase):
    def test_settings(self):
        self.assertEqual(Settings.LOG_LEVEL, "INFO")

    def test_hyperparameters(self):
        self.assertGreater(Hyperparameters.GNN_LR, 0)

if __name__ == "__main__":
    unittest.main()
