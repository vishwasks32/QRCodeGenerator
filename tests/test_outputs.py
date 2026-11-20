import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from qr_code_generator import generator, ui


class OutputTests(unittest.TestCase):
    def test_saves_in_outputs_and_adds_default_extension(self):
        with tempfile.TemporaryDirectory() as directory:
            output_dir = Path(directory) / "outputs"
            with patch.object(generator, "OUTPUT_DIR", output_dir):
                generator.generate_qr("example", "sample")
            self.assertTrue((output_dir / "sample.png").read_bytes().startswith(b"\x89PNG\r\n\x1a\n"))

    def test_rejects_paths_and_invalid_filenames(self):
        for filename in ("", ".", "..", "../outside.png", r"..\outside.png", r"C:\outside.png", "bad?.png"):
            with self.subTest(filename=filename):
                with self.assertRaises(ValueError):
                    generator.output_path(filename)

    def test_gui_cancel_overwrite_and_success(self):
        with tempfile.TemporaryDirectory() as directory:
            output_dir = Path(directory) / "outputs"
            output_dir.mkdir()
            existing = output_dir / "existing.png"
            existing.write_bytes(b"existing")
            with (
                patch.object(generator, "OUTPUT_DIR", output_dir),
                patch.object(ui, "configure_logging"),
                patch.object(ui.tk, "Tk"),
                patch.object(ui.ttk, "Frame"),
                patch.object(ui.ttk, "Label"),
                patch.object(ui.ttk, "Entry") as entry,
                patch.object(ui.ttk, "Button") as button,
                patch.object(ui.simpledialog, "askstring") as ask,
                patch.object(ui.messagebox, "askyesno", return_value=False),
                patch.object(ui.messagebox, "showinfo"),
            ):
                entry.return_value.get.return_value = "example"
                ui.main()
                save = button.call_args.kwargs["command"]
                ask.return_value = None
                save()
                ask.return_value = "existing.png"
                save()
                self.assertEqual(existing.read_bytes(), b"existing")
                entry.return_value.delete.assert_not_called()
                ask.return_value = "new"
                save()
                self.assertTrue((output_dir / "new.png").exists())
                entry.return_value.delete.assert_called_once()


if __name__ == "__main__":
    unittest.main()
