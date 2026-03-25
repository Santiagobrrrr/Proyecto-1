import json
from config import COMICS_PATH, PERSONAJES_PATH
from src.modelos.comic import Comic
from src.modelos.personajes import Personaje


class AlmacenamientoService:
    @staticmethod
    def guardar_comics(comics):
        data = [comic.to_dict() for comic in comics]

        with open(COMICS_PATH, "w", encoding="utf-8") as archivo:
            json.dump(data, archivo, ensure_ascii=False, indent=4)

    @staticmethod
    def cargar_comics():
        with open(COMICS_PATH, "r", encoding="utf-8") as archivo:
            data = json.load(archivo)

        return [Comic.from_dict(item) for item in data]

    @staticmethod
    def guardar_personajes(personajes):
        data = [personaje.to_dict() for personaje in personajes]

        with open(PERSONAJES_PATH, "w", encoding="utf-8") as archivo:
            json.dump(data, archivo, ensure_ascii=False, indent=4)

    @staticmethod
    def cargar_personajes():
        with open(PERSONAJES_PATH, "r", encoding="utf-8") as archivo:
            data = json.load(archivo)

        return [Personaje.from_dict(item) for item in data]