# QR Code Generator

Install the package once using the Python interpreter that will launch it:

```text
python -m pip install .
```

On Linux, use `python3 -m pip install .` instead and ensure Tkinter is installed.

Then launch the graphical interface by double-clicking:

- **Windows:** `Launch QR Generator.pyw`. The `.pyw` file association must
  point to the Python installation with the package dependencies.
- **Linux:** `QR Code Generator.desktop`. The desktop entry and application
  icon are installed under the Python installation's data directory. The
  `python3` on your PATH must be the interpreter where you installed the
  package. Mark the desktop file executable and allow launching it if your
  desktop environment requires it.

The installed commands `qr-generator-ui` and `qr-generator` remain available
for launching the GUI and CLI, respectively. Alternatively, run the CLI with:

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
