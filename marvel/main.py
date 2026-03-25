from config import validate_config
from src.api.comic_vine import ComicVineClient


def test_comicvine():
    client = ComicVineClient()

    print("Probando conexión con Comic Vine...")
    data = client.search_characters("Spider-Man", limit=5)

    results = data.get("results", [])
    print(f"Resultados encontrados: {len(results)}")

    for i, item in enumerate(results, start=1):
        print(f"{i}. {item.get('name', 'Sin nombre')}")


if __name__ == "__main__":
    validate_config()
    test_comicvine()