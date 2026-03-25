from dataclasses import dataclass

@dataclass
class Creador:
    id: int | None = None
    nombre: str = ""
    rol: str = ""
    imagen_url: str = ""

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "rol": self.rol,
            "imagen_url": self.imagen_url
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get("id"),
            nombre=data.get("nombre", ""),
            rol=data.get("rol", ""),
            imagen_url=data.get("imagen_url", "")
        )