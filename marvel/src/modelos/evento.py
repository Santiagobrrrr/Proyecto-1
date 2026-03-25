from dataclasses import dataclass

@dataclass
class Evento:
    id: int | None = None
    nombre: str = ""
    descripcion: str = ""
    imagen_url: str = ""

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "imagen_url": self.imagen_url
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get("id"),
            nombre=data.get("nombre", ""),
            descripcion=data.get("descripcion", ""),
            imagen_url=data.get("imagen_url", "")
        )