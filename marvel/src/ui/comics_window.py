from math import ceil
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QLabel, QLineEdit,
    QPushButton, QComboBox, QFrame, QTextBrowser, QMessageBox
)

from src.servicios.comic_s import ComicService
from src.ui.detail_dialog import DetailDialog, load_pixmap_from_url


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
                color: #F8FAFC;
            }
            QLabel#muted {
                color: #94A3B8;
                font-size: 13px;
            }
            QLineEdit, QComboBox, QListWidget, QTextBrowser {
                background-color: #1E293B;
                color: #F8FAFC;
                border: 1px solid #334155;
                border-radius: 12px;
                padding: 10px;
            }
            QPushButton {
                background-color: #DC2626;
                color: white;
                border: none;
                border-radius: 12px;
                padding: 10px 14px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #B91C1C;
            }
            QPushButton.secondary {
                background-color: #1E293B;
                border: 1px solid #334155;
            }
            QPushButton.secondary:hover {
                background-color: #273449;
            }
        """)

        root = QVBoxLayout(self)

        titulo = QLabel("Catálogo de Comics Marvel")
        titulo.setObjectName("title")
        subtitulo = QLabel("Minimalista, con búsqueda, ordenamiento, paginación e imagen.")
        subtitulo.setObjectName("muted")

        root.addWidget(titulo)
        root.addWidget(subtitulo)

        top = QHBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar por título o año...")

        self.sort_combo = QComboBox()
        self.sort_combo.addItems([
            "Nombre A-Z",
            "Nombre Z-A",
            "Fecha reciente",
            "Fecha antigua"
        ])

        btn_filtrar = QPushButton("Filtrar")
        btn_filtrar.clicked.connect(self.aplicar_filtros)

        btn_actualizar = QPushButton("Buscar")
        btn_actualizar.setProperty("class", "secondary")
        btn_actualizar.clicked.connect(self.actualizar_desde_api)

        top.addWidget(self.search_input, 2)
        top.addWidget(self.sort_combo, 1)
        top.addWidget(btn_filtrar)
        top.addWidget(btn_actualizar)

        root.addLayout(top)

        content = QHBoxLayout()

        left_card = QFrame()
        left_card.setProperty("class", "card")
        left_layout = QVBoxLayout(left_card)

        self.lista = QListWidget()
        self.lista.itemSelectionChanged.connect(self.mostrar_detalle)
        self.lista.itemDoubleClicked.connect(self.abrir_dialogo_detalle)

        left_layout.addWidget(self.lista)

        nav = QHBoxLayout()

        self.btn_prev = QPushButton("← Anterior")
        self.btn_prev.setProperty("class", "secondary")
        self.btn_prev.clicked.connect(self.pagina_anterior)

        self.lbl_pagina = QLabel("Página 1 / 1")
        self.lbl_pagina.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.btn_next = QPushButton("Siguiente →")
        self.btn_next.setProperty("class", "secondary")
        self.btn_next.clicked.connect(self.pagina_siguiente)

        nav.addWidget(self.btn_prev)
        nav.addWidget(self.lbl_pagina, 1)
        nav.addWidget(self.btn_next)

        left_layout.addLayout(nav)

        right_card = QFrame()
        right_card.setProperty("class", "card")
        right_layout = QVBoxLayout(right_card)

        self.image_label = QLabel("Sin imagen")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.detail_title = QLabel("Selecciona un comic")
        self.detail_title.setObjectName("title")
        self.detail_title.setStyleSheet("font-size: 20px;")

        self.detail_meta = QLabel("Aquí aparecerán los detalles.")
        self.detail_meta.setWordWrap(True)

        self.detail_desc = QTextBrowser()
        self.detail_desc.setPlainText("Sin descripción.")

        self.btn_dialog = QPushButton("Ver detalle completo")
        self.btn_dialog.clicked.connect(self.abrir_dialogo_detalle)

        right_layout.addWidget(self.image_label)
        right_layout.addWidget(self.detail_title)
        right_layout.addWidget(self.detail_meta)
        right_layout.addWidget(self.detail_desc, 1)
        right_layout.addWidget(self.btn_dialog)

        content.addWidget(left_card, 3)
        content.addWidget(right_card, 2)

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
            QMessageBox.information(self, "Listo", "Comics actualizados desde la API.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo actualizar:\n{e}")

    def aplicar_filtros(self):
        texto = self.search_input.text().strip().lower()

        filtrados = []
        for comic in self.todos:
            titulo = comic.nombre.lower()
            fecha = (comic.fecha_publicacion or "")[:4]
            if not texto or texto in titulo or texto in fecha:
                filtrados.append(comic)

        criterio = self.sort_combo.currentText()

        if criterio == "Nombre A-Z":
            filtrados.sort(key=lambda c: c.nombre.lower())
        elif criterio == "Nombre Z-A":
            filtrados.sort(key=lambda c: c.nombre.lower(), reverse=True)
        elif criterio == "Fecha reciente":
            filtrados.sort(key=lambda c: c.fecha_publicacion or "", reverse=True)
        elif criterio == "Fecha antigua":
            filtrados.sort(key=lambda c: c.fecha_publicacion or "")

        self.filtrados = filtrados
        self.pagina_actual = 1
        self.mostrar_pagina()

    def mostrar_pagina(self):
        self.lista.clear()
        self.items_pagina = []

        total_paginas = max(1, ceil(len(self.filtrados) / self.por_pagina))

        if self.pagina_actual > total_paginas:
            self.pagina_actual = total_paginas

        self.items_pagina = self.service.paginar_comics(
            self.filtrados,
            self.pagina_actual,
            self.por_pagina
        )

        if not self.items_pagina:
            self.lista.addItem("No hay comics para mostrar.")
            self.limpiar_detalle()
        else:
            for comic in self.items_pagina:
                fecha = comic.fecha_publicacion[:10] if comic.fecha_publicacion else "Sin fecha"
                self.lista.addItem(f"{comic.nombre}  •  {fecha}")

            self.lista.setCurrentRow(0)

        self.lbl_pagina.setText(f"Página {self.pagina_actual} / {total_paginas}")
        self.btn_prev.setEnabled(self.pagina_actual > 1)
        self.btn_next.setEnabled(self.pagina_actual < total_paginas)

    def comic_actual(self):
        row = self.lista.currentRow()
        if row < 0 or row >= len(self.items_pagina):
            return None
        return self.items_pagina[row]

    def mostrar_detalle(self):
        comic = self.comic_actual()
        if comic is None:
            return

        creadores = ", ".join([c.nombre for c in comic.creadores[:4]]) or "Sin creadores"

        self.detail_title.setText(comic.nombre)
        self.detail_meta.setText(
            f"<b>Editorial:</b> {comic.editorial or 'No disponible'}<br>"
            f"<b>Volumen:</b> {comic.volumen or 'No disponible'}<br>"
            f"<b>Fecha:</b> {comic.fecha_publicacion or 'No disponible'}<br>"
            f"<b>Creadores:</b> {creadores}"
        )
        self.detail_desc.setHtml(comic.descripcion or comic.descripcion_corta or "Sin descripción.")
        self.image_label.setPixmap(load_pixmap_from_url(comic.imagen_url))

    def abrir_dialogo_detalle(self):
        comic = self.comic_actual()
        if comic is None:
            return

        creadores = ", ".join([c.nombre for c in comic.creadores[:6]]) or "Sin creadores"

        dialog = DetailDialog(
            titulo=comic.nombre,
            subtitulo=comic.volumen or "Comic Marvel",
            imagen_url=comic.imagen_url,
            metadata={
                "Editorial": comic.editorial or "No disponible",
                "Fecha": comic.fecha_publicacion or "No disponible",
                "Volumen": comic.volumen or "No disponible",
                "Creadores": creadores
            },
            descripcion=comic.descripcion or comic.descripcion_corta or "Sin descripción.",
            parent=self
        )
        dialog.exec()

    def limpiar_detalle(self):
        self.detail_title.setText("Selecciona un comic")
        self.detail_meta.setText("Aquí aparecerán los detalles.")
        self.detail_desc.setPlainText("Sin descripción.")
        self.image_label.setText("Sin imagen")

    def pagina_siguiente(self):
        self.pagina_actual += 1
        self.mostrar_pagina()

    def pagina_anterior(self):
        self.pagina_actual -= 1
        self.mostrar_pagina()