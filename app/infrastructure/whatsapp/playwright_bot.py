from __future__ import annotations
import random
import re
import time
import unicodedata
from pathlib import Path
from typing import Any

from playwright.sync_api import (
    BrowserContext,
    Page,
    Playwright,
    TimeoutError as PlaywrightTimeoutError,
    sync_playwright,
)

from app.domain.entities import Cliente
from app.domain.ports import (
    ChatNotFoundError,
    IWhatsAppSender,
    PageNotReadyError,
    SendFailedError,
)
from config.logger import logger
from config.settings import settings


WSP_SELECTORS: dict[str, Any] = {
    "PAGINA_CARGADA_INDICADOR": '#side input, div[data-icon="chat"], [aria-label="Nuevo chat"]',
    "SEARCH_INPUT": '#side input, div[role="textbox"]',
    "NUEVO_CHAT_BTN": (
        'button:has(title:has-text("wds-ic-new-chat-filled")), '
        'button:has(title:has-text("ic-add")), '
        'button[data-tab="2"]'
    ),
    "CONTACT_NAME_INPUTS": [
        'input[placeholder*="nombre" i]',
        'input[placeholder*="name" i]',
        'input[aria-label*="nombre" i]',
        'input[aria-label*="name" i]',
        'div[role="textbox"]',  
    ],
    
    "CONTACT_PHONE_INPUTS": [
        'input[type="tel"]',
        'input[placeholder*="teléfono" i]',
        'input[placeholder*="telefono" i]',
        'input[placeholder*="phone" i]',
        'input[aria-label*="teléfono" i]',
        'input[aria-label*="telefono" i]',
        'input[aria-label*="phone" i]',
    ],
    "BOTON_GUARDAR_CONTACTO": [
        'button[aria-label="Guardar"]',
        'button[aria-label="Save"]',
        'button[title="Guardar"]',
        'button[title="Save"]',
        '[role="button"][aria-label="Guardar"]',
        '[role="button"][aria-label="Save"]',
        'button:has([data-icon="checkmark"])',
        '[role="button"]:has([data-icon="checkmark"])',
        'button:has([data-icon="check"])',
        '[role="button"]:has([data-icon="check"])',
    ],
    "BOTON_ATRAS": [
        'button[aria-label="Atrás"]',
        'button[aria-label="Back"]',
        '[role="button"][aria-label="Atrás"]',
        '[role="button"][aria-label="Back"]',
        'button:has([data-icon="back"])',
        '[role="button"]:has([data-icon="back"])',
    ],
    "CAJA_TEXTO_MENSAJE": (
        '[data-testid="conversation-compose-box-input"], '
        'footer div[role="textbox"]'
    ),
    "BOTON_ADJUNTAR": (
        'button[aria-label="Adjuntar"], button[data-testid="compose-btn-attach"], '
        'div[title="Adjuntar"], [aria-label*="Adjuntar"]'
    ),
    "INPUT_ARCHIVO_MEDIA": 'input[type="file"][accept*="video"]',
    "VISTA_PREVIA_MEDIA": (
        '[data-testid="media-preview"], [data-testid="media-preview-content"], '
        'div[role="dialog"], img[src^="blob:"], video[src^="blob:"]'
    ),
    "BOTON_ENVIAR": [
        'button[data-testid="compose-btn-send"]',
        '#main button[aria-label="Enviar"]',
        '#main button[aria-label="Send"]',
        '#main [role="button"][aria-label="Enviar"]',
        '#main [role="button"][aria-label="Send"]',
        'span[data-icon="send"]',
        'button:has([data-icon="wds-ic-send-filled"])',
        '[role="button"]:has([data-icon="wds-ic-send-filled"])',
        'button:has([data-icon="send"])',
        '[role="button"]:has([data-icon="send"])',
    ],
}

