import unittest
from unittest.mock import patch

from qr_code_generator import launcher, ui


class LauncherTests(unittest.TestCase):
    def test_launches_gui(self):
        with patch.object(ui, "main") as main:
            launcher.main()
        main.assert_called_once()

    def test_reports_startup_error(self):
        with (
            patch.object(ui, "main", side_effect=OSError("cannot open log")),
            patch.object(launcher.messagebox, "showerror") as showerror,
        ):
            with self.assertRaises(OSError):
                launcher.main()
        showerror.assert_called_once_with(
            "Could not start QR Code Generator", "cannot open log"
        )


if __name__ == "__main__":
    unittest.main()
