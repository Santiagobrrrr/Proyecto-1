from dataclasses import dataclass, field
from src.modelos.creador import Creador
from src.modelos.evento import Evento


@dataclass
class Personaje:
    id: int | None = None
    nombre: str = ""
    nombre_real: str = ""
    descripcion_corta: str = ""
    descripcion: str = ""
    imagen_url: str = ""
    editorial: str = ""
    url_detalle: str = ""
    comics: list[str] = field(default_factory=list)
    eventos: list[Evento] = field(default_factory=list)
    creadores: list[Creador] = field(default_factory=list)

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "nombre_real": self.nombre_real,
            "descripcion_corta": self.descripcion_corta,
            "descripcion": self.descripcion,
            "imagen_url": self.imagen_url,
            "editorial": self.editorial,
            "url_detalle": self.url_detalle,
            "comics": self.comics,
            "eventos": [evento.to_dict() for evento in self.eventos],
            "creadores": [creador.to_dict() for creador in self.creadores]
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get("id"),
            nombre=data.get("nombre", ""),
            nombre_real=data.get("nombre_real", ""),
            descripcion_corta=data.get("descripcion_corta", ""),
            descripcion=data.get("descripcion", ""),
            imagen_url=data.get("imagen_url", ""),
            editorial=data.get("editorial", ""),
            url_detalle=data.get("url_detalle", ""),
            comics=data.get("comics", []),
            eventos=[Evento.from_dict(e) for e in data.get("eventos", [])],
            creadores=[Creador.from_dict(c) for c in data.get("creadores", [])]
        )

    @classmethod
    def from_api(cls, data):
        imagen = data.get("image") or {}
        editorial = data.get("publisher") or {}

        return cls(
            id=data.get("id"),
            nombre=data.get("name", "") or "Sin nombre",
            nombre_real=data.get("real_name", "") or "",
            descripcion_corta=data.get("deck", "") or "",
            descripcion=data.get("description", "") or "",
            imagen_url=imagen.get("small_url", "") or "",
            editorial=editorial.get("name", "") or "",
            url_detalle=data.get("site_detail_url", "") or "",
            comics=[],
            eventos=[],
            creadores=[]
        )