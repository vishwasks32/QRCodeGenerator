from tkinter import messagebox


def main():
    try:
        from .ui import main as launch_ui

        launch_ui()
    except (ImportError, OSError) as error:
        messagebox.showerror("Could not start QR Code Generator", str(error))
        raise


if __name__ == "__main__":
    main()
