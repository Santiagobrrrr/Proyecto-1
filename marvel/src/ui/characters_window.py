from math import ceil

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QLabel, QLineEdit,
    QPushButton, QComboBox, QFrame, QTextBrowser, QMessageBox
)
from src.servicios.personaje_s import PersonajeService
from src.ui.detail_dialog import DetailDialog, load_pixmap_from_url


class CharactersWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Personajes Marvel")
        self.service = PersonajeService()

        self.todos = []
        self.filtrados = []
        self.pagina_actual = 1
        self.por_pagina = 10
        self.items_pagina = []

        self._build_ui()
        self.cargar_personajes()

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
                background-color: #2563EB;
                color: white;
                border: none;
                border-radius: 12px;
                padding: 10px 14px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #1D4ED8;
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

        titulo = QLabel("Catálogo de Personajes Marvel")
        titulo.setObjectName("title")
        subtitulo = QLabel("Búsqueda, nombre real, editorial, comics asociados e imagen.")
        subtitulo.setObjectName("muted")

        root.addWidget(titulo)
        root.addWidget(subtitulo)

        top = QHBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Escribe un personaje, por ejemplo: Spider-Man")

        self.sort_combo = QComboBox()
        self.sort_combo.addItems([
            "Nombre A-Z",
            "Nombre Z-A",
            "Editorial"
        ])

        btn_buscar_api = QPushButton("Buscar")
        btn_buscar_api.clicked.connect(self.buscar_en_api)

        btn_filtrar = QPushButton("Filtrar")
        btn_filtrar.setProperty("class", "secondary")
        btn_filtrar.clicked.connect(self.aplicar_filtros)

        top.addWidget(self.search_input, 2)
        top.addWidget(self.sort_combo, 1)
        top.addWidget(btn_buscar_api)
        top.addWidget(btn_filtrar)

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

        self.detail_title = QLabel("Selecciona un personaje")
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

    def cargar_personajes(self):
        personajes = self.service.cargar_personajes_desde_json()
        if not personajes:
            personajes = self.service.guardar_detalles_personajes_desde_api(query="Spider-Man", limit=10)

        self.todos = personajes
        self.aplicar_filtros()

    def buscar_en_api(self):
        query = self.search_input.text().strip() or "Spider-Man"

        try:
            self.todos = self.service.guardar_detalles_personajes_desde_api(query=query, limit=10)
            self.aplicar_filtros()
            QMessageBox.information(self, "Listo", f"Personajes cargados para: {query}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo buscar personajes:\n{e}")

    def aplicar_filtros(self):
        texto = self.search_input.text().strip().lower()

        filtrados = []
        for personaje in self.todos:
            nombre = personaje.nombre.lower()
            nombre_real = personaje.nombre_real.lower()
            editorial = personaje.editorial.lower()
            if not texto or texto in nombre or texto in nombre_real or texto in editorial:
                filtrados.append(personaje)

        criterio = self.sort_combo.currentText()

        if criterio == "Nombre A-Z":
            filtrados.sort(key=lambda p: p.nombre.lower())
        elif criterio == "Nombre Z-A":
            filtrados.sort(key=lambda p: p.nombre.lower(), reverse=True)
        elif criterio == "Editorial":
            filtrados.sort(key=lambda p: p.editorial.lower())

        self.filtrados = filtrados
        self.pagina_actual = 1
        self.mostrar_pagina()

    def mostrar_pagina(self):
        self.lista.clear()
        self.items_pagina = []

        total_paginas = max(1, ceil(len(self.filtrados) / self.por_pagina))

        if self.pagina_actual > total_paginas:
            self.pagina_actual = total_paginas

        self.items_pagina = self.service.paginar_personajes(
            self.filtrados,
            self.pagina_actual,
            self.por_pagina
        )

        if not self.items_pagina:
            self.lista.addItem("No hay personajes para mostrar.")
            self.limpiar_detalle()
        else:
            for personaje in self.items_pagina:
                sub = personaje.nombre_real or personaje.editorial or "Sin detalle"
                self.lista.addItem(f"{personaje.nombre}  •  {sub}")

            self.lista.setCurrentRow(0)

        self.lbl_pagina.setText(f"Página {self.pagina_actual} / {total_paginas}")
        self.btn_prev.setEnabled(self.pagina_actual > 1)
        self.btn_next.setEnabled(self.pagina_actual < total_paginas)

    def personaje_actual(self):
        row = self.lista.currentRow()
        if row < 0 or row >= len(self.items_pagina):
            return None
        return self.items_pagina[row]

    def mostrar_detalle(self):
        personaje = self.personaje_actual()
        if personaje is None:
            return

        comics = ", ".join(personaje.comics[:6]) or "Sin comics relacionados"

        self.detail_title.setText(personaje.nombre)
        self.detail_meta.setText(
            f"<b>Nombre real:</b> {personaje.nombre_real or 'No disponible'}<br>"
            f"<b>Editorial:</b> {personaje.editorial or 'No disponible'}<br>"
            f"<b>Comics:</b> {comics}"
        )
        self.detail_desc.setHtml(personaje.descripcion or personaje.descripcion_corta or "Sin descripción.")
        self.image_label.setPixmap(load_pixmap_from_url(personaje.imagen_url))

    def abrir_dialogo_detalle(self):
        personaje = self.personaje_actual()
        if personaje is None:
            return

        comics = ", ".join(personaje.comics[:10]) or "Sin comics relacionados"

        dialog = DetailDialog(
            titulo=personaje.nombre,
            subtitulo=personaje.nombre_real or "Personaje Marvel",
            imagen_url=personaje.imagen_url,
            metadata={
                "Editorial": personaje.editorial or "No disponible",
                "Nombre real": personaje.nombre_real or "No disponible",
                "Comics": comics
            },
            descripcion=personaje.descripcion or personaje.descripcion_corta or "Sin descripción.",
            parent=self
        )
        dialog.exec()

    def limpiar_detalle(self):
        self.detail_title.setText("Selecciona un personaje")
        self.detail_meta.setText("Aquí aparecerán los detalles.")
        self.detail_desc.setPlainText("Sin descripción.")
        self.image_label.setText("Sin imagen")

    def pagina_siguiente(self):
        self.pagina_actual += 1
        self.mostrar_pagina()

    def pagina_anterior(self):
        self.pagina_actual -= 1
        self.mostrar_pagina()