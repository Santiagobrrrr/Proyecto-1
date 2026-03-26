from config import validate_config
from src.api.comic_vine import ComicVineClient
from src.modelos.personajes import Personaje
from src.servicios.almacenamiento import AlmacenamientoService


def test_personajes():
    client = ComicVineClient()

    print("Buscando personajes en Comic Vine...")
    data = client.search_characters("Spider-Man", limit=5)

    results = data.get("results", [])
    personajes = [Personaje.from_api(item) for item in results]

    print(f"Personajes convertidos a objetos: {len(personajes)}")

    for i, personaje in enumerate(personajes, start=1):
        print(f"{i}. {personaje.nombre} | Editorial: {personaje.editorial}")

    AlmacenamientoService.guardar_personajes(personajes)
    print("Personajes guardados en personajes.json")

    personajes_cargados = AlmacenamientoService.cargar_personajes()
    print(f"Personajes cargados desde JSON: {len(personajes_cargados)}")

    for i, personaje in enumerate(personajes_cargados, start=1):
        print(f"{i}. {personaje.nombre}")


if __name__ == "__main__":
    validate_config()
    test_personajes()