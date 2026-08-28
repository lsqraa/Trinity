from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any
from app.domain.entities import Cliente, Envio, EstadoEnvio


class WhatsAppError(Exception):
    pass


class ChatNotFoundError(WhatsAppError):
    pass


class SendFailedError(WhatsAppError):
    pass


class PageNotReadyError(WhatsAppError):
    pass


class IWhatsAppSender(ABC):

    @abstractmethod
    def connect(self) -> None:
        pass

    @abstractmethod
    def send_message(self, cliente: Cliente, message: str, image_path: str) -> bool:
        pass

    @abstractmethod
    def disconnect(self) -> None:
        pass


class IEnvioRepository(ABC):

    @abstractmethod
    def save_clientes(self, clientes: list[Cliente]) -> int:
        pass

    @abstractmethod
    def get_next_pendientes(self, limit: int = 45) -> list[Envio]:
        pass

    @abstractmethod
    def actualizar_envio(
        self,
        envio_id: int,
        estado: EstadoEnvio,
        ultimo_error: str | None = None,
    ) -> None:
        pass

    @abstractmethod
    def get_envios_hoy_count(self) -> int:
        pass

    @abstractmethod
    def get_stats(self) -> dict[str, int]:
        pass


class IExcelReader(ABC):

    @abstractmethod
    def extract_raw_records(self, file_path: str) -> list[dict[str, Any]]:
        pass

