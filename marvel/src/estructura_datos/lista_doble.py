class NodoDoble:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None
        self.anterior = None


class ListaDoble:
    def __init__(self):
        self.cabeza = None
        self.cola = None
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
        else:
            nuevo.anterior = self.cola
            self.cola.siguiente = nuevo
            self.cola = nuevo

        self.tamanio += 1

    def prepend(self, dato):
        nuevo = NodoDoble(dato)

        if self.esta_vacia():
            self.cabeza = nuevo
            self.cola = nuevo
        else:
            nuevo.siguiente = self.cabeza
            self.cabeza.anterior = nuevo
            self.cabeza = nuevo

        self.tamanio += 1

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

    def obtener_nodo_por_indice(self, indice):
        if indice < 0 or indice >= self.tamanio:
            raise IndexError("Índice fuera de rango")

        actual = self.cabeza
        contador = 0

        while actual is not None:
            if contador == indice:
                return actual
            actual = actual.siguiente
            contador += 1

    def obtener_dato_por_indice(self, indice):
        nodo = self.obtener_nodo_por_indice(indice)
        return nodo.dato

    def to_list(self):
        return self.recorrer_adelante()

    def __iter__(self):
        actual = self.cabeza
        while actual is not None:
            yield actual.dato
            actual = actual.siguiente