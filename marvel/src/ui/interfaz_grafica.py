from math import ceil

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QLineEdit, QComboBox, QScrollArea, QGridLayout, QTextBrowser,
    QMessageBox, QStackedWidget
)

from src.servicios.comic_s import ComicService
from src.servicios.personaje_s import PersonajeService
from src.ui.interfaz import ComicCard, CharacterCard, clear_layout, load_pixmap_from_url


class ComicsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.service = ComicService()
        self.todos = []
        self.filtrados = []
        self.pagina_actual = 1
        self.por_pagina = 8
        self.items_pagina = []

        self._build_ui()
        self.cargar_datos()

    def _build_ui(self):
        root = QHBoxLayout(self)
        root.setContentsMargins(20, 20, 20, 20)
        root.setSpacing(18)

        # Columna izquierda
        left = QVBoxLayout()

        header = QLabel("LISTADO DE CÓMICS")
        header.setObjectName("sectionTitle")

        sub = QLabel("Búsqueda, ordenamiento, paginación e imágenes estilo catálogo.")
        sub.setObjectName("sectionSubtitle")

        controls = QHBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar cómic por nombre o año...")

        self.sort_combo = QComboBox()
        self.sort_combo.addItems([
            "Nombre A-Z",
            "Nombre Z-A",
            "Fecha reciente",
            "Fecha antigua"
        ])

        btn_filtrar = QPushButton("Aplicar")
        btn_filtrar.clicked.connect(self.aplicar_filtros)

        btn_buscar = QPushButton("Buscar")
        btn_buscar.setObjectName("secondaryButton")
        btn_buscar.clicked.connect(self.buscar_en_api)

        controls.addWidget(self.search_input, 2)
        controls.addWidget(self.sort_combo, 1)
        controls.addWidget(btn_filtrar)
        controls.addWidget(btn_buscar)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setObjectName("cardsScroll")

        self.cards_container = QWidget()
        self.cards_layout = QGridLayout(self.cards_container)
        self.cards_layout.setSpacing(14)
        self.scroll.setWidget(self.cards_container)

        nav = QHBoxLayout()
        self.btn_prev = QPushButton("← Anterior")
        self.btn_prev.setObjectName("secondaryButton")
        self.btn_prev.clicked.connect(self.pagina_anterior)

        self.lbl_pagina = QLabel("Página 1 / 1")
        self.lbl_pagina.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.btn_next = QPushButton("Siguiente →")
        self.btn_next.setObjectName("secondaryButton")
        self.btn_next.clicked.connect(self.pagina_siguiente)

        nav.addWidget(self.btn_prev)
        nav.addWidget(self.lbl_pagina, 1)
        nav.addWidget(self.btn_next)

        left.addWidget(header)
        left.addWidget(sub)
        left.addLayout(controls)
        left.addWidget(self.scroll, 1)
        left.addLayout(nav)

        # Columna derecha
        right_card = QFrame()
        right_card.setObjectName("detailCard")
        right = QVBoxLayout(right_card)

        self.detail_image = QLabel("Sin imagen")
        self.detail_image.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.detail_title = QLabel("Selecciona un cómic")
        self.detail_title.setObjectName("detailTitle")

        self.detail_meta = QLabel("Aquí aparecerán los detalles.")
        self.detail_meta.setWordWrap(True)
        self.detail_meta.setObjectName("detailMeta")

        self.detail_desc = QTextBrowser()
        self.detail_desc.setObjectName("detailText")
        self.detail_desc.setPlainText("Sin descripción.")

        right.addWidget(self.detail_image)
        right.addWidget(self.detail_title)
        right.addWidget(self.detail_meta)
        right.addWidget(self.detail_desc, 1)

        root.addLayout(left, 3)
        root.addWidget(right_card, 2)

    def cargar_datos(self):
        comics = self.service.cargar_comics_desde_json()
        if not comics:
            comics = self.service.guardar_comics_desde_api(limit=20)

        self.todos = comics
        self.aplicar_filtros()

    def actualizar_desde_api(self):
        query = self.search_input.text().strip()

        if not query:
            QMessageBox.warning(self, "Aviso", "Escribe el nombre de un cómic.")
            return

        try:
            self.todos = self.service.buscar_comics_api(query)
            self.aplicar_filtros()

            if not self.todos:
                QMessageBox.information(self, "Sin resultados", f"No se encontraron cómics para: {query}")
            else:
                QMessageBox.information(self, "Listo", "Cómics actualizados desde la API.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo actualizar:\n{e}")

    def buscar_en_api(self):
        query = self.search_input.text().strip()

        if not query:
            QMessageBox.warning(self, "Aviso", "Escribe el nombre de un cómic.")
            return

        try:
            self.todos = self.service.buscar_comics_api(query, limit=20)
            self.pagina_actual = 1
            self.aplicar_filtros()

            if not self.todos:
                QMessageBox.information(self, "Sin resultados", f"No se encontraron cómics para: {query}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo buscar:\n{e}")

    def aplicar_filtros(self):
        texto = self.search_input.text().strip().lower()
        filtrados = []

        for comic in self.todos:
            if (
                not texto
                or texto in comic.nombre.lower()
                or texto in (comic.fecha_publicacion or "").lower()
                or texto in (comic.volumen or "").lower()
            ):
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
        clear_layout(self.cards_layout)

        total_paginas = max(1, ceil(len(self.filtrados) / self.por_pagina))
        if self.pagina_actual > total_paginas:
            self.pagina_actual = total_paginas

        self.items_pagina = self.service.paginar_comics(
            self.filtrados, self.pagina_actual, self.por_pagina
        )

        if not self.items_pagina:
            self.detail_title.setText("No hay cómics")
            self.detail_meta.setText("Sin resultados.")
            self.detail_desc.setPlainText("Prueba con otro filtro.")
        else:
            fila = 0
            columna = 0
            for comic in self.items_pagina:
                card = ComicCard(comic, self.mostrar_detalle)
                self.cards_layout.addWidget(card, fila, columna)

                columna += 1
                if columna == 3:
                    columna = 0
                    fila += 1

            self.mostrar_detalle(self.items_pagina[0])

        self.lbl_pagina.setText(f"Página {self.pagina_actual} / {total_paginas}")
        self.btn_prev.setEnabled(self.pagina_actual > 1)
        self.btn_next.setEnabled(self.pagina_actual < total_paginas)

    def mostrar_detalle(self, comic):
        creadores = ", ".join([c.nombre for c in comic.creadores[:4]]) or "Sin creadores"

        self.detail_image.setPixmap(load_pixmap_from_url(comic.imagen_url, 260, 340))
        self.detail_title.setText(comic.nombre)
        self.detail_meta.setText(
            f"<b>Editorial:</b> {comic.editorial or 'No disponible'}<br>"
            f"<b>Volumen:</b> {comic.volumen or 'No disponible'}<br>"
            f"<b>Fecha:</b> {comic.fecha_publicacion or 'No disponible'}<br>"
            f"<b>Creadores:</b> {creadores}"
        )
        self.detail_desc.setHtml(comic.descripcion or comic.descripcion_corta or "Sin descripción disponible.")

    def pagina_siguiente(self):
        self.pagina_actual += 1
        self.mostrar_pagina()

    def pagina_anterior(self):
        self.pagina_actual -= 1
        self.mostrar_pagina()


