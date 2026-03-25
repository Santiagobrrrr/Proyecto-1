#Aquí voy a empezar con la interfaz grafica, voy a hacer clases para cada ventana

import tkinter as tk
from tkinter.ttk import Style

import requests

class Styles:
    BG_MAIN = "maroon"
    TITLE = {
        "bg": "maroon",
        "fg": "gold",
        "font": ("Impact", 48)
    }

    BOTONES = {
        "bg": "gold",
        "fg": "black",
        "font": ("Impact", 20),
        "width": 20,
        "height": 1
    }

class ComicsView(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Listado de Comics")
        self.state("zoomed")
        self.config(bg=Styles.BG_MAIN)

        self.datos = []
        self.datos_filtrados = []
        self.pagina = 0
        self.por_pagina = 10

        self.entrada = tk.Entry(self, font=("Arial", 20))
        self.entrada.pack(pady=10)

        tk.Button(self, text="Buscar", **Styles.BOTONES, command=self.buscar).pack()

        frame_orden = tk.Frame(self)
        frame_orden.pack(pady=5)

        tk.Button(frame_orden, text="Ordenar por Nombre", **Styles.BOTONES, command=self.ordenar_nombre).pack(side="left", padx=5)
        tk.Button(frame_orden, text="Ordenar por Año", **Styles.BOTONES, command=self.ordenar_anio).pack(side="left", padx=5)

        frame_lista = tk.Frame(self)
        frame_lista.pack(pady=10)

        scrollbar = tk.Scrollbar(frame_lista)
        scrollbar.pack(side="right", fill="y")

        self.lista = tk.Listbox(frame_lista, width=100, height=20, yscrollcommand=scrollbar.set)
        self.lista.pack(side="left")

        scrollbar.config(command=self.lista.yview)

        self.lista.bind("<<ListboxSelect>>", self.mostrar_detalle)

        self.detalle = tk.Label(self, text="", justify="left", wraplength=800)
        self.detalle.pack(pady=10)

        frame_nav = tk.Frame(self)
        frame_nav.pack(pady=10)

        tk.Button(frame_nav, text="Anterior", **Styles.BOTONES, command=self.anterior).pack(side="left", padx=10)
        tk.Button(frame_nav, text="Siguiente", **Styles.BOTONES, command=self.siguiente).pack(side="left", padx=10)

        self.label_pagina = tk.Label(frame_nav, text="Página 1")
        self.label_pagina.pack(side="left", padx=10)

    def buscar(self):
        query = self.entrada.get().strip()
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
        self.lista.delete(0, tk.END)

        inicio = self.pagina * self.por_pagina
        fin = inicio + self.por_pagina
        subset = self.datos_filtrados[inicio:fin]

        if not subset:
            self.lista.insert(tk.END, "No hay resultados")
            return

        for comic in subset:
            titulo = comic.get("title", "")
            anio = comic.get("yearPage", "")
            self.lista.insert(tk.END, f"{titulo} ({anio})")

        self.label_pagina.config(text=f"Página {self.pagina + 1}")

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

    def mostrar_detalle(self, event):
        seleccion = self.lista.curselection()
        if not seleccion:
            return

        index = seleccion[0] + (self.pagina * self.por_pagina)
        if index >= len(self.datos_filtrados):
            return

        comic = self.datos_filtrados[index]

        info = f"""
Título: {comic.get('title')}
Serie: {comic.get('seriesName')}
Número: {comic.get('issueNumber')}
Año: {comic.get('yearPage')}
"""
        self.detalle.config(text=info)

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.state("zoomed")
        self.title('Mundo Comic')
        self.config(bg=Styles.BG_MAIN)

        self.label = tk.Label(self, text='Mundo Comic', **Styles.TITLE)
        self.label.pack(pady=20)

        self.boton = tk.Button(
            self,
            text="Comics Disponibles",
            command=lambda: ComicsView(self),
            **Styles.BOTONES
        )
        self.boton.pack(pady=10)

        self.boton2 = tk.Button(
            self,
            text="Comics de Personajes",
            command=self.abrir_comics_personajes,
            **Styles.BOTONES
        )
        self.boton2.pack(pady=10)

    def abrir_comics_personajes(self):
        ventana = tk.Toplevel(self)
        ventana.title("Comics de Personajes")
        ventana.state("zoomed")
        ventana.config(bg=Styles.BG_MAIN)

        label = tk.Label(ventana, text="Aquí van los comics por personaje", **Styles.TITLE)
        label.pack(pady=20)

App().mainloop()