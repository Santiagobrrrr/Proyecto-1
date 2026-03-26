class NodoCircular:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None

class ListaCircular:
    def __init__(self):
        self.cabeza = None
        self.actual = None
        self.tamanio = 0

    def esta_vacia(self):
        return self.cabeza is None

    def __len__(self):
        return self.tamanio

    def append(self, dato):
        nuevo = NodoCircular(dato)

        if self.esta_vacia():
            self.cabeza = nuevo
            nuevo.siguiente = nuevo
            self.actual = self.cabeza
        else:
            ultimo = self.cabeza
            while ultimo.siguiente != self.cabeza:
                ultimo = ultimo.siguiente

            ultimo.siguiente = nuevo
            nuevo.siguiente = self.cabeza

        self.tamanio += 1

    def current(self):
        if self.esta_vacia():
            return None
        return self.actual.dato

    def next(self):
        if self.esta_vacia():
            return None

        self.actual = self.actual.siguiente
        return self.actual.dato

    def to_list(self, limite=None):
        resultado = []

        if self.esta_vacia():
            return resultado

        actual = self.cabeza
        contador = 0

        while True:
            resultado.append(actual.dato)
            actual = actual.siguiente
            contador += 1

            if actual == self.cabeza:
                break

            if limite is not None and contador >= limite:
                break

        return resultado