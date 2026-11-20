import logging
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from qr_code_generator import generator, logging_config, ui


class LoggingTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.log_dir = Path(self.directory.name) / "logs"
        self.log_dir_patch = patch.object(logging_config, "LOG_DIR", self.log_dir)
        self.log_dir_patch.start()
        self.output_dir_patch = patch.object(
            generator, "OUTPUT_DIR", Path(self.directory.name) / "outputs"
        )
        self.output_dir_patch.start()
        self.logger = logging.getLogger("qr_generator")
        self.original_handlers = self.logger.handlers[:]
        self.original_level = self.logger.level
        self.original_propagate = self.logger.propagate
        self.logger.handlers.clear()

    def tearDown(self):
        for handler in self.logger.handlers[:]:
            self.logger.removeHandler(handler)
            handler.close()
        self.logger.handlers.extend(self.original_handlers)
        self.logger.setLevel(self.original_level)
        self.logger.propagate = self.original_propagate
        self.output_dir_patch.stop()
        self.log_dir_patch.stop()
        self.directory.cleanup()

    def test_cli_logs_success_without_logging_input(self):
        with patch("builtins.input", side_effect=["private input", "qr.png"]):
            generator.main()
        logging_config.configure_logging()
        log = (self.log_dir / "qr_generator.log").read_text(encoding="utf-8")
        self.assertIn("CLI started", log)
        self.assertEqual(log.count("QR code saved successfully"), 1)
        self.assertNotIn("private input", log)
        self.assertEqual(len(self.logger.handlers), 1)

    def test_cli_logs_and_reraises_save_failure(self):
        blocked_dir = Path(self.directory.name) / "not_a_directory"
        blocked_dir.write_text("file", encoding="utf-8")
        with (
            patch.object(generator, "OUTPUT_DIR", blocked_dir),
            patch("builtins.input", side_effect=["private input", "qr.png"]),
        ):
            with self.assertRaises(OSError):
                generator.main()
        log = (self.log_dir / "qr_generator.log").read_text(encoding="utf-8")
        self.assertIn("Could not generate or save QR code", log)
        self.assertNotIn("QR code saved successfully", log)

    def test_gui_logs_save_failure(self):
        with (
            patch.object(ui.tk, "Tk"),
            patch.object(ui.ttk, "Frame"),
            patch.object(ui.ttk, "Label"),
            patch.object(ui.ttk, "Entry") as entry,
            patch.object(ui.ttk, "Button") as button,
            patch.object(ui.simpledialog, "askstring", return_value="qr.png"),
            patch.object(ui.messagebox, "showerror") as showerror,
            patch.object(ui, "generate_qr", side_effect=OSError("save failed")),
        ):
            entry.return_value.get.return_value = "private input"
            ui.main()
            button.call_args.kwargs["command"]()
            showerror.assert_called_once()
            entry.return_value.delete.assert_not_called()
        log = (self.log_dir / "qr_generator.log").read_text(encoding="utf-8")
        self.assertIn("GUI started", log)
        self.assertIn("Could not generate or save QR code", log)
        self.assertIn("OSError: save failed", log)
        self.assertNotIn("private input", log)


if __name__ == "__main__":
    unittest.main()
