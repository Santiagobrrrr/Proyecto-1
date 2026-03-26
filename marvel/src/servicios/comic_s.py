from src.api.comic_vine import ComicVineClient
from src.modelos.comic import Comic
from src.modelos.creador import Creador
from src.servicios.almacenamiento import AlmacenamientoService
from src.estructura_datos.lista_simple import ListaSimple
from config import ITEMS_PER_PAGE


class ComicService:
    def __init__(self):
        self.client = ComicVineClient()

    def obtener_comics_api(self, limit=10, offset=0):
        comics = []
        ids_agregados = set()

        batch_size = 20
        current_offset = offset
        max_batches = 5

        for _ in range(max_batches):
            data = self.client.list_issues(limit=batch_size, offset=current_offset)
            results = data.get("results", [])

            if not results:
                break

            for item in results:
                issue_id = item.get("id")
                volumen = item.get("volume") or {}
                volume_id = volumen.get("id")

                if not issue_id or not volume_id or issue_id in ids_agregados:
                    continue

                try:
                    volume_data = self.client.get_volume_detail(volume_id)
                    volume_result = volume_data.get("results", {}) or {}
                    publisher = volume_result.get("publisher") or {}
                    nombre_editorial = (publisher.get("name") or "").strip()

                    if nombre_editorial.lower() == "marvel":
                        detail_data = self.client.get_issue_detail(issue_id)
                        detail_result = detail_data.get("results", {}) or {}

                        comic = Comic.from_api(detail_result, editorial=nombre_editorial)

                        person_credits = detail_result.get("person_credits", []) or []
                        comic.creadores = [Creador.from_api(persona) for persona in person_credits]

                        comics.append(comic)
                        ids_agregados.add(issue_id)

                        if len(comics) >= limit:
                            return comics

                except Exception as e:
                    print(f"No se pudo procesar issue {issue_id}: {e}")

            current_offset += batch_size

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