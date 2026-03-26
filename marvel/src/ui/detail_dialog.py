import requests
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QTextBrowser, QFrame
)

cache_imagenes = {}

class ImageLoader(QThread):
    finished = pyqtSignal(QPixmap)

    def __init__(self, url, width=280, height=380):
        super().__init__()
        self.url = url
        self.width = width
        self.height = height

    def run(self):
        pixmap = QPixmap(self.width, self.height)
        pixmap.fill(Qt.GlobalColor.transparent)

        if not self.url:
            self.finished.emit(pixmap)
            return

        if self.url in cache_imagenes:
            self.finished.emit(cache_imagenes[self.url])
            return

        try:
            response = requests.get(self.url, timeout=10)
            response.raise_for_status()
            pixmap.loadFromData(response.content)

            pixmap = pixmap.scaled(
                self.width,
                self.height,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )

            cache_imagenes[self.url] = pixmap

        except Exception:
            pass

        self.finished.emit(pixmap)

class DetailDialog(QDialog):
    def __init__(self, titulo, subtitulo, imagen_url, metadata, descripcion="", parent=None):
        super().__init__(parent)
        self.setWindowTitle(titulo)
        self.resize(780, 640)

        self.setStyleSheet("""
            QDialog {
                background-color: #111827;
                color: #F9FAFB;
            }
            QLabel#title {
                font-size: 24px;
                font-weight: 700;
                color: #F9FAFB;
            }
            QLabel#subtitle {
                font-size: 14px;
                color: #D1D5DB;
            }
            QLabel.info {
                font-size: 13px;
                color: #E5E7EB;
                padding: 4px 0;
            }
            QFrame.card {
                background-color: #1F2937;
                border: 1px solid #374151;
                border-radius: 18px;
                padding: 14px;
            }
            QTextBrowser {
                background-color: #111827;
                color: #F9FAFB;
                border: 1px solid #374151;
                border-radius: 12px;
                padding: 10px;
            }
        """)

        layout = QVBoxLayout(self)

        card = QFrame()
        card.setObjectName("card")
        card.setProperty("class", "card")
        card_layout = QVBoxLayout(card)

        title = QLabel(titulo)
        title.setObjectName("title")

        subtitle = QLabel(subtitulo)
        subtitle.setObjectName("subtitle")
        subtitle.setWordWrap(True)

        self.imagen = QLabel()
        self.imagen.setAlignment(Qt.AlignmentFlag.AlignCenter)

        placeholder = QPixmap(280, 380)
        placeholder.fill(Qt.GlobalColor.transparent)
        self.imagen.setPixmap(placeholder)

        self.loader = ImageLoader(imagen_url)
        self.loader.finished.connect(self.imagen.setPixmap)
        self.loader.start()

        card_layout.addWidget(title)
        card_layout.addWidget(subtitle)
        card_layout.addWidget(self.imagen)

        for key, value in metadata.items():
            label = QLabel(f"<b>{key}:</b> {value}")
            label.setProperty("class", "info")
            label.setWordWrap(True)
            card_layout.addWidget(label)

        descripcion_box = QTextBrowser()
        if descripcion:
            descripcion_box.setHtml(descripcion)
        else:
            descripcion_box.setPlainText("Sin descripción disponible.")

        layout.addWidget(card)
        layout.addWidget(descripcion_box)