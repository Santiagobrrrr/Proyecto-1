from math import ceil
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QLabel, QLineEdit,
    QPushButton, QComboBox, QFrame, QTextBrowser, QMessageBox
)

from src.servicios.comic_s import ComicService
from src.ui.detail_dialog import DetailDialog


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

        import requests
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

class ComicsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Comics Marvel")
        self.service = ComicService()

        self.todos = []
        self.filtrados = []
        self.pagina_actual = 1
        self.por_pagina = 10
        self.items_pagina = []

        self.loader = None

        self._build_ui()
        self.cargar_comics()

    def _build_ui(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #0F172A;
                color: #F8FAFC;
                font-family: Segoe UI;
            }
            QFrame.card {
                background-color: #111827;
                border: 1px solid #334155;
                border-radius: 18px;
            }
            QLabel#title {
                font-size: 26px;
                font-weight: 700;
            }
            QLabel#muted {
                color: #94A3B8;
                font-size: 13px;
            }
        """)

        root = QVBoxLayout(self)

        titulo = QLabel("Catálogo de Comics Marvel")
        titulo.setObjectName("title")

        subtitulo = QLabel("Búsqueda, ordenamiento y paginación.")
        subtitulo.setObjectName("muted")

        root.addWidget(titulo)
        root.addWidget(subtitulo)

        top = QHBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar...")

        self.sort_combo = QComboBox()
        self.sort_combo.addItems([
            "Nombre A-Z", "Nombre Z-A", "Fecha reciente", "Fecha antigua"
        ])

        btn_filtrar = QPushButton("Aplicar")
        btn_filtrar.clicked.connect(self.aplicar_filtros)

        btn_actualizar = QPushButton("Buscar")
        btn_actualizar.clicked.connect(self.actualizar_desde_api)

        top.addWidget(self.search_input, 2)
        top.addWidget(self.sort_combo, 1)
        top.addWidget(btn_filtrar)
        top.addWidget(btn_actualizar)

        root.addLayout(top)

        content = QHBoxLayout()

        self.lista = QListWidget()
        self.lista.itemSelectionChanged.connect(self.mostrar_detalle)

        content.addWidget(self.lista, 3)

        right = QVBoxLayout()

        self.image_label = QLabel("Cargando...")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.detail_title = QLabel("Selecciona un comic")
        self.detail_meta = QLabel("")
        self.detail_desc = QTextBrowser()

        right.addWidget(self.image_label)
        right.addWidget(self.detail_title)
        right.addWidget(self.detail_meta)
        right.addWidget(self.detail_desc)

        content.addLayout(right, 2)

        root.addLayout(content)

    def cargar_comics(self):
        comics = self.service.cargar_comics_desde_json()
        if not comics:
            comics = self.service.guardar_comics_desde_api(limit=20)

        self.todos = comics
        self.aplicar_filtros()

    def actualizar_desde_api(self):
        try:
            self.todos = self.service.guardar_comics_desde_api(limit=20)
            self.aplicar_filtros()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def aplicar_filtros(self):
        texto = self.search_input.text().lower()

        filtrados = [
            c for c in self.todos
            if texto in c.nombre.lower() or texto in (c.fecha_publicacion or "")
        ]

        self.filtrados = filtrados
        self.pagina_actual = 1
        self.mostrar_pagina()

    def mostrar_pagina(self):
        self.lista.clear()

        self.items_pagina = self.service.paginar_comics(
            self.filtrados,
            self.pagina_actual,
            self.por_pagina
        )

        for comic in self.items_pagina:
            self.lista.addItem(comic.nombre)

        if self.items_pagina:
            self.lista.setCurrentRow(0)

    def comic_actual(self):
        row = self.lista.currentRow()
        if row < 0 or row >= len(self.items_pagina):
            return None
        return self.items_pagina[row]

    def mostrar_detalle(self):
        comic = self.comic_actual()
        if not comic:
            return

        self.detail_title.setText(comic.nombre)
        self.detail_meta.setText(comic.fecha_publicacion or "")
        self.detail_desc.setHtml(comic.descripcion or "Sin descripción")

        # Placeholder
        placeholder = QPixmap(280, 380)
        placeholder.fill(Qt.GlobalColor.transparent)
        self.image_label.setPixmap(placeholder)

        # HILO
        self.loader = ImageLoader(comic.imagen_url)
        self.loader.finished.connect(self.image_label.setPixmap)
        self.loader.start()

    def abrir_dialogo_detalle(self):
        comic = self.comic_actual()
        if not comic:
            return

        dialog = DetailDialog(
            titulo=comic.nombre,
            subtitulo=comic.volumen or "",
            imagen_url=comic.imagen_url,
            metadata={},
            descripcion=comic.descripcion or ""
        )
        dialog.exec()