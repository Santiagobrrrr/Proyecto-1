import sys
from PyQt6.QtWidgets import QApplication
from config import validate_config
from src.ui.interfaz_grafica import MainWindow


if __name__ == "__main__":
    validate_config()

    app = QApplication(sys.argv)
    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec())