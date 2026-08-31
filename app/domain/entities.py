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
    nombre: str | None = None   
    id: int | None = None       
    

@dataclass
class Envio:
    cliente: Cliente
    estado: EstadoEnvio = EstadoEnvio.PENDIENTE
    ultimo_error: str | None = None
    id: int | None = None