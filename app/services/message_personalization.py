from __future__ import annotations
import random
from pathlib import Path
from app.domain.entities import Cliente
from config.settings import settings
from config.logger import logger

class MessagePersonalizerService:
    def __init__(self) -> None:
        # Directorio On-Premise para la multimedia
        self.media_dir = Path(settings.BASE_DIR) / "data" / "assets"
        self.media_dir.mkdir(parents=True, exist_ok=True)

        # 🚨 EL HOOK: Mensajes rotativos al azar, pero IMAGEN FIJA por asesor
        self._libreria_mensajes = {
            "carlos ruiz": {
                "textos": [
                    "Hola {nombre}, te saluda Carlos Ruiz. Tengo excelentes beneficios exclusivos para ti esta semana. ¿Te interesa?",
                    "¡Buen día, {nombre}! Carlos Ruiz por acá. Te escribo para compartirte una promoción especial vigente hoy.",
                    "¿Qué tal, {nombre}? Espero te encuentres muy bien. Te saluda Carlos Ruiz para dejarte una gran oportunidad de ahorro.",
                    "Hola {nombre}, un gusto saludarte. Soy Carlos Ruiz, tu asesor. Adjunto te dejo un beneficio pensado en ti.",
                    "Estimado(a) {nombre}, le escribe Carlos Ruiz. Nos complace presentarle las ofertas exclusivas de este mes."
                ],
                "imagen_fija": "promocion_carlos.jpg"  # ◄ Imagen única controlada por ti
            },
            "ana gomez": {
                "textos": [
                    "¡Buen día, {nombre}! Qué gusto saludarte. Te escribe Ana Gómez con nuestro catálogo actualizado y descuentos.",
                    "Hola {nombre}, te saluda Ana Gómez. Te adjunto las novedades de la sucursal con precios especiales para ti.",
                    "¿Cómo estás, {nombre}? Ana Gómez de tu sucursal de confianza te comparte grandes noticias adjuntas aquí.",
                    "Hola {nombre}. Soy Ana Gómez, un placer contactarte para dejarte nuestra lista de beneficios vigentes.",
                    "¡Saludos, {nombre}! Ana Gómez por aquí. Te comparto de inmediato las promociones que tenemos disponibles."
                ],
                "imagen_fija": "catalogo_ana.jpg"      # ◄ Imagen única controlada por ti
            },
            "default": {
                "textos": [
                    "Hola {nombre}, te saluda un asesor especializado. Te compartimos información importante de tus beneficios.",
                    "¡Buen día, {nombre}! Un gusto saludarte desde nuestra sucursal. Adjunto encontrarás novedades para ti.",
                    "¿Qué tal, {nombre}? Te escribimos para hacerte llegar los catálogos y promociones vigentes de la semana.",
                    "Hola {nombre}, esperamos que tengas un gran día. Te compartimos la siguiente información comercial exclusiva.",
                    "Estimado(a) {nombre}, le escribimos desde su sucursal asignada para presentarle las ofertas del mes."
                ],
                "imagen_fija": "info_general.jpg"     # ◄ Imagen única de respaldo
            }
        }

    def obtener_mensaje_e_imagen(self, cliente: Cliente) -> tuple[str, str]:
        """
        Elige un mensaje al azar de forma independiente, pero mantiene la imagen fija asignada.
        Retorna: (mensaje_personalizado, ruta_absoluta_imagen)
        """
        asesor_key = str(cliente.asesor_nombre).strip().lower()
        
        # Buscar la configuración del asesor o caer en default
        config = self._libreria_mensajes.get(asesor_key, self._libreria_mensajes["default"])
        
        # 1. Selección Aleatoria de Texto e Inyección de Nombre
        texto_plantilla = random.choice(config["textos"])
        nombre_saludo = cliente.nombre if cliente.nombre else "Cliente"
        mensaje_final = texto_plantilla.format(nombre=nombre_saludo)
        
        # 2. Asignación de Imagen Fija (Determinada por ti por código)
        nombre_imagen = config["imagen_fija"]
        ruta_imagen = self.media_dir / nombre_imagen
        
        # Validación defensiva On-Premise de existencia de archivo
        if not ruta_imagen.is_file():
            logger.warning(
                "La imagen fija configurada '%s' para el asesor '%s' no existe físicamente en: %s", 
                nombre_imagen, cliente.asesor_nombre, ruta_imagen
            )
            
        return mensaje_final, str(ruta_imagen)