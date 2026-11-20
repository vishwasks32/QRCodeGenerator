import logging
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

from qrcode.exceptions import DataOverflowError

from .generator import generate_qr, output_path
from .logging_config import configure_logging


logger = logging.getLogger("qr_generator.ui")


def main():
    configure_logging()
    logger.info("GUI started")
    root = tk.Tk()
    root.title("QR Code Generator")
    root.resizable(False, False)

    frame = ttk.Frame(root, padding=20)
    frame.grid(sticky="nsew")

    ttk.Label(frame, text="URL or text:").grid(row=0, column=0, sticky="w")
    entry = ttk.Entry(frame, width=50)
    entry.grid(row=1, column=0, pady=(5, 15), sticky="ew")
    entry.focus()

    def save_qr():
        value = entry.get().strip()
        if not value:
            messagebox.showwarning("Missing input", "Enter a URL or text to generate a QR code.", parent=root)
            return

        filename = simpledialog.askstring(
            "Save QR code",
            "Enter a filename. QR codes are saved in the outputs folder:",
            initialvalue="qrcode.png",
            parent=root,
        )
        if filename is None:
            return

        try:
            path = output_path(filename)
            if path.exists() and not messagebox.askyesno(
                "Replace file?", f"{path.name} already exists. Replace it?", parent=root
            ):
                return
            generate_qr(value, filename)
        except (OSError, ValueError, DataOverflowError) as error:
            logger.exception("Could not generate or save QR code")
            messagebox.showerror("Could not save QR code", str(error), parent=root)
            return
        entry.delete(0, tk.END)
        messagebox.showinfo("QR code saved", f"QR code saved as {path}", parent=root)

    ttk.Button(frame, text="Generate and save", command=save_qr).grid(row=2, column=0, sticky="e")
    root.mainloop()


if __name__ == "__main__":
    main()
