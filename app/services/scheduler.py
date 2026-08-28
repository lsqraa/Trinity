from __future__ import annotations
from typing import Any

from app.domain.entities import Cliente, Envio, EstadoEnvio
from app.domain.ports import (
    IEnvioRepository,
    IExcelReader,
    IWhatsAppSender,
)
from app.services.validator import ContactValidatorService
from config.logger import logger
from config.settings import settings


class SchedulerService:

    def __init__(
        self,
        excel_reader: IExcelReader,
        envio_repo: IEnvioRepository,
        whatsapp_sender: IWhatsAppSender,
        validator_service: ContactValidatorService,
    ) -> None:
        self.excel_reader = excel_reader
        self.envio_repo = envio_repo
        self.whatsapp_sender = whatsapp_sender
        self.validator_service = validator_service

    def importar_campana_desde_excel(self, file_path: str) -> int:
        logger.info("Iniciando importación de campaña desde Excel: %s", file_path)
        raw_records = self.excel_reader.extract_raw_records(file_path)
        clientes = self.validator_service.validate_and_transform_records(raw_records)
        if not clientes:
            logger.warning("No se encontraron registros válidos para importar en %s", file_path)
            return 0
        nuevos_guardados = self.envio_repo.save_clientes(clientes)
        logger.info(
            "Campaña importada exitosamente. Registros válidos: %d, Nuevos envíos en cola: %d",
            len(clientes),
            nuevos_guardados,
        )
        return nuevos_guardados

    def ejecutar_envios_del_dia(self, personalizador_servicio: Any) -> str:
        envios_hoy = self.envio_repo.get_envios_hoy_count()
        limite_diario = settings.DAILY_MESSAGE_LIMIT
        cupos_disponibles = max(0, limite_diario - envios_hoy)

        logger.info(
            "Control de cuota diaria: %d/%d mensajes enviados hoy. Cupos disponibles: %d",
            envios_hoy,
            limite_diario,
            cupos_disponibles,
        )

        if cupos_disponibles <= 0:
            msg = f"Cuota diaria alcanzada: {envios_hoy}/{limite_diario} mensajes enviados hoy."
            logger.warning(msg)
            return msg

        pendientes = self.envio_repo.get_next_pendientes(limit=cupos_disponibles)
        if not pendientes:
            msg = "No hay envíos pendientes en cola para procesar."
            logger.info(msg)
            return msg

        exitosos = 0
        fallidos = 0

        logger.info("Conectando servicio de WhatsApp para procesar %d envíos...", len(pendientes))
        self.whatsapp_sender.connect()
        try:
            for envio in pendientes:
                if envio.id is None:
                    continue

                try:
                    mensaje, ruta_imagen = self._obtener_contenido_mensaje(
                        personalizador_servicio, envio.cliente
                    )
                    enviado = self.whatsapp_sender.send_message(
                        cliente=envio.cliente,
                        message=mensaje,
                        image_path=ruta_imagen,
                    )
                    if enviado:
                        self.envio_repo.actualizar_envio(
                            envio_id=envio.id,
                            estado=EstadoEnvio.ENVIADO,
                        )
                        exitosos += 1
                        logger.info(
                            "Envío exitoso a %s (%s).",
                            envio.cliente.telefono,
                            envio.cliente.nombre or envio.cliente.asesor_nombre,
                        )
                    else:
                        error_msg = "Fallo en la interfaz de WhatsApp durante el envío"
                        self.envio_repo.actualizar_envio(
                            envio_id=envio.id,
                            estado=EstadoEnvio.FALLIDO,
                            ultimo_error=error_msg,
                        )
                        fallidos += 1
                        logger.warning(
                            "Envío fallido a %s: %s",
                            envio.cliente.telefono,
                            error_msg,
                        )
                except Exception as e:
                    self.envio_repo.actualizar_envio(
                        envio_id=envio.id,
                        estado=EstadoEnvio.FALLIDO,
                        ultimo_error=str(e),
                    )
                    fallidos += 1
                    logger.error("Excepción en envío a %s: %s", envio.cliente.telefono, e)
        finally:
            self.whatsapp_sender.disconnect()
            logger.info("Desconexión de WhatsApp finalizada.")

        total_procesados = exitosos + fallidos
        resumen = (
            f"Jornada finalizada. Procesados: {total_procesados} "
            f"(Exitosos: {exitosos}, Fallidos: {fallidos}). "
            f"Total acumulado hoy: {envios_hoy + exitosos}/{limite_diario}."
        )
        logger.info(resumen)
        return resumen

    def _obtener_contenido_mensaje(
        self, personalizador: Any, cliente: Cliente
    ) -> tuple[str, str]:
        if hasattr(personalizador, "obtener_mensaje_e_imagen"):
            return personalizador.obtener_mensaje_e_imagen(cliente)
        if hasattr(personalizador, "get_message_and_image"):
            return personalizador.get_message_and_image(cliente)
        if hasattr(personalizador, "generar"):
            return personalizador.generar(cliente)
        if callable(personalizador):
            return personalizador(cliente)
        raise ValueError("El servicio personalizador no implementa un método compatible.")
