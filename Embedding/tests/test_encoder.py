import unittest
from embedding.encoder import TextEncoder
from embedding.config import EmbeddingConfig

class TestTextEncoder(unittest.TestCase):
    def setUp(self):
        self.encoder = TextEncoder(EmbeddingConfig())

    def test_single_vector(self):
        vec = self.encoder.get_vector("Xin chào")
        self.assertEqual(len(vec), 384)

    def test_batch_vectors(self):
        texts = ["Xin chào", "Tạm biệt"]
        vecs = self.encoder.get_vectors(texts)
        self.assertEqual(len(vecs), 2)

if __name__ == "__main__":
    unittest.main()