class PersonajesPage(QWidget):
    def __init__(self):
        super().__init__()
        self.service = PersonajeService()
        self.todos = []
        self.filtrados = []
        self.pagina_actual = 1
        self.por_pagina = 8
        self.items_pagina = []
        self.filtro_rapido = "todos"

        self._build_ui()
        self.cargar_datos()

    def _build_ui(self):
        root = QHBoxLayout(self)
        root.setContentsMargins(20, 20, 20, 20)
        root.setSpacing(18)

        left = QVBoxLayout()

        header = QLabel("LISTADO DE PERSONAJES")
        header.setObjectName("sectionTitle")

        sub = QLabel("Incluye búsqueda y filtros rápidos por clic, aparte del buscador.")
        sub.setObjectName("sectionSubtitle")

        controls = QHBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar personaje...")

        self.sort_combo = QComboBox()
        self.sort_combo.addItems([
            "Nombre A-Z",
            "Nombre Z-A",
            "Editorial"
        ])

        btn_buscar_api = QPushButton("Buscar")
        btn_buscar_api.clicked.connect(self.buscar_en_api)

        btn_filtrar = QPushButton("Aplicar")
        btn_filtrar.setObjectName("secondaryButton")
        btn_filtrar.clicked.connect(self.aplicar_filtros)

        controls.addWidget(self.search_input, 2)
        controls.addWidget(self.sort_combo, 1)
        controls.addWidget(btn_buscar_api)
        controls.addWidget(btn_filtrar)

        quick_filters = QHBoxLayout()

        self.btn_todos = QPushButton("Todos")
        self.btn_con_real = QPushButton("Con nombre real")
        self.btn_sin_real = QPushButton("Sin nombre real")
        self.btn_con_comics = QPushButton("Con comics")
        self.btn_sin_comics = QPushButton("Sin comics")

        self.btn_todos.setObjectName("chipButton")
        self.btn_con_real.setObjectName("chipButton")
        self.btn_sin_real.setObjectName("chipButton")
        self.btn_con_comics.setObjectName("chipButton")
        self.btn_sin_comics.setObjectName("chipButton")

        self.btn_todos.clicked.connect(lambda: self.set_filtro_rapido("todos"))
        self.btn_con_real.clicked.connect(lambda: self.set_filtro_rapido("con_real"))
        self.btn_sin_real.clicked.connect(lambda: self.set_filtro_rapido("sin_real"))
        self.btn_con_comics.clicked.connect(lambda: self.set_filtro_rapido("con_comics"))
        self.btn_sin_comics.clicked.connect(lambda: self.set_filtro_rapido("sin_comics"))

        quick_filters.addWidget(self.btn_todos)
        quick_filters.addWidget(self.btn_con_real)
        quick_filters.addWidget(self.btn_sin_real)
        quick_filters.addWidget(self.btn_con_comics)
        quick_filters.addWidget(self.btn_sin_comics)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setObjectName("cardsScroll")

        self.cards_container = QWidget()
        self.cards_layout = QGridLayout(self.cards_container)
        self.cards_layout.setSpacing(14)
        self.scroll.setWidget(self.cards_container)

        nav = QHBoxLayout()
        self.btn_prev = QPushButton("← Anterior")
        self.btn_prev.setObjectName("secondaryButton")
        self.btn_prev.clicked.connect(self.pagina_anterior)

        self.lbl_pagina = QLabel("Página 1 / 1")
        self.lbl_pagina.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.btn_next = QPushButton("Siguiente →")
        self.btn_next.setObjectName("secondaryButton")
        self.btn_next.clicked.connect(self.pagina_siguiente)

        nav.addWidget(self.btn_prev)
        nav.addWidget(self.lbl_pagina, 1)
        nav.addWidget(self.btn_next)

        left.addWidget(header)
        left.addWidget(sub)
        left.addLayout(controls)
        left.addLayout(quick_filters)
        left.addWidget(self.scroll, 1)
        left.addLayout(nav)

        right_card = QFrame()
        right_card.setObjectName("detailCard")
        right = QVBoxLayout(right_card)

        self.detail_image = QLabel("Sin imagen")
        self.detail_image.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.detail_title = QLabel("Selecciona un personaje")
        self.detail_title.setObjectName("detailTitle")

        self.detail_meta = QLabel("Aquí aparecerán los detalles.")
        self.detail_meta.setWordWrap(True)
        self.detail_meta.setObjectName("detailMeta")

        self.detail_desc = QTextBrowser()
        self.detail_desc.setObjectName("detailText")
        self.detail_desc.setPlainText("Sin descripción.")

        right.addWidget(self.detail_image)
        right.addWidget(self.detail_title)
        right.addWidget(self.detail_meta)
        right.addWidget(self.detail_desc, 1)

        root.addLayout(left, 3)
        root.addWidget(right_card, 2)

    def cargar_datos(self):
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
            QMessageBox.critical(self, "Error", f"No se pudo buscar:\n{e}")

    def set_filtro_rapido(self, filtro):
        self.filtro_rapido = filtro
        self.aplicar_filtros()

    def aplicar_filtros(self):
        texto = self.search_input.text().strip().lower()
        filtrados = []

        for personaje in self.todos:
            if texto and not (
                texto in personaje.nombre.lower()
                or texto in (personaje.nombre_real or "").lower()
                or texto in (personaje.editorial or "").lower()
            ):
                continue

            if self.filtro_rapido == "con_real" and not personaje.nombre_real:
                continue
            if self.filtro_rapido == "sin_real" and personaje.nombre_real:
                continue
            if self.filtro_rapido == "con_comics" and not personaje.comics:
                continue
            if self.filtro_rapido == "sin_comics" and personaje.comics:
                continue

            filtrados.append(personaje)

        criterio = self.sort_combo.currentText()

        if criterio == "Nombre A-Z":
            filtrados.sort(key=lambda p: p.nombre.lower())
        elif criterio == "Nombre Z-A":
            filtrados.sort(key=lambda p: p.nombre.lower(), reverse=True)
        elif criterio == "Editorial":
            filtrados.sort(key=lambda p: (p.editorial or "").lower())

        self.filtrados = filtrados
        self.pagina_actual = 1
        self.mostrar_pagina()

    def mostrar_pagina(self):
        clear_layout(self.cards_layout)

        total_paginas = max(1, ceil(len(self.filtrados) / self.por_pagina))
        if self.pagina_actual > total_paginas:
            self.pagina_actual = total_paginas

        self.items_pagina = self.service.paginar_personajes(
            self.filtrados, self.pagina_actual, self.por_pagina
        )

        if not self.items_pagina:
            self.detail_title.setText("No hay personajes")
            self.detail_meta.setText("Sin resultados.")
            self.detail_desc.setPlainText("Prueba con otro filtro.")
        else:
            fila = 0
            columna = 0
            for personaje in self.items_pagina:
                card = CharacterCard(personaje, self.mostrar_detalle)
                self.cards_layout.addWidget(card, fila, columna)

                columna += 1
                if columna == 3:
                    columna = 0
                    fila += 1

            self.mostrar_detalle(self.items_pagina[0])

        self.lbl_pagina.setText(f"Página {self.pagina_actual} / {total_paginas}")
        self.btn_prev.setEnabled(self.pagina_actual > 1)
        self.btn_next.setEnabled(self.pagina_actual < total_paginas)

    def mostrar_detalle(self, personaje):
        comics = ", ".join(personaje.comics[:6]) if personaje.comics else "Sin comics relacionados"

        self.detail_image.setPixmap(load_pixmap_from_url(personaje.imagen_url, 260, 340))
        self.detail_title.setText(personaje.nombre)
        self.detail_meta.setText(
            f"<b>Nombre real:</b> {personaje.nombre_real or 'No disponible'}<br>"
            f"<b>Editorial:</b> {personaje.editorial or 'No disponible'}<br>"
            f"<b>Comics:</b> {comics}"
        )
        self.detail_desc.setHtml(personaje.descripcion or personaje.descripcion_corta or "Sin descripción disponible.")

    def pagina_siguiente(self):
        self.pagina_actual += 1
        self.mostrar_pagina()

    def pagina_anterior(self):
        self.pagina_actual -= 1
        self.mostrar_pagina()


