from src.api.comic_vine import ComicVineClient
from src.modelos.comic import Comic
from src.servicios.almacenamiento import AlmacenamientoService
from src.estructura_datos.lista_simple import ListaSimple
from config import ITEMS_PER_PAGE


class ComicService:
    def __init__(self):
        self.client = ComicVineClient()

    def obtener_comics_api(self, limit=10, offset=0):
        data = self.client.list_issues(limit=limit, offset=offset)
        results = data.get("results", [])
        comics = [Comic.from_api(item) for item in results]
        return comics

    def guardar_comics_desde_api(self, limit=10, offset=0):
        comics = self.obtener_comics_api(limit=limit, offset=offset)
        AlmacenamientoService.guardar_comics(comics)
        return comics

    def cargar_comics_desde_json(self):
        return AlmacenamientoService.cargar_comics()

    def obtener_lista_simple_comics(self, comics=None):
        if comics is None:
            comics = self.cargar_comics_desde_json()

        lista = ListaSimple()
        for comic in comics:
            lista.agregar_al_final(comic)

        return lista

    def buscar_comics_por_nombre(self, texto):
        comics = self.cargar_comics_desde_json()
        texto = texto.lower().strip()

        resultados = []
        for comic in comics:
            if texto in comic.nombre.lower():
                resultados.append(comic)

        return resultados

    def paginar_comics(self, comics, pagina=1, por_pagina=ITEMS_PER_PAGE):
        if pagina < 1:
            pagina = 1

        inicio = (pagina - 1) * por_pagina
        fin = inicio + por_pagina
        return comics[inicio:fin]