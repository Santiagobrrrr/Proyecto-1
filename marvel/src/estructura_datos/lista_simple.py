class NodoSimple:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None


class ListaSimple:
    def __init__(self):
        self.cabeza = None
        self.tamanio = 0

    def esta_vacia(self):
        return self.cabeza is None

    def __len__(self):
        return self.tamanio

    def agregar_al_final(self, dato):
        nuevo = NodoSimple(dato)

        if self.esta_vacia():
            self.cabeza = nuevo
        else:
            actual = self.cabeza
            while actual.siguiente is not None:
                actual = actual.siguiente
            actual.siguiente = nuevo

        self.tamanio += 1

    def agregar_al_inicio(self, dato):
        nuevo = NodoSimple(dato)
        nuevo.siguiente = self.cabeza
        self.cabeza = nuevo
        self.tamanio += 1

    def obtener_por_indice(self, indice):
        if indice < 0 or indice >= self.tamanio:
            raise IndexError("Índice fuera de rango")

        actual = self.cabeza
        contador = 0

        while actual is not None:
            if contador == indice:
                return actual.dato
            actual = actual.siguiente
            contador += 1

    def buscar(self, condicion):
        actual = self.cabeza

        while actual is not None:
            if condicion(actual.dato):
                return actual.dato
            actual = actual.siguiente

        return None

    def to_list(self):
        resultado = []
        actual = self.cabeza

        while actual is not None:
            resultado.append(actual.dato)
            actual = actual.siguiente

        return resultado

    def __iter__(self):
        actual = self.cabeza
        while actual is not None:
            yield actual.dato
            actual = actual.siguiente