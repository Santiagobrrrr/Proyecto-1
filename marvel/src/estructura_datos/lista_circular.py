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

    def reset(self):
        self.actual = self.cabeza

    def avanzar_n(self, n):
        if self.esta_vacia():
            return None

        for _ in range(n):
            self.actual = self.actual.siguiente

        return self.actual.dato