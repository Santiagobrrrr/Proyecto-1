from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QFrame
)

from src.ui.comics_window import ComicsWindow
from src.ui.characters_window import CharactersWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TIENDA MARVEL")
        self.comics_window = None
        self.characters_window = None

        self.setStyleSheet("""
            QMainWindow, QWidget {
                background-color: #020617;
                color: #F8FAFC;
                font-family: Segoe UI;
            }
            QFrame.card {
                background-color: #111827;
                border: 1px solid #334155;
                border-radius: 22px;
                padding: 22px;
            }
            QLabel#hero {
                font-size: 34px;
                font-weight: 800;
                color: #F8FAFC;
            }
            QLabel#subhero {
                font-size: 15px;
                color: #94A3B8;
            }
            QLabel.section {
                font-size: 20px;
                font-weight: 700;
            }
            QLabel.desc {
                color: #CBD5E1;
                font-size: 13px;
            }
            QPushButton {
                background-color: #DC2626;
                color: white;
                border: none;
                border-radius: 14px;
                padding: 12px 16px;
                font-weight: 700;
            }
            QPushButton.secondary {
                background-color: #2563EB;
            }
            QPushButton:hover {
                opacity: 0.9;
            }
        """)

        central = QWidget()
        self.setCentralWidget(central)

        root = QVBoxLayout(central)
        root.setContentsMargins(40, 40, 40, 40)
        root.setSpacing(24)

        hero = QLabel("TIENDA MARVEL")
        hero.setObjectName("hero")

        subhero = QLabel(
            "MUNDO MARVEL"
            " Comics y Personajes"
        )
        subhero.setObjectName("subhero")
        subhero.setWordWrap(True)

        root.addWidget(hero)
        root.addWidget(subhero)

        cards = QHBoxLayout()

        comic_card = QFrame()
        comic_card.setProperty("class", "card")
        comic_layout = QVBoxLayout(comic_card)

        comic_title = QLabel("Comics")
        comic_title.setProperty("class", "section")

        comic_desc = QLabel(
            "Lista paginada, búsqueda por nombre o año, ordenamiento, imagen y detalle completo."
        )
        comic_desc.setProperty("class", "desc")
        comic_desc.setWordWrap(True)

        comic_btn = QPushButton("Abrir catálogo de comics")
        comic_btn.clicked.connect(self.abrir_comics)

        comic_layout.addWidget(comic_title)
        comic_layout.addWidget(comic_desc)
        comic_layout.addStretch()
        comic_layout.addWidget(comic_btn)

        char_card = QFrame()
        char_card.setProperty("class", "card")
        char_layout = QVBoxLayout(char_card)

        char_title = QLabel("Personajes")
        char_title.setProperty("class", "section")

        char_desc = QLabel(
            "Búsqueda, nombre real, editorial, comics relacionados, imagen y vista detallada."
        )
        char_desc.setProperty("class", "desc")
        char_desc.setWordWrap(True)

        char_btn = QPushButton("Abrir catálogo de personajes")
        char_btn.setProperty("class", "secondary")
        char_btn.clicked.connect(self.abrir_personajes)

        char_layout.addWidget(char_title)
        char_layout.addWidget(char_desc)
        char_layout.addStretch()
        char_layout.addWidget(char_btn)

        cards.addWidget(comic_card)
        cards.addWidget(char_card)

        footer = QLabel("Proyecto de estructuras de datos")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer.setObjectName("subhero")

        root.addLayout(cards)
        root.addStretch()
        root.addWidget(footer)

    def abrir_comics(self):
        if self.comics_window is None:
            self.comics_window = ComicsWindow()
        self.comics_window.showMaximized()
        self.comics_window.raise_()

    def abrir_personajes(self):
        if self.characters_window is None:
            self.characters_window = CharactersWindow()
        self.characters_window.showMaximized()
        self.characters_window.raise_()