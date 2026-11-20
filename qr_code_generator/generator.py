import logging
from pathlib import Path

import qrcode
from qrcode.exceptions import DataOverflowError

from .logging_config import configure_logging
from .paths import DATA_DIR


logger = logging.getLogger("qr_generator.generator")
OUTPUT_DIR = DATA_DIR / "outputs"


def output_path(filename):
    if (
        not filename
        or filename in (".", "..")
        or filename[-1] in (".", " ")
        or any(char in filename for char in '<>:"/\\|?*')
    ):
        raise ValueError("Enter a filename without a directory path or invalid characters.")
    if not Path(filename).suffix:
        filename += ".png"
    return OUTPUT_DIR / filename


def generate_qr(url, filename=None):
    if filename is None:
        filename = input("Enter the filename to save the QR code (e.g., qrcode.png): ")
    path = output_path(filename)
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    img.save(path)
    logger.info("QR code saved successfully")
    print(f"QR code saved as {path}")


def main():
    configure_logging()
    logger.info("CLI started")
    url = input("Enter the URL to generate QR code: ")
    try:
        generate_qr(url)
    except (OSError, ValueError, DataOverflowError):
        logger.exception("Could not generate or save QR code")
        raise


if __name__ == "__main__":
    main()