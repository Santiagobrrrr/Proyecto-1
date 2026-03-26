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
        results = data.get("results", []) or []

        personajes = [Personaje.from_api(item) for item in results]
        return personajes

    def obtener_detalle_personaje_api(self, character_id):
        data = self.client.get_character_detail(character_id)
        result = data.get("results", {}) or {}

        personaje = Personaje.from_api(result)

        issue_credits = result.get("issue_credits", []) or []
        volume_credits = result.get("volume_credits", []) or []

        comics = []

        for issue in issue_credits:
            nombre_issue = issue.get("name", "") or ""
            if nombre_issue:
                comics.append(nombre_issue)

        for volume in volume_credits:
            nombre_volume = volume.get("name", "") or ""
            if nombre_volume and nombre_volume not in comics:
                comics.append(nombre_volume)

        personaje.comics = comics[:20]

        return personaje

    def guardar_personajes_desde_api(self, query="Spider-Man", limit=10, offset=0):
        personajes = self.buscar_personajes_api(query=query, limit=limit, offset=offset)
        AlmacenamientoService.guardar_personajes(personajes)
        return personajes

    def guardar_detalles_personajes_desde_api(self, query="Spider-Man", limit=10, offset=0):
        personajes_base = self.buscar_personajes_api(query=query, limit=limit, offset=offset)
        personajes_detallados = []

        for personaje in personajes_base:
            try:
                detalle = self.obtener_detalle_personaje_api(personaje.id)
                personajes_detallados.append(detalle)
            except Exception as e:
                print(f"No se pudo obtener detalle del personaje {personaje.nombre}: {e}")
                personajes_detallados.append(personaje)

        AlmacenamientoService.guardar_personajes(personajes_detallados)
        return personajes_detallados

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

    def filtrar_por_editorial(self, editorial="Marvel"):
        personajes = self.cargar_personajes_desde_json()
        editorial = editorial.lower().strip()

        resultados = []
        for personaje in personajes:
            if personaje.editorial.lower() == editorial:
                resultados.append(personaje)

        return resultados

    def paginar_personajes(self, personajes, pagina=1, por_pagina=ITEMS_PER_PAGE):
        if pagina < 1:
            pagina = 1

        inicio = (pagina - 1) * por_pagina
        fin = inicio + por_pagina
        return personajes[inicio:fin]