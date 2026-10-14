import os
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from common.ocr import recognize, require_tesseract


class TesseractTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name).resolve()
        self.pytesseract = SimpleNamespace(
            pytesseract=SimpleNamespace(tesseract_cmd="tesseract"),
            image_to_string=Mock(return_value="  recognized text\n"),
        )
        for context in (
            patch.dict(os.environ, {}, clear=True),
            patch.dict(sys.modules, {"pytesseract": self.pytesseract}),
            patch("common.ocr.sys.platform", "win32"),
        ):
            context.start()
            self.addCleanup(context.stop)

    def install(self, variable="ProgramFiles", folder="Tesseract-OCR"):
        root = self.root / variable
        os.environ[variable] = str(root)
        executable = root / folder / "tesseract.exe"
        executable.parent.mkdir(parents=True, exist_ok=True)
        executable.touch()
        return str(executable.resolve())

    def test_explicit_override_takes_precedence(self):
        self.install()
        override = str(self.root / "custom" / "tesseract.exe")
        os.environ["TESSERACT_CMD"] = override
        with patch("common.ocr.shutil.which", return_value=override) as which:
            self.assertIsNone(require_tesseract())
        which.assert_called_once_with(override)
        self.assertEqual(self.pytesseract.pytesseract.tesseract_cmd, override)

    def test_invalid_override_does_not_fall_back(self):
        self.install()
        for override in ("missing-tesseract", ""):
            with self.subTest(override=override):
                os.environ["TESSERACT_CMD"] = override
                with patch("common.ocr.shutil.which", return_value=None):
                    with self.assertRaisesRegex(RuntimeError, "TESSERACT_CMD"):
                        require_tesseract()

    def test_path_takes_precedence_over_windows_locations(self):
        self.install()
        executable = str(self.root / "on-path" / "tesseract.exe")
        with patch("common.ocr.shutil.which", return_value=executable) as which:
            require_tesseract()
        which.assert_called_once_with("tesseract")
        self.assertEqual(self.pytesseract.pytesseract.tesseract_cmd, executable)

    def test_windows_installations_without_path(self):
        locations = (
            ("ProgramFiles", "Tesseract-OCR"),
            ("ProgramFiles(x86)", "Tesseract-OCR"),
            ("LOCALAPPDATA", "Programs/Tesseract-OCR"),
            ("LOCALAPPDATA", "Tesseract-OCR"),
        )
        for variable, folder in locations:
            with self.subTest(variable=variable, folder=folder):
                with patch.dict(os.environ, {}, clear=True):
                    executable = self.install(variable, folder)
                    with patch("common.ocr.shutil.which", return_value=None):
                        require_tesseract()
                    self.assertEqual(self.pytesseract.pytesseract.tesseract_cmd, executable)
                    Path(executable).unlink()

    def test_missing_engine_has_windows_installation_guidance(self):
        with patch("common.ocr.shutil.which", return_value=None):
            with self.assertRaisesRegex(RuntimeError, "winget install --id UB-Mannheim"):
                require_tesseract()

    def test_non_windows_does_not_search_windows_locations(self):
        self.install()
        with patch("common.ocr.sys.platform", "linux"):
            with patch("common.ocr.shutil.which", return_value=None):
                with self.assertRaisesRegex(RuntimeError, "Tesseract was not found"):
                    require_tesseract()

    def test_recognize_uses_discovered_executable_and_preserves_options(self):
        executable = self.install()
        image = np.zeros((10, 10), dtype=np.uint8)
        with patch("common.ocr.shutil.which", return_value=None):
            self.assertEqual(recognize(image, language="deu", psm=11), "recognized text")
        self.assertEqual(self.pytesseract.pytesseract.tesseract_cmd, executable)
        self.pytesseract.image_to_string.assert_called_once_with(
            image, lang="deu", config="--psm 11",
        )


if __name__ == "__main__":
    unittest.main()