class DashboardPage(QWidget):
    def __init__(self, open_comics, open_personajes):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(18)

        hero = QLabel("SUPERHERO CATALOG SYSTEM")
        hero.setObjectName("heroTitle")
        hero.setAlignment(Qt.AlignmentFlag.AlignCenter)

        sub = QLabel(" ")
        sub.setObjectName("heroSubtitle")
        sub.setAlignment(Qt.AlignmentFlag.AlignCenter)

        actions = QHBoxLayout()

        left = QFrame()
        left.setObjectName("heroCard")
        left_layout = QVBoxLayout(left)

        left_title = QLabel("Personajes")
        left_title.setObjectName("heroCardTitle")

        left_desc = QLabel("Búsqueda por texto + filtros por clic.")
        left_desc.setWordWrap(True)

        btn_personajes = QPushButton("Entrar a personajes")
        btn_personajes.clicked.connect(open_personajes)

        left_layout.addWidget(left_title)
        left_layout.addWidget(left_desc)
        left_layout.addStretch()
        left_layout.addWidget(btn_personajes)

        right = QFrame()
        right.setObjectName("heroCard")
        right_layout = QVBoxLayout(right)

        right_title = QLabel("Cómics")
        right_title.setObjectName("heroCardTitle")

        right_desc = QLabel("Catálogo visual con ordenamiento, paginación y detalle.")
        right_desc.setWordWrap(True)

        btn_comics = QPushButton("Entrar a cómics")
        btn_comics.clicked.connect(open_comics)

        right_layout.addWidget(right_title)
        right_layout.addWidget(right_desc)
        right_layout.addStretch()
        right_layout.addWidget(btn_comics)

        actions.addWidget(left)
        actions.addWidget(right)

        layout.addStretch()
        layout.addWidget(hero)
        layout.addWidget(sub)
        layout.addLayout(actions)
        layout.addStretch()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Superhero Catalog System")
        self.resize(1400, 860)

        self.setStyleSheet("""
            QMainWindow, QWidget {
                background-color: #101217;
                color: #F8FAFC;
                font-family: Segoe UI;
            }

            QLabel#heroTitle {
                font-size: 38px;
                font-weight: 900;
                color: #FFFFFF;
                letter-spacing: 1px;
            }

            QLabel#heroSubtitle {
                color: #FDE047;
                font-size: 14px;
                font-weight: 600;
            }

            QLabel#sectionTitle {
                font-size: 26px;
                font-weight: 800;
                color: #FFFFFF;
                background-color: #0F0F10;
                border-left: 8px solid #FACC15;
                padding: 8px 12px;
            }

            QLabel#sectionSubtitle {
                color: #CBD5E1;
                font-size: 13px;
            }

            QLabel#detailTitle {
                font-size: 22px;
                font-weight: 800;
                color: #FFFFFF;
            }

            QLabel#detailMeta {
                color: #E5E7EB;
                font-size: 13px;
            }

            QLabel#cardTitle {
                font-size: 14px;
                font-weight: 800;
                color: #FFFFFF;
            }

            QLabel#cardMeta {
                font-size: 12px;
                color: #FDE68A;
            }

            QFrame#card {
                background-color: #1A1D24;
                border: 3px solid #2A2F3A;
                border-radius: 16px;
            }

            QFrame#detailCard {
                background-color: #111827;
                border: 2px solid #FACC15;
                border-radius: 18px;
                padding: 14px;
            }

            QFrame#heroCard {
                background-color: #151922;
                border: 2px solid #FACC15;
                border-radius: 22px;
                padding: 18px;
            }

            QLabel#heroCardTitle {
                font-size: 24px;
                font-weight: 800;
                color: #FDE047;
            }

            QLineEdit, QComboBox, QTextBrowser {
                background-color: #1E293B;
                color: #F8FAFC;
                border: 2px solid #334155;
                border-radius: 14px;
                padding: 10px 12px;
                font-size: 13px;
            }

            QScrollArea#cardsScroll {
                border: none;
                background: transparent;
            }

            QPushButton {
                background-color: #EAB308;
                color: #111827;
                border: none;
                border-radius: 12px;
                padding: 10px 14px;
                font-weight: 800;
            }

            QPushButton:hover {
                background-color: #FACC15;
            }

            QPushButton#secondaryButton {
                background-color: #DC2626;
                color: white;
            }

            QPushButton#secondaryButton:hover {
                background-color: #B91C1C;
            }

            QPushButton#menuButton {
                background-color: transparent;
                color: #F8FAFC;
                text-align: left;
                border-radius: 10px;
                padding: 12px 14px;
                font-size: 14px;
                font-weight: 700;
            }

            QPushButton#menuButton:hover {
                background-color: #1F2937;
            }

            QPushButton#chipButton {
                background-color: #1F2937;
                color: #F8FAFC;
                border: 1px solid #475569;
                border-radius: 18px;
                padding: 8px 12px;
                font-size: 12px;
                font-weight: 700;
            }

            QPushButton#chipButton:hover {
                background-color: #334155;
            }
        """)

        central = QWidget()
        self.setCentralWidget(central)

        root = QHBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        sidebar = QFrame()
        sidebar.setFixedWidth(220)
        sidebar.setStyleSheet("background-color: #0B0E13; border-right: 2px solid #FACC15;")
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(14, 20, 14, 20)
        sidebar_layout.setSpacing(10)

        logo = QLabel("⚡ MARVEL HUB")
        logo.setStyleSheet("font-size: 20px; font-weight: 900; color: #FACC15;")
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        btn_inicio = QPushButton("🏠  Inicio")
        btn_inicio.setObjectName("menuButton")
        btn_inicio.clicked.connect(lambda: self.stack.setCurrentWidget(self.dashboard))

        btn_comics = QPushButton("📚  Cómics")
        btn_comics.setObjectName("menuButton")
        btn_comics.clicked.connect(lambda: self.stack.setCurrentWidget(self.comics_page))

        btn_personajes = QPushButton("🦸  Personajes")
        btn_personajes.setObjectName("menuButton")
        btn_personajes.clicked.connect(lambda: self.stack.setCurrentWidget(self.personajes_page))

        sidebar_layout.addWidget(logo)
        sidebar_layout.addSpacing(20)
        sidebar_layout.addWidget(btn_inicio)
        sidebar_layout.addWidget(btn_comics)
        sidebar_layout.addWidget(btn_personajes)
        sidebar_layout.addStretch()

        self.stack = QStackedWidget()

        self.comics_page = ComicsPage()
        self.personajes_page = PersonajesPage()
        self.dashboard = DashboardPage(
            open_comics=lambda: self.stack.setCurrentWidget(self.comics_page),
            open_personajes=lambda: self.stack.setCurrentWidget(self.personajes_page)
        )

        self.stack.addWidget(self.dashboard)
        self.stack.addWidget(self.comics_page)
        self.stack.addWidget(self.personajes_page)

        root.addWidget(sidebar)
        root.addWidget(self.stack, 1)