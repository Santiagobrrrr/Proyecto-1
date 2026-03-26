from src.api.comic_vine import ComicVineClient
from src.modelos.personajes import Personaje
from src.servicios.almacenamiento import AlmacenamientoService
from src.estructura_datos.lista_simple import ListaSimple
from config import ITEMS_PER_PAGE

class PersonajeService:
    def __init__(self):
        self.client = ComicVineClient()

    def buscar_personajes_api(self, query="Spider-Man", limit=10, offset=0):
        data = self.client.search_characters(query=query, limit=limit, offset=offset)
        results = data.get("results", [])
        personajes = [Personaje.from_api(item) for item in results]
        return personajes

    def guardar_personajes_desde_api(self, query="Spider-Man", limit=10, offset=0):
        personajes = self.buscar_personajes_api(query=query, limit=limit, offset=offset)
        AlmacenamientoService.guardar_personajes(personajes)
        return personajes

    def cargar_personajes_desde_json(self):
        return AlmacenamientoService.cargar_personajes()

    def obtener_lista_simple_personajes(self, personajes=None):
        if personajes is None:
            personajes = self.cargar_personajes_desde_json()

        lista = ListaSimple()
        for personaje in personajes:
            lista.agregar_al_final(personaje)

        return lista

    def buscar_personajes_por_nombre(self, texto):
        personajes = self.cargar_personajes_desde_json()
        texto = texto.lower().strip()

        resultados = []
        for personaje in personajes:
            if texto in personaje.nombre.lower():
                resultados.append(personaje)

        return resultados

    def paginar_personajes(self, personajes, pagina=1, por_pagina=ITEMS_PER_PAGE):
        if pagina < 1:
            pagina = 1

        inicio = (pagina - 1) * por_pagina
        fin = inicio + por_pagina
        return personajes[inicio:fin]