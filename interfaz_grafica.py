#Aquí voy a empezar con la interfaz grafica, voy a hacer clases para cada ventana

import sys
import requests
from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout,
    QListWidget, QLabel, QLineEdit, QMainWindow
)
from PyQt6.QtCore import Qt

class ComicsView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Listado de Comics")
        self.showMaximized()

        self.datos = []
        self.datos_filtrados = []
        self.pagina = 0
        self.por_pagina = 10

        layout = QVBoxLayout()

        self.entrada = QLineEdit()
        self.entrada.setPlaceholderText("Buscar...")
        layout.addWidget(self.entrada)

        btn_buscar = QPushButton("Buscar")
        btn_buscar.clicked.connect(self.buscar)
        layout.addWidget(btn_buscar)

        layout_orden = QHBoxLayout()

        btn_nombre = QPushButton("Ordenar por Nombre")
        btn_nombre.clicked.connect(self.ordenar_nombre)

        btn_anio = QPushButton("Ordenar por Año")
        btn_anio.clicked.connect(self.ordenar_anio)

        layout_orden.addWidget(btn_nombre)
        layout_orden.addWidget(btn_anio)

        layout.addLayout(layout_orden)

        self.lista = QListWidget()
        self.lista.itemSelectionChanged.connect(self.mostrar_detalle)
        layout.addWidget(self.lista)

        self.detalle = QLabel("")
        self.detalle.setWordWrap(True)
        layout.addWidget(self.detalle)

        layout_nav = QHBoxLayout()

        btn_ant = QPushButton("Anterior")
        btn_ant.clicked.connect(self.anterior)

        btn_sig = QPushButton("Siguiente")
        btn_sig.clicked.connect(self.siguiente)

        self.label_pagina = QLabel("Página 1")

        layout_nav.addWidget(btn_ant)
        layout_nav.addWidget(btn_sig)
        layout_nav.addWidget(self.label_pagina)

        layout.addLayout(layout_nav)

        self.setLayout(layout)

    def buscar(self):
        query = self.entrada.text().strip()
        if not query:
            return

        url = f"https://marvel.emreparker.com/v1/search/issues?q={query}"

        try:
            response = requests.get(url)
            data = response.json()

            self.datos = data.get("items", [])
            self.datos_filtrados = self.datos.copy()
            self.pagina = 0

            self.mostrar_pagina()

        except Exception as e:
            print("Error:", e)

    def mostrar_pagina(self):
        self.lista.clear()

        inicio = self.pagina * self.por_pagina
        fin = inicio + self.por_pagina
        subset = self.datos_filtrados[inicio:fin]

        if not subset:
            self.lista.addItem("No hay resultados")
            return

        for comic in subset:
            titulo = comic.get("title", "")
            anio = comic.get("yearPage", "")
            self.lista.addItem(f"{titulo} ({anio})")

        self.label_pagina.setText(f"Página {self.pagina + 1}")

    def siguiente(self):
        if (self.pagina + 1) * self.por_pagina < len(self.datos_filtrados):
            self.pagina += 1
            self.mostrar_pagina()

    def anterior(self):
        if self.pagina > 0:
            self.pagina -= 1
            self.mostrar_pagina()

    def ordenar_nombre(self):
        self.datos_filtrados.sort(key=lambda x: x.get("title", ""))
        self.pagina = 0
        self.mostrar_pagina()

    def ordenar_anio(self):
        self.datos_filtrados.sort(key=lambda x: x.get("yearPage", 0))
        self.pagina = 0
        self.mostrar_pagina()

    def mostrar_detalle(self):
        seleccion = self.lista.currentRow()
        index = seleccion + (self.pagina * self.por_pagina)

        if index >= len(self.datos_filtrados) or seleccion < 0:
            return

        comic = self.datos_filtrados[index]

        info = f"""
Título: {comic.get('title')}
Serie: {comic.get('seriesName')}
Número: {comic.get('issueNumber')}
Año: {comic.get('yearPage')}
"""
        self.detalle.setText(info)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mundo Comic")

        central = QWidget()
        layout = QVBoxLayout()

        titulo = QLabel("Mundo Comic")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo.setStyleSheet("font-size: 40px; color: gold;")
        layout.addWidget(titulo)

        btn1 = QPushButton("Comics Disponibles")
        btn1.clicked.connect(self.abrir_comics)
        btn1.setFixedSize(300,50)
        layout.addWidget(btn1)

        btn2 = QPushButton("Comics de Personajes")
        btn2.clicked.connect(self.abrir_personajes)
        btn2.setFixedSize(300, 50)
        layout.addWidget(btn2)

        central.setLayout(layout)
        self.setCentralWidget(central)

    def abrir_comics(self):
        self.ventana = ComicsView()
        self.ventana.show()

    def abrir_personajes(self):
        ventana = QWidget()
        ventana.setWindowTitle("Comics de Personajes")
        ventana.showMaximized()

        layout = QVBoxLayout()
        label = QLabel("Aquí van los comics por personaje")
        layout.addWidget(label)

        ventana.setLayout(layout)
        self.ventana2 = ventana


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    window.showMaximized()
    sys.exit(app.exec())