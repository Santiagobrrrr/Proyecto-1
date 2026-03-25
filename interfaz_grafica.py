#Aquí voy a empezar con la interfaz grafica, voy a hacer clases para cada ventana

import tkinter as tk

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

class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.state("zoomed")
        self.title('Ventana Principal')
        self.config(bg=Styles.BG_MAIN)

        self.label = tk.Label(self, text='Mundo Comic', **Styles.TITLE)
        self.label.pack(pady=20)

        self.boton = tk.Button(
            self,
            text="Comics Disponibles",
            command=self.abrir_comics_disponibles,
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

    def abrir_comics_disponibles(self):
        ventana = tk.Toplevel(self)
        ventana.title("Comics Disponibles")
        ventana.state("zoomed")
        ventana.config(bg=Styles.BG_MAIN)

        label = tk.Label(ventana, text="Aquí van los comics disponibles", **Styles.TITLE)
        label.pack(pady=20)

    def abrir_comics_personajes(self):
        ventana = tk.Toplevel(self)
        ventana.title("Comics de Personajes")
        ventana.state("zoomed")
        ventana.config(bg=Styles.BG_MAIN)

        label = tk.Label(ventana, text="Aquí van los comics por personaje", **Styles.TITLE)
        label.pack(pady=20)

App().mainloop()