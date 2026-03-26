class NodoDoble:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None
        self.anterior = None


class ListaDoble:
    def __init__(self):
        self.cabeza = None
        self.cola = None
        self.actual = None
        self.tamanio = 0

    def esta_vacia(self):
        return self.cabeza is None

    def __len__(self):
        return self.tamanio

    def append(self, dato):
        nuevo = NodoDoble(dato)

        if self.esta_vacia():
            self.cabeza = nuevo
            self.cola = nuevo
            self.actual = nuevo
        else:
            nuevo.anterior = self.cola
            self.cola.siguiente = nuevo
            self.cola = nuevo

        self.tamanio += 1

    def agregar_y_mover_actual(self, dato):
        self.append(dato)
        self.actual = self.cola

    def actual_dato(self):
        if self.actual is None:
            return None
        return self.actual.dato

    def mover_anterior(self):
        if self.actual is not None and self.actual.anterior is not None:
            self.actual = self.actual.anterior
            return self.actual.dato
        return None

    def mover_siguiente(self):
        if self.actual is not None and self.actual.siguiente is not None:
            self.actual = self.actual.siguiente
            return self.actual.dato
        return None

    def recorrer_adelante(self):
        resultado = []
        actual = self.cabeza

        while actual is not None:
            resultado.append(actual.dato)
            actual = actual.siguiente

        return resultado

    def recorrer_atras(self):
        resultado = []
        actual = self.cola

        while actual is not None:
            resultado.append(actual.dato)
            actual = actual.anterior

        return resultado