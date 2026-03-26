from dataclasses import dataclass, field
from src.modelos.creador import Creador


@dataclass
class Comic:
    id: int | None = None
    nombre: str = ""
    numero: str = ""
    descripcion_corta: str = ""
    descripcion: str = ""
    fecha_publicacion: str = ""
    imagen_url: str = ""
    volumen: str = ""
    url_detalle: str = ""
    editorial: str = ""
    personajes: list[str] = field(default_factory=list)
    creadores: list[Creador] = field(default_factory=list)

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "numero": self.numero,
            "descripcion_corta": self.descripcion_corta,
            "descripcion": self.descripcion,
            "fecha_publicacion": self.fecha_publicacion,
            "imagen_url": self.imagen_url,
            "volumen": self.volumen,
            "url_detalle": self.url_detalle,
            "personajes": self.personajes,
            "editorial": self.editorial,
            "creadores": [creador.to_dict() for creador in self.creadores]
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get("id"),
            nombre=data.get("nombre", ""),
            numero=data.get("numero", ""),
            descripcion_corta=data.get("descripcion_corta", ""),
            descripcion=data.get("descripcion", ""),
            fecha_publicacion=data.get("fecha_publicacion", ""),
            editorial=data.get("editorial", ""),
            imagen_url=data.get("imagen_url", ""),
            volumen=data.get("volumen", ""),
            url_detalle=data.get("url_detalle", ""),
            personajes=data.get("personajes", []),
            creadores=[Creador.from_dict(c) for c in data.get("creadores", [])]
        )

    @classmethod
    def from_api(cls, data, editorial=""):
        imagen = data.get("image") or {}
        volumen = data.get("volume") or {}

        nombre_issue = data.get("name", "") or ""
        nombre_volumen = volumen.get("name", "") or ""
        numero_issue = str(data.get("issue_number", "") or "")
        fecha = data.get("store_date", "") or data.get("cover_date", "") or ""

        if nombre_issue:
            nombre_final = nombre_issue
        elif nombre_volumen and numero_issue:
            nombre_final = f"{nombre_volumen} #{numero_issue}"
        elif nombre_volumen:
            nombre_final = nombre_volumen
        else:
            nombre_final = "Sin nombre"

        return cls(
            id=data.get("id"),
            nombre=nombre_final,
            numero=numero_issue,
            descripcion_corta=data.get("deck", "") or "",
            descripcion=data.get("description", "") or "",
            fecha_publicacion=fecha,
            imagen_url=imagen.get("small_url", "") or "",
            volumen=nombre_volumen,
            editorial=editorial,
            url_detalle=data.get("site_detail_url", "") or "",
            personajes=[],
            creadores=[]
        )