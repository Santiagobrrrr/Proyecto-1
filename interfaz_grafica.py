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
        "font": ("Impact", 48),
        "width": 20,
        "height": 1
    }

class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.geometry('600x600')
        self.title('Ventana Principal')
        self.config(bg = Styles.BG_MAIN)
        self.label = tk.Label(self, text = 'Mundo Comic', **Styles.TITLE)
        self.label.pack()
        self.boton = tk.Button(self, text = "Comics Disponibles", **Styles.BOTONES)
        self.boton.pack(pady=10)
        self.boton2 = tk.Button(self, text = "Comics de Personajes", **Styles.BOTONES)
        self.boton2.pack(pady=10)


App().mainloop()