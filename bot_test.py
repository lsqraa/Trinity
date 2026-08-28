import sys
import time
from pathlib import Path

# Asegurar que Python encuentre la carpeta app desde la raíz
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from app.domain.entities import Cliente
from app.infrastructure.whatsapp.playwright_bot import PlaywrightWhatsAppBot

def probar_bot_cuenta_business():
    print("=== INICIANDO PRUEBA DE FLUJO EN CUENTA WHATSAPP BUSINESS ===")
    
    # 1. Configuración de clientes de prueba (Formato de 9 dígitos de Ecuador)
    # REEMPLAZA estos números con teléfonos reales para validar la continuidad
    clientes_prueba = [
        Cliente(
            telefono="963074330",  # Contacto 1: Validará la primera inserción en la agenda Business
            nombre="Cliente Business Alfa",
            asesor_nombre="Carlos Ruiz",
            id=1
        ),
        Cliente(
            telefono="986789388",  # Contacto 2: Validará el segundo envío consecutivo exitoso
            nombre="Cliente Business Beta",
            asesor_nombre="Carlos Ruiz",
            id=2
        ),
        Cliente(
            telefono="994841154",  # Contacto 2: Validará el segundo envío consecutivo exitoso
            nombre="Cliente Business 2",
            asesor_nombre="Carlos Isra xd",
            id=2
        )
    ]
    
    # 2. Definir la ruta física de tu imagen fija en Windows
    # REEMPLAZA esta ruta por una imagen real que tengas descargada en tu computadora
    ruta_imagen_fija = r"C:\Users\brown\Downloads\images.jpg"
    
    # Validación previa de seguridad On-Premise
    if not Path(ruta_imagen_fija).is_file():
        print(f"❌ ERROR CRÍTICO: El archivo de imagen no existe en la ruta especificada: {ruta_imagen_fija}")
        print("Por favor, corrige la ruta o coloca una imagen válida antes de iniciar.")
        return

    bot = PlaywrightWhatsAppBot()
    
    try:
        # 3. Conectar al navegador (Abre Chromium persistente)
        bot.connect()
        print("\n=== Navegador Inicializado. Escanea el QR con la cuenta Business si es requerido ===")
        
        for index, cliente in enumerate(clientes_prueba, start=1):
            print(f"\n🚀 [PROCESANDO TARGET {index}/{len(clientes_prueba)}]")
            print(f"Nombre: {cliente.nombre} | Celular: {cliente.telefono}")
            print(f"Asesor a cargo: {cliente.asesor_nombre} -> Imagen fija: {Path(ruta_imagen_fija).name}")
            
            # 4. Despachar la acción física en la pasarela automatizada
            exito = bot.send_message(
                cliente=cliente,
                message=f"Hola {cliente.nombre}, este es un saludo de prueba automatizado desde la cuenta Business.",
                image_path=ruta_imagen_fija
            )
            
            if exito:
                print(f"✅ [TARGET {index}] - RESULTADO: True (Flujo de contacto y multimedia completado).")
            else:
                print(f"❌ [TARGET {index}] - RESULTADO: False (Fallo en selectores o timeout del formulario).")
            
            # Retraso técnico de cortesía para estabilizar la pantalla lateral antes de la limpieza con Escape
            if index < len(clientes_prueba):
                print("\nEsperando 6 segundos de estabilidad antes de pasar al siguiente cliente...")
                time.sleep(6)
                
        print("\n=== PRUEBA EN CUENTA BUSINESS FINALIZADA ===")
        
    except Exception as e:
        import traceback
        print("\n❌ EXCEPCIÓN CRÍTICA EN LA EJECUCIÓN DEL SCRIPT DE PRUEBA:")
        traceback.print_exc()
    finally:
        # 5. Desconectar y liberar memoria RAM de la sucursal
        print("\nCerrando pasarela de Playwright...")
        bot.disconnect()

if __name__ == "__main__":
    probar_bot_cuenta_business()