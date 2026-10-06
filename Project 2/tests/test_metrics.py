import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from common.metrics import cer, edit_counts, wer


class MetricTests(unittest.TestCase):
    def test_known_levenshtein_distance(self):
        result = edit_counts("kitten", "sitting")
        self.assertEqual(result.errors, 3)
        self.assertEqual(result.reference_length, 6)

    def test_exact_match(self):
        self.assertEqual(cer("hello", "hello").rate, 0.0)
        self.assertEqual(wer("hello world", "hello world").rate, 0.0)

    def test_word_error(self):
        result = wer("the brown fox", "the fox")
        self.assertEqual(result.deletions, 1)
        self.assertAlmostEqual(result.rate, 1 / 3)

    def test_normalization(self):
        self.assertEqual(cer("Hello  WORLD", "hello world", normalize=True).rate, 0.0)

    def test_empty_reference(self):
        self.assertEqual(cer("", "").rate, 0.0)
        self.assertEqual(cer("", "x").rate, 1.0)


if __name__ == "__main__":
    unittest.main()
