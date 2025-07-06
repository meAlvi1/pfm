import platform
from utils import setup_logging

def main():
    setup_logging()
    if platform.system() == "Windows":
        from gui import create_gui
        create_gui()
    else:
        from cli import cli_main
        cli_main()

if __name__ == "__main__":
    main()
