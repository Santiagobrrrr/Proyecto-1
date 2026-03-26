from config import validate_config
from src.servicios.comic_s import ComicService
from src.servicios.personaje_s import PersonajeService

def prueba_comics():
    print("=== PRUEBA DE COMICS ===")
    service = ComicService()

    comics = service.guardar_comics_desde_api(limit=8)
    print(f"Comics obtenidos desde API: {len(comics)}")

    for i, comic in enumerate(comics, start=1):
        nombres_creadores = ", ".join([c.nombre for c in comic.creadores[:3]])
        if not nombres_creadores:
            nombres_creadores = "Sin creadores"

        print(
            f"{i}. {comic.nombre} | "
            f"Editorial: {comic.editorial} | "
            f"Fecha: {comic.fecha_publicacion} | "
            f"Creadores: {nombres_creadores}"
        )

    comics_json = service.cargar_comics_desde_json()
    print(f"Comics cargados desde JSON: {len(comics_json)}")

    lista = service.obtener_lista_simple_comics(comics_json)
    print(f"Comics en ListaSimple: {len(lista)}")
    print()

def prueba_personajes():
    print("=== PRUEBA DE PERSONAJES ===")
    service = PersonajeService()

    personajes = service.guardar_personajes_desde_api(query="Spider-Man", limit=5)
    print(f"Personajes obtenidos desde API: {len(personajes)}")

    for i, personaje in enumerate(personajes, start=1):
        print(f"{i}. {personaje.nombre} | Editorial: {personaje.editorial}")

    personajes_json = service.cargar_personajes_desde_json()
    print(f"Personajes cargados desde JSON: {len(personajes_json)}")

    lista = service.obtener_lista_simple_personajes(personajes_json)
    print(f"Personajes en ListaSimple: {len(lista)}")
    print()

if __name__ == "__main__":
    validate_config()
    prueba_comics()
    prueba_personajes()