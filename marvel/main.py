from src.servicios.personaje_s import PersonajeService

def prueba_personajes():
    print("=== PRUEBA DE PERSONAJES ===")
    service = PersonajeService()

    personajes = service.guardar_detalles_personajes_desde_api(query="Spider-Man", limit=5)
    print(f"Personajes obtenidos desde API: {len(personajes)}")

    for i, personaje in enumerate(personajes, start=1):
        comics_texto = ", ".join(personaje.comics[:3]) if personaje.comics else "Sin comics"
        print(
            f"{i}. {personaje.nombre} | "
            f"Editorial: {personaje.editorial} | "
            f"Nombre real: {personaje.nombre_real or 'No disponible'} | "
            f"Comics: {comics_texto}"
        )

    personajes_json = service.cargar_personajes_desde_json()
    print(f"Personajes cargados desde JSON: {len(personajes_json)}")

    lista = service.obtener_lista_simple_personajes(personajes_json)
    print(f"Personajes en ListaSimple: {len(lista)}")
    print()

if __name__ == "__main__":
    prueba_personajes()