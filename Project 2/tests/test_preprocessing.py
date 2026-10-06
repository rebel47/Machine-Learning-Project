import sys
import unittest
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from common.degradation import apply_degradation
from common.preprocessing import binarize, clean_document, four_point_transform


class PreprocessingTests(unittest.TestCase):
    def setUp(self):
        self.image = np.full((100, 160, 3), 255, dtype=np.uint8)
        self.image[35:65, 40:120] = 0

    def test_clean_document_shape(self):
        final, stages, angle = clean_document(self.image)
        self.assertEqual(final.shape, self.image.shape[:2])
        self.assertEqual(set(stages), {"01_gray", "02_denoised", "03_binary", "04_deskewed"})
        self.assertIsInstance(angle, float)

    def test_binary_values(self):
        result = binarize(self.image[:, :, 0])
        self.assertTrue(set(np.unique(result)).issubset({0, 255}))

    def test_degradations_preserve_shape(self):
        for kind in ("blur", "noise", "rotation", "low_contrast", "occlusion"):
            with self.subTest(kind=kind):
                self.assertEqual(apply_degradation(self.image, kind, 0.5).shape, self.image.shape)

    def test_perspective_transform(self):
        points = np.array([[0, 0], [159, 0], [159, 99], [0, 99]])
        transformed = four_point_transform(self.image, points)
        self.assertGreater(transformed.size, 0)


if __name__ == "__main__":
    unittest.main()
