from __future__ import annotations
import random
from pathlib import Path
from app.domain.entities import Cliente
from config.settings import settings
from config.logger import logger

class MessagePersonalizerService:
    def __init__(self) -> None:
        self.media_dir = Path(settings.BASE_DIR) / "data" / "assets"
        self.media_dir.mkdir(parents=True, exist_ok=True)

        self._variantes_mensajes = [
            "👋 ¡Hola {nombre}! Nos contactaste anteriormente. Si no recuerdas haberlo hecho, por favor "
            "ignora este mensaje. En South American Language Center Cotopaxi "
            "tenemos una forma diferente de aprender: clases personalizadas, "
            "práctica y acompañamiento para que avances de verdad. "
            "🗣️✨🎯 Si tu objetivo es mejorar para estudiar, trabajar, viajar "
            "o comunicarte con más confianza, ¡este es un buen momento para comenzar! "
            "📲 Contáctanos y agenda tu prueba de ubicación. ¡Da el primer paso!",

            "👋 ¡Hola {nombre}! Nos contactaste tiempo atras, Si no fuiste tu porfavor "
            "ignora este mensaje. En South American Language Center Cotopaxi "
            "tenemos una forma diferente de aprender: clases personalizadas, "
            "experiencias prácticas y acompañamiento para que avances de verdad. "
            "🗣️✨ 🎯 Si estás buscando mejorar tu inglés para estudiar, trabajar, "
            "viajar o simplemente sentirte más seguro al hablar, este puede ser "
            "tu momento.📲 Escríbenos y agenda tu prueba de ubicación. ¡Empieza hoy!",

            "👋 ¡Hola {nombre}! Nos contactaste tiempo atrás y queremos ayudarte a continuar con tu proceso. Si no fuiste tú, por favor "
            "ignora este mensaje. En South American Language Center Cotopaxi "
            "ofrecemos clases personalizadas, práctica y acompañamiento "
            "para que aprender inglés sea más sencillo y puedas ver resultados. "
            "🗣️✨🎯 Si quieres mejorar tu inglés para estudiar, trabajar, viajar "
            "o hablar con mayor confianza, ¡este puede ser tu momento! "
            "📲 Escríbenos para conocer más y agenda tu prueba de ubicación. ¡Empieza hoy!",

            "👋 ¡Hola {nombre}! Nos contactaste hace algún tiempo. Si no fuiste tú, "
            "por favor ignora este mensaje. En South American Language Center Cotopaxi "
            "tenemos una manera diferente de aprender: clases personalizadas, "
            "experiencias prácticas y acompañamiento para que realmente puedas avanzar. "
            "🗣️✨🎯 Si quieres mejorar tu inglés para estudiar, trabajar, "
            "viajar o simplemente ganar confianza al hablar, ¡este puede ser "
            "el momento! 📲 Escríbenos y agenda tu prueba de ubicación. ¡Empieza hoy!"
        ]

        self._imagen_fija = "salc.jpeg"

    def obtener_mensaje_e_imagen(self, cliente: Cliente) -> tuple[str, str]:
        plantilla_seleccionada = random.choice(self._variantes_mensajes)
        nombre_saludo = cliente.nombre if cliente.nombre else "Cliente"
        mensaje_final = plantilla_seleccionada.format(nombre=nombre_saludo)
        
        ruta_imagen = self.media_dir / self._imagen_fija
        
        if not ruta_imagen.is_file():
            logger.warning(
                "La imagen fija institucional '%s' no se encuentra físicamente en: %s. "
                "Por favor, cópiala desde Downloads antes de iniciar la campaña.", 
                self._imagen_fija, ruta_imagen
            )
            
        return mensaje_final, str(ruta_imagen)