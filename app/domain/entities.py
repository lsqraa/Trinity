from __future__ import annotations
from dataclasses import dataclass
from enum import Enum


class EstadoEnvio(str, Enum):
    PENDIENTE = "PENDIENTE"
    ENVIADO = "ENVIADO"
    FALLIDO = "FALLIDO"


@dataclass
class Cliente:
    telefono: str
    asesor_nombre: str
    nombre: str | None = None   # Si es opcional se le daun valor por defecto
    id: int | None = None       # Los valores por defecto siempre al final. Estar atento al momento de insertar el cliente por primera vez para capturar el ID que devuelve la base de datos.


@dataclass
class Envio:
    cliente: Cliente
    estado: EstadoEnvio = EstadoEnvio.PENDIENTE
    ultimo_error: str | None = None
    id: int | None = None