# QR Code Generator

## Install

Use the standard installer for your operating system:

- **Windows:** Run `QR-Code-Generator-Setup.exe`. It adds the app to the Start
  menu and offers an optional desktop shortcut. To remove it, use **Settings >
  Apps > Installed apps > QR Code Generator > Uninstall**.
- **Debian or Ubuntu:** Open the `.deb` installer in the Software app. To
  remove the app, use the Software app's installed-apps list.

The Windows setup executable and Debian/Ubuntu package are built by the
**Build Installers** GitHub Actions workflow. Download them from that
workflow's artifacts.

For development, the installed commands `qr-generator-ui` and `qr-generator`
launch the GUI and CLI. The original `python qr_generator_ui.py` and
`python qr_generator.py` commands also work from the project directory.

The application code is in `qr_code_generator/`. Enter a filename in the GUI or
CLI; generated QR codes are saved in `QRCodeGenerator/outputs/` under your home
directory. Directory paths are not accepted. The `.png` extension is added when
no extension is supplied. Existing files in the project's `outputs/` directory
are not moved automatically.

Application events and errors are recorded in
`QRCodeGenerator/logs/qr_generator.log` under your home directory. The input text
is not deliberately logged; error details may include file paths or other
exception messages.