PHONE_ON_WHATSAPP = re.compile(
    r"Este número de teléfono está en WhatsApp|This phone number is on WhatsApp",
    re.I,
)
PHONE_ALREADY_CONTACT = re.compile(
    r"Este número de teléfono ya está en tus contactos|"
    r"This phone number is already in your contacts",
    re.I,
)
ADDRESS_BOOK_CONFIRMATION = re.compile(
    r"Se añadirá este contacto a la libreta de contactos de tu teléfono|"
    r"This contact will be added to your phone's address book",
    re.I,
)
PHOTOS_MENU = re.compile(r"fotos? y videos|photos|imágenes y videos", re.I)
DIALOG_LABELS = [
    "Aceptar", "Continuar", "Enviar", "OK", "Listo",
    "Hecho", "Guardar", "Done", "Continue", "Ok", "Close", "Cerrar",
]


class PlaywrightWhatsAppBot(IWhatsAppSender):
    def __init__(
        self,
        profile_dir: str | None = None,
        whatsapp_url: str | None = None,
        headless: bool | None = None,
        login_timeout_sec: int | None = None,
    ) -> None:
        self.profile_dir = Path(profile_dir or settings.PLAYWRIGHT_USER_DATA_DIR)
        self.whatsapp_url = whatsapp_url or settings.WHATSAPP_URL
        self.headless = settings.PLAYWRIGHT_HEADLESS if headless is None else headless
        self.login_timeout_sec = login_timeout_sec or settings.LOGIN_TIMEOUT_SEC
        self._pw: Playwright | None = None
        self._context: BrowserContext | None = None
        self._page: Page | None = None

    def connect(self) -> None:
        self.profile_dir.mkdir(parents=True, exist_ok=True)
        self._pw = sync_playwright().start()
        self._context = self._pw.chromium.launch_persistent_context(
            user_data_dir=str(self.profile_dir),
            headless=self.headless,
            args=["--disable-notifications", "--start-maximized"],
        )
        self._page = (
            self._context.pages[0]
            if self._context.pages
            else self._context.new_page()
        )
        self._page.goto(self.whatsapp_url)
        self._wait_for_whatsapp_ready()
        self._human_delay(2.0, 4.0)

    def send_message(self, cliente: Cliente, message: str, image_path: str) -> bool:
        if not self._page:
            return False

        try:
            self._dismiss_dialog()
            if not self._open_new_chat(cliente):
                return False

            self._dismiss_dialog()
            self._human_delay(0.6, 1.4)

            if not self._send_message_with_image(message, image_path):
                return False

            delay = random.uniform(settings.MIN_DELAY_SECONDS, settings.MAX_DELAY_SECONDS)
            time.sleep(delay)
            return True
        except Exception:
            try:
                if self._page:
                    self._page.keyboard.press("Escape")
            except Exception:
                pass
            return False

    def disconnect(self) -> None:
        if self._context:
            self._context.close()
            self._context = None
        if self._pw:
            self._pw.stop()
            self._pw = None
        self._page = None

    def _wait_for_whatsapp_ready(self) -> None:
        if not self._page:
            raise PageNotReadyError("Página no inicializada.")

        deadline = time.time() + self.login_timeout_sec
        while time.time() < deadline:
            try:
                self._page.locator(WSP_SELECTORS["PAGINA_CARGADA_INDICADOR"]).first.wait_for(
                    state="visible", timeout=3000
                )
                return
            except PlaywrightTimeoutError:
                pass

            for label in ("Usar aquí", "Use here"):
                try:
                    self._page.get_by_text(label, exact=True).click(timeout=1200)
                except Exception:
                    pass
            time.sleep(3)

        raise PageNotReadyError(
            f"WhatsApp Web no cargó en {self.login_timeout_sec}s."
        )

    def _open_new_chat(self, cliente: Cliente) -> bool:
        if not self._page:
            return False

        self._page.keyboard.press("Escape")
        self._human_delay(0.1, 0.2)
        self._page.keyboard.press("Escape")
        self._human_delay(0.15, 0.3)

        contact_name = self._get_display_name(cliente)
        
        new_contact_option = self._page.locator('text="Nuevo contacto", text="New contact"').first

        try:
            target_chat = self._page.locator('title:text-is("wds-ic-new-chat-filled") >> xpath=..').first
            if target_chat.count() == 0:
                target_chat = self._page.locator('title:text-is("ic-add") >> xpath=..').first

            target_chat.wait_for(state="visible", timeout=2000)
            target_chat.click(force=True, timeout=2000)
            
            self._human_delay(0.5, 0.7)
            
        except Exception as e:
            logger.error("No se pudo presionar el botón de Nuevo Chat con el mouse: %s", e)
            self._page.keyboard.press("Escape")
            return False

        interfaz_moderna = False

        try:
            new_contact_option.wait_for(state="visible", timeout=1200)
            if new_contact_option.is_visible():
                new_contact_option.click(timeout=1500, force=True)
                self._human_delay(0.3, 0.5)
                interfaz_moderna = True
        except Exception:
            interfaz_moderna = False

        if not interfaz_moderna:
            try:
                icono_agregar_clasico = self._page.locator(
                    'button:has(title:has-text("person")), [aria-label*="contacto" i], [title*="contacto" i]'
                ).first
                if icono_agregar_clasico.count() > 0 and icono_agregar_clasico.is_visible(timeout=1000):
                    icono_agregar_clasico.click(force=True, timeout=1500)
                else:
                    self._page.keyboard.press("Tab")
                    self._page.keyboard.press("Enter")
                self._human_delay(0.4, 0.7)
                interfaz_moderna = True
            except Exception as e:
                logger.warning("No se pudo desplegar formulario de contacto clásico: %s", e)
                interfaz_moderna = False

        self._human_delay(0.2, 0.4)
        old_header = self._get_chat_header_text()

        if interfaz_moderna:
            self._human_delay(0.4, 0.6)

            if not self._fill_contact_name(contact_name):
                logger.warning("No se pudo completar el campo de nombre para el contacto.")
                self._page.keyboard.press("Escape")
                return False

            if not self._fill_contact_phone(cliente.telefono):
                logger.warning("No se pudo completar el campo de teléfono para %s", cliente.telefono)
                self._page.keyboard.press("Escape")
                return False

            if self._phone_is_already_contact():
                logger.info("El teléfono %s ya figura en la agenda de contactos.", cliente.telefono)

            try:
                self._page.get_by_text(PHONE_ON_WHATSAPP).first.wait_for(state="visible", timeout=6000)
            except Exception as e:
                logger.warning("Validación de número en WhatsApp fallida para %s: %s", cliente.telefono, e)
                self._page.keyboard.press("Escape")
                return False

            if not self._confirm_add_to_address_book():
                logger.warning("No se pudo confirmar la adición a la libreta de direcciones.")
                self._page.keyboard.press("Escape")
                return False

            if not self._save_new_contact():
                logger.warning("Fallo al guardar el nuevo contacto en la libreta.")
                self._page.keyboard.press("Escape")
                return False
        else:
            caja_busqueda = self._page.locator(WSP_SELECTORS["SEARCH_INPUT"]).first
            caja_busqueda.click(timeout=2000)
            caja_busqueda.fill("")
            for ch in cliente.telefono:
                caja_busqueda.type(ch, delay=random.randint(40, 90)) 
            self._page.keyboard.press("Enter")
            self._human_delay(1.5, 2.5)

        deadline = time.time() + 6
        while time.time() < deadline:
            if self._get_chat_header_text() != old_header:
                logger.info("Chat abierto exitosamente para %s (%s).", cliente.telefono, contact_name)
                return True
            time.sleep(0.05) 

        logger.warning("Timeout al sincronizar apertura de chat para %s.", cliente.telefono)
        self._page.keyboard.press("Escape")
        self._human_delay(0.3, 0.6)
        return False
    
    def _send_message_with_image(self, text: str, image_path: str) -> bool:
        if not self._page:
            return False

        self._type_like_human(WSP_SELECTORS["CAJA_TEXTO_MENSAJE"], text)

        if not self._attach_image(image_path):
            return False

        deadline = time.time() + 15
        while time.time() < deadline:
            if self._is_preview_open():
                break
            time.sleep(0.25)

        if not self._is_preview_open():
            return False

        time.sleep(1)
        return self._send_current_message()

    def _get_display_name(self, cliente: Cliente) -> str:
        if cliente.nombre:
            cleaned = "".join(
                ch for ch in cliente.nombre if unicodedata.category(ch) != "Cc"
            ).strip()
            if cleaned:
                return cleaned
        return cliente.asesor_nombre.strip()

    def _human_delay(self, min_sec: float = 0.2, max_sec: float = 0.5) -> None:
        time.sleep(random.uniform(min_sec, max_sec))

    def _type_like_human(self, selector: str, text: str) -> None:
        if not self._page:
            return
        locator = self._page.locator(selector).first
        locator.click(timeout=4000)
        self._human_delay(0.2, 0.4)
        locator.fill("", timeout=4000)
        self._human_delay(0.1, 0.2)
        for ch in text:
            locator.type(ch, delay=random.randint(60, 140), timeout=4000)

    def _dismiss_dialog(self) -> None:
        if not self._page:
            return
        try:
            dialog = self._page.locator("div[role='dialog']:visible").first
            if not (dialog.count() and dialog.is_visible()):
                return
            for label in DIALOG_LABELS:
                try:
                    btn = self._page.get_by_text(label, exact=True).first
                    if btn.count() and btn.is_visible():
                        btn.click(timeout=1500)
                        self._human_delay(0.4, 0.9)
                        return
                except Exception:
                    continue
            btns = dialog.locator("button")
            if btns.count():
                btns.last.click(timeout=1500)
                self._human_delay(0.4, 0.9)
        except Exception:
            pass

    def _click_first_visible(self, selectors: list[str] | str, timeout: int = 2000) -> bool:
        if not self._page:
            return False
        selector_list = [selectors] if isinstance(selectors, str) else selectors
        for selector in selector_list:
            try:
                self._page.locator(selector).first.click(timeout=timeout)
                return True
            except Exception:
                continue
        return False

    def _fill_first_visible(self, selectors: list[str], text: str) -> bool:
        if not self._page:
            return False
        for selector in selectors:
            locator = self._page.locator(selector)
            for index in range(locator.count()):
                field = locator.nth(index)
                try:
                    if not field.is_visible():
                        continue
                    field.click(timeout=2000)
                    field.fill("", timeout=2000)
                    field.type(text, delay=random.randint(60, 140), timeout=5000)
                    return True
                except Exception:
                    continue
        return False

    def _type_into_field(self, field: Any, text: str) -> bool:
        field.click(timeout=2000)
        field.fill("", timeout=2000)
        field.type(text, delay=random.randint(60, 140), timeout=5000)
        return True

    def _type_in_labeled_field(self, labels: list[str], text: str) -> bool:
        if not self._page:
            return False
        for label in labels:
            field = self._page.get_by_label(label, exact=True).first
            try:
                if field.count() and field.is_visible():
                    return self._type_into_field(field, text)
            except Exception:
                continue
        return False

    def _fill_contact_phone(self, phone: str) -> bool:
        if not self._page:
            return False
            
        for label in ["Número de teléfono", "Teléfono"]:
            field = self._page.get_by_label(label, exact=True).first
            try:
                if field.count() and field.is_visible():
                    field.click(timeout=2000)
                    field.fill("", timeout=2000)
                    field.type(phone, delay=random.randint(15, 30), timeout=5000)
                    return True
            except Exception:
                continue

        for selector in WSP_SELECTORS["CONTACT_PHONE_INPUTS"]:
            fields = self._page.locator(selector)
            for index in range(fields.count()):
                field = fields.nth(index)
                try:
                    if not field.is_visible():
                        continue
                    field.click(timeout=2000)
                    field.fill("", timeout=2000)
                    field.type(phone, delay=random.randint(15, 30), timeout=5000)
                    entered = re.sub(r"\D", "", field.input_value(timeout=1000))
                    if entered.endswith(re.sub(r"\D", "", phone)):
                        return True
                except Exception:
                    continue
            return False

    def _fill_contact_name(self, name: str) -> bool:
        if self._type_in_labeled_field(["Nombre", "First name"], name):
            return True
            
        for selector in WSP_SELECTORS["CONTACT_NAME_INPUTS"]:
            fields = self._page.locator(selector)
            for index in range(fields.count()):
                field = fields.nth(index)
                try:
                    if not field.is_visible():
                        continue
                    field.click(timeout=2000)
                    field.fill("", timeout=2000)
                    field.type(name, delay=random.randint(15, 30), timeout=5000)
                    return True
                except Exception:
                    continue
        return False

    def _confirm_add_to_address_book(self) -> bool:
        if not self._page:
            return False
        try:
            control = self._page.get_by_text(ADDRESS_BOOK_CONFIRMATION).first
            control.wait_for(state="visible", timeout=5000)
            control.evaluate(
                """element => {
                    const target = element.closest(
                        'label, button, [role="button"], [role="checkbox"]'
                    ) || element;
                    target.click();
                }"""
            )
            self._human_delay(0.3, 0.6)
            return True
        except Exception:
            return False

    def _cancel_new_contact(self) -> None:
        if not self._page:
            return
        if not self._click_first_visible(WSP_SELECTORS["BOTON_ATRAS"], timeout=1500):
            self._page.keyboard.press("Escape")
        self._human_delay(0.4, 0.8)

    def _phone_is_already_contact(self) -> bool:
        if not self._page:
            return False
        try:
            self._page.get_by_text(PHONE_ALREADY_CONTACT).first.wait_for(
                state="visible", timeout=3000
            )
            return True
        except Exception:
            return False

    def _save_new_contact(self) -> bool:
        if not self._page:
            return False
        svgs = self._page.locator("svg:has(title)")
        for index in range(svgs.count() - 1, -1, -1):
            icon = svgs.nth(index)
            try:
                if not icon.is_visible():
                    continue
                title = icon.locator("title").text_content(timeout=1000)
                if (title or "").strip() != "ic-check":
                    continue
                try:
                    icon.click(timeout=3000)
                except Exception:
                    icon.evaluate(
                        """element => {
                            const target = element.closest('button, [role="button"]')
                                || element.parentElement;
                            target.click();
                        }"""
                    )
                return True
            except Exception:
                continue

        if self._click_first_visible(WSP_SELECTORS["BOTON_GUARDAR_CONTACTO"], timeout=5000):
            return True

        icons = self._page.locator("[data-icon='checkmark'], [data-icon='check']")
        for index in range(icons.count() - 1, -1, -1):
            icon = icons.nth(index)
            try:
                if not icon.is_visible():
                    continue
                icon.evaluate(
                    """element => {
                        const target = element.closest('button, [role="button"]')
                            || element.parentElement;
                        target.click();
                    }"""
                )
                return True
            except Exception:
                continue
        return False

    def _get_chat_header_text(self) -> str:
        if not self._page:
            return ""
        return self._page.evaluate(
            "() => { const h = document.querySelector('#main header'); "
            "return h ? h.textContent.trim() : ''; }"
        )

    def _is_preview_open(self) -> bool:
        if not self._page:
            return False
        try:
            preview = self._page.locator(WSP_SELECTORS["VISTA_PREVIA_MEDIA"])
            for index in range(preview.count()):
                if preview.nth(index).is_visible():
                    return True
            return False
        except Exception:
            return False

    def _attach_image(self, image_path: str) -> bool:
        if not self._page:
            return False
        if not Path(image_path).is_file():
            return False

        try:
            self._page.locator(WSP_SELECTORS["INPUT_ARCHIVO_MEDIA"]).first.set_input_files(
                image_path, timeout=5000
            )
            return True
        except Exception:
            pass

        try:
            self._page.locator(WSP_SELECTORS["BOTON_ADJUNTAR"]).first.click(timeout=5000)
        except Exception:
            return False
        self._human_delay(1.0, 1.8)

        try:
            with self._page.expect_file_chooser(timeout=8000) as chooser:
                self._page.locator("[role='menuitem']").filter(
                    has_text=PHOTOS_MENU
                ).last.click(timeout=5000)
            chooser.value.set_files(image_path)
            return True
        except Exception:
            pass

        try:
            self._page.locator(WSP_SELECTORS["INPUT_ARCHIVO_MEDIA"]).first.set_input_files(
                image_path, timeout=5000
            )
            return True
        except Exception:
            self._page.keyboard.press("Escape")
            return False

    def _send_current_message(self) -> bool:
        return self._click_first_visible(WSP_SELECTORS["BOTON_ENVIAR"])


PlaywrightBot = PlaywrightWhatsAppBot
