# QR Code Generator

Install the package:

```powershell
python -m pip install .
```

Start the graphical interface:

```powershell
qr-generator-ui
```

Alternatively, run the command-line interface:

```powershell
qr-generator
```

The original `python qr_generator_ui.py` and `python qr_generator.py` commands
also work from the project directory.

The application code is in `qr_code_generator/`. Enter a filename in the GUI or
CLI; generated QR codes are saved in `QRCodeGenerator/outputs/` under your home
directory. Directory paths are not accepted. The `.png` extension is added when
no extension is supplied. Existing files in the project's `outputs/` directory
are not moved automatically.

Application events and errors are recorded in
`QRCodeGenerator/logs/qr_generator.log` under your home directory. The input text
is not deliberately logged; error details may include file paths or other
exception messages.
