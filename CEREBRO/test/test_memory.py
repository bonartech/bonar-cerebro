import unittest

import networkx as nx
import numpy as np
from core.memory_manager import MemoryManager
from scipy.sparse import coo_matrix

class TestMemory(unittest.TestCase):
    def setUp(self):
        self.memory = MemoryManager()

    def test_add_memory(self):
        self.memory.add_memory("perro", "animal", 1.5)
        related = self.memory.get_related_concepts("perro")
        self.assertTrue(any("animal" in pair for pair in related))


        # 🚀 Cargar el grafo desde MemoryManager


if __name__ == "__main__":
    unittest.main()
