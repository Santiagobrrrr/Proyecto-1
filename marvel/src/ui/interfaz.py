import requests
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (
    QFrame, QLabel, QVBoxLayout, QPushButton
)


def load_pixmap_from_url(url, width=170, height=220):
    pixmap = QPixmap(width, height)
    pixmap.fill(Qt.GlobalColor.transparent)

    if not url:
        return pixmap

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        pixmap.loadFromData(response.content)
        return pixmap.scaled(
            width,
            height,
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation
        )
    except Exception:
        return pixmap


def clear_layout(layout):
    while layout.count():
        item = layout.takeAt(0)
        widget = item.widget()
        child_layout = item.layout()

        if widget is not None:
            widget.deleteLater()
        elif child_layout is not None:
            clear_layout(child_layout)


class ComicCard(QFrame):
    def __init__(self, comic, on_click):
        super().__init__()
        self.comic = comic
        self.on_click = on_click

        self.setObjectName("card")
        self.setFixedWidth(210)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)

        image = QLabel()
        image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        image.setPixmap(load_pixmap_from_url(comic.imagen_url, 180, 220))

        titulo = QLabel(comic.nombre)
        titulo.setObjectName("cardTitle")
        titulo.setWordWrap(True)
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        meta = QLabel((comic.fecha_publicacion or "Sin fecha")[:10])
        meta.setObjectName("cardMeta")
        meta.setAlignment(Qt.AlignmentFlag.AlignCenter)

        btn = QPushButton("Ver cómic")
        btn.clicked.connect(lambda: self.on_click(self.comic))

        layout.addWidget(image)
        layout.addWidget(titulo)
        layout.addWidget(meta)
        layout.addWidget(btn)


class CharacterCard(QFrame):
    def __init__(self, personaje, on_click):
        super().__init__()
        self.personaje = personaje
        self.on_click = on_click

        self.setObjectName("card")
        self.setFixedWidth(210)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)

        image = QLabel()
        image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        image.setPixmap(load_pixmap_from_url(personaje.imagen_url, 180, 220))

        titulo = QLabel(personaje.nombre)
        titulo.setObjectName("cardTitle")
        titulo.setWordWrap(True)
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        meta_text = personaje.nombre_real or personaje.editorial or "Sin detalle"
        meta = QLabel(meta_text)
        meta.setObjectName("cardMeta")
        meta.setWordWrap(True)
        meta.setAlignment(Qt.AlignmentFlag.AlignCenter)

        btn = QPushButton("Ver perfil")
        btn.clicked.connect(lambda: self.on_click(self.personaje))

        layout.addWidget(image)
        layout.addWidget(titulo)
        layout.addWidget(meta)
        layout.addWidget(btn)