from __future__ import annotations
import logging
from pathlib import Path
from typing import Any
from PyQt6.QtGui import QIcon, QPixmap
from pathlib import Path
from PyQt6.QtCore import QObject, Qt, QThread, QTimer, pyqtSignal, pyqtSlot
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QApplication,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from app.domain.entities import Envio, EstadoEnvio
from app.domain.ports import IEnvioRepository
from app.services.message_personalization import MessagePersonalizerService
from app.services.scheduler import SchedulerService
from config.logger import logger
from config.settings import settings



COLOR_SURFACE = "#faf9ff"
COLOR_SURFACE_DIM = "#ccdaff"
COLOR_SURFACE_BRIGHT = "#faf9ff"
COLOR_SURFACE_LOWEST = "#ffffff"
COLOR_SURFACE_LOW = "#f1f3ff"
COLOR_SURFACE_HIGH = "#e1e8ff"
COLOR_SURFACE_HIGHEST = "#d8e2ff"
COLOR_BACKGROUND = "#faf9ff"
COLOR_SURFACE_VARIANT = "#d8e2ff"

COLOR_ON_SURFACE = "#051a3e"
COLOR_ON_SURFACE_VARIANT = "#434654"
COLOR_OUTLINE = "#737685"
COLOR_OUTLINE_VARIANT = "#c3c6d6"

COLOR_PRIMARY = "#003d9b"
COLOR_ON_PRIMARY = "#ffffff"
COLOR_PRIMARY_CONTAINER = "#0052cc"
COLOR_ON_PRIMARY_CONTAINER = "#c4d2ff"
COLOR_INVERSE_PRIMARY = "#b2c5ff"
COLOR_SURFACE_TINT = "#0c56d0"

COLOR_SECONDARY = "#535f73"
COLOR_ON_SECONDARY = "#ffffff"
COLOR_SECONDARY_CONTAINER = "#d4e0f8"

COLOR_ERROR = "#ba1a1a"
COLOR_ON_ERROR = "#ffffff"
COLOR_ERROR_CONTAINER = "#ffdad6"
COLOR_ON_ERROR_CONTAINER = "#93000a"

COLOR_SUCCESS = "#1a7d37"
COLOR_SUCCESS_CONTAINER = "#d4edda"
COLOR_WARNING = "#b45309"
COLOR_WARNING_CONTAINER = "#fff3cd"

DARK_BACKGROUND = "#0B121F"
DARK_SURFACE = "#161C27"
DARK_SURFACE_CONTAINER = "#1E2738"
DARK_SURFACE_HIGH = "#252D3D"
DARK_BORDER = "#252D3D"
DARK_ON_SURFACE = "#edf0ff"
DARK_ON_SURFACE_VARIANT = "#9ca3b8"
DARK_OUTLINE = "#3d4560"
DARK_PRIMARY = "#b2c5ff"
DARK_PRIMARY_CONTAINER = "#0040a2"
DARK_SURFACE_LOW = "#131924"
DARK_SURFACE_LOWEST = "#0E1520"

SPACING_XS = 4
SPACING_SM = 8
SPACING_MD = 16
SPACING_LG = 24
SPACING_XL = 32

FONT_STACK = '"Inter", "Segoe UI", "Helvetica Neue", Arial, sans-serif'
FONT_MONO_STACK = '"JetBrains Mono", "Cascadia Code", "Consolas", monospace'
FONT_SIZE_XS = 11
FONT_SIZE_SM = 12
FONT_SIZE_MD = 14
FONT_SIZE_LG = 16
FONT_SIZE_XL = 20
FONT_SIZE_2XL = 24
FONT_SIZE_3XL = 32

RADIUS_SM = 4
RADIUS_DEFAULT = 8
RADIUS_MD = 12
RADIUS_LG = 16

SIDEBAR_WIDTH = 240
TOPBAR_HEIGHT = 64
TABLE_ROW_HEIGHT = 40


def get_light_qss() -> str:
    return f"""
    * {{
        margin: 0;
        padding: 0;
        font-family: {FONT_STACK};
        font-size: {FONT_SIZE_MD}px;
        color: {COLOR_ON_SURFACE};
    }}

    QMainWindow {{
        background-color: {COLOR_BACKGROUND};
    }}

    QWidget {{
        background-color: transparent;
    }}

    QScrollBar:vertical {{
        background: transparent;
        width: 6px;
        margin: 0;
    }}
    QScrollBar::handle:vertical {{
        background: {COLOR_OUTLINE_VARIANT};
        border-radius: 3px;
        min-height: 30px;
    }}
    QScrollBar::handle:vertical:hover {{
        background: {COLOR_OUTLINE};
    }}
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical,
    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
        background: none;
        height: 0;
    }}

    QPushButton {{
        background-color: {COLOR_SURFACE_LOWEST};
        color: {COLOR_ON_SURFACE};
        border: 1px solid {COLOR_OUTLINE_VARIANT};
        border-radius: {RADIUS_DEFAULT}px;
        padding: {SPACING_SM}px {SPACING_MD}px;
        font-size: {FONT_SIZE_MD}px;
        font-weight: 600;
        min-height: 24px;
    }}
    QPushButton:hover {{
        background-color: {COLOR_SURFACE_LOW};
        border-color: {COLOR_OUTLINE};
    }}
    QPushButton:pressed {{
        background-color: {COLOR_SURFACE_HIGH};
    }}
    QPushButton:disabled {{
        background-color: {COLOR_SURFACE_LOW};
        color: {COLOR_OUTLINE};
        border-color: {COLOR_OUTLINE_VARIANT};
    }}

    QPushButton[class="primary"] {{
        background-color: {COLOR_PRIMARY};
        color: {COLOR_ON_PRIMARY};
        border: none;
    }}
    QPushButton[class="primary"]:hover {{
        background-color: {COLOR_PRIMARY_CONTAINER};
    }}
    QPushButton[class="primary"]:pressed {{
        background-color: {COLOR_SURFACE_TINT};
    }}
    QPushButton[class="primary"]:disabled {{
        background-color: {COLOR_OUTLINE_VARIANT};
        color: {COLOR_OUTLINE};
    }}

    QPushButton[class="ghost"] {{
        background-color: transparent;
        color: {COLOR_PRIMARY};
        border: 1px solid {COLOR_PRIMARY};
    }}
    QPushButton[class="ghost"]:hover {{
        background-color: {COLOR_SURFACE_LOW};
    }}
    QPushButton[class="ghost"]:pressed {{
        background-color: {COLOR_SURFACE_HIGH};
    }}
    QPushButton[class="ghost"]:disabled {{
        background-color: transparent;
        color: {COLOR_OUTLINE};
        border-color: {COLOR_OUTLINE_VARIANT};
    }}

    QLineEdit, QTextEdit {{
        background-color: {COLOR_SURFACE_LOWEST};
        color: {COLOR_ON_SURFACE};
        border: 1px solid {COLOR_OUTLINE_VARIANT};
        border-radius: {RADIUS_DEFAULT}px;
        padding: {SPACING_SM}px {SPACING_MD}px;
        font-size: {FONT_SIZE_MD}px;
    }}
    QLineEdit:focus, QTextEdit:focus {{
        border: 2px solid {COLOR_PRIMARY};
        padding: {SPACING_SM - 1}px {SPACING_MD - 1}px;
    }}
    QLineEdit:disabled, QTextEdit:disabled {{
        background-color: {COLOR_SURFACE_LOW};
        color: {COLOR_OUTLINE};
    }}

    #consoleLogs {{
        font-family: {FONT_MONO_STACK};
        font-size: {FONT_SIZE_SM}px;
        background-color: #0b121f;
        color: #d1d5db;
        border: 1px solid {COLOR_OUTLINE_VARIANT};
        border-radius: {RADIUS_DEFAULT}px;
        padding: {SPACING_SM}px;
    }}

    QTableWidget {{
        background-color: {COLOR_SURFACE_LOWEST};
        color: {COLOR_ON_SURFACE};
        border: 1px solid {COLOR_OUTLINE_VARIANT};
        border-radius: {RADIUS_MD}px;
        gridline-color: {COLOR_OUTLINE_VARIANT};
        selection-background-color: {COLOR_SURFACE_HIGHEST};
        selection-color: {COLOR_ON_SURFACE};
        alternate-background-color: {COLOR_SURFACE_LOW};
        font-size: {FONT_SIZE_SM}px;
    }}
    QTableWidget::item {{
        padding: {SPACING_XS}px {SPACING_SM}px;
        border-bottom: 1px solid {COLOR_OUTLINE_VARIANT};
    }}
    QHeaderView::section {{
        background-color: {COLOR_SURFACE_LOW};
        color: {COLOR_ON_SURFACE_VARIANT};
        border: none;
        border-bottom: 2px solid {COLOR_OUTLINE_VARIANT};
        padding: {SPACING_SM}px;
        font-size: {FONT_SIZE_XS}px;
        font-weight: 600;
        text-transform: uppercase;
    }}

    #sidebar {{
        background-color: {COLOR_SURFACE_LOWEST};
        border-right: 1px solid {COLOR_OUTLINE_VARIANT};
        min-width: {SIDEBAR_WIDTH}px;
        max-width: {SIDEBAR_WIDTH}px;
    }}
    #sidebarTitle {{
        font-size: {FONT_SIZE_LG}px;
        font-weight: 700;
        color: {COLOR_PRIMARY};
        padding: {SPACING_MD}px;
    }}
    #sidebarSection {{
        font-size: {FONT_SIZE_XS}px;
        font-weight: 600;
        color: {COLOR_OUTLINE};
        padding: {SPACING_MD}px {SPACING_MD}px {SPACING_XS}px {SPACING_MD}px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }}
    #sidebarNavItem {{
        background-color: transparent;
        color: {COLOR_ON_SURFACE_VARIANT};
        border: none;
        border-radius: {RADIUS_DEFAULT}px;
        padding: {SPACING_SM}px {SPACING_MD}px;
        text-align: left;
        font-size: {FONT_SIZE_MD}px;
        font-weight: 500;
        min-height: 36px;
    }}
    #sidebarNavItem:hover {{
        background-color: {COLOR_SURFACE_LOW};
        color: {COLOR_ON_SURFACE};
    }}
    #sidebarNavItem[active="true"] {{
        background-color: {COLOR_SURFACE_HIGH};
        color: {COLOR_PRIMARY};
        font-weight: 600;
    }}

    #topBar {{
        background-color: {COLOR_SURFACE_LOWEST};
        border-bottom: 1px solid {COLOR_OUTLINE_VARIANT};
        min-height: {TOPBAR_HEIGHT}px;
        max-height: {TOPBAR_HEIGHT}px;
        padding: 0 {SPACING_LG}px;
    }}
    #topBarTitle {{
        font-size: {FONT_SIZE_XL}px;
        font-weight: 700;
        color: {COLOR_ON_SURFACE};
    }}
    #topBarStatus {{
        font-size: {FONT_SIZE_SM}px;
        font-weight: 600;
        color: {COLOR_ON_SURFACE_VARIANT};
        padding: {SPACING_XS}px {SPACING_SM}px;
        background-color: {COLOR_SURFACE_LOW};
        border-radius: {RADIUS_SM}px;
    }}

    #card {{
        background-color: {COLOR_SURFACE_LOWEST};
        border: 1px solid {COLOR_OUTLINE_VARIANT};
        border-radius: {RADIUS_MD}px;
        padding: {SPACING_MD}px;
    }}
    #statValue {{
        font-size: {FONT_SIZE_2XL}px;
        font-weight: 700;
        color: {COLOR_ON_SURFACE};
    }}
    #statLabel {{
        font-size: {FONT_SIZE_XS}px;
        font-weight: 600;
        color: {COLOR_ON_SURFACE_VARIANT};
        text-transform: uppercase;
    }}
    """


def get_dark_qss() -> str:
    return f"""
    * {{
        margin: 0;
        padding: 0;
        font-family: {FONT_STACK};
        font-size: {FONT_SIZE_MD}px;
        color: {DARK_ON_SURFACE};
    }}

    QMainWindow {{
        background-color: {DARK_BACKGROUND};
    }}

    QWidget {{
        background-color: transparent;
    }}

    QScrollBar:vertical {{
        background: transparent;
        width: 6px;
        margin: 0;
    }}
    QScrollBar::handle:vertical {{
        background: {DARK_OUTLINE};
        border-radius: 3px;
        min-height: 30px;
    }}
    QScrollBar::handle:vertical:hover {{
        background: {DARK_ON_SURFACE_VARIANT};
    }}
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical,
    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
        background: none;
        height: 0;
    }}

    QPushButton {{
        background-color: {DARK_SURFACE_CONTAINER};
        color: {DARK_ON_SURFACE};
        border: 1px solid {DARK_BORDER};
        border-radius: {RADIUS_DEFAULT}px;
        padding: {SPACING_SM}px {SPACING_MD}px;
        font-size: {FONT_SIZE_MD}px;
        font-weight: 600;
        min-height: 24px;
    }}
    QPushButton:hover {{
        background-color: {DARK_SURFACE_HIGH};
        border-color: {DARK_OUTLINE};
    }}
    QPushButton:pressed {{
        background-color: {DARK_SURFACE};
    }}
    QPushButton:disabled {{
        background-color: {DARK_SURFACE};
        color: {DARK_OUTLINE};
        border-color: {DARK_BORDER};
    }}

    QPushButton[class="primary"] {{
        background-color: {DARK_PRIMARY_CONTAINER};
        color: #ffffff;
        border: none;
    }}
    QPushButton[class="primary"]:hover {{
        background-color: #0052cc;
    }}
    QPushButton[class="primary"]:pressed {{
        background-color: #003d9b;
    }}
    QPushButton[class="primary"]:disabled {{
        background-color: {DARK_SURFACE_HIGH};
        color: {DARK_OUTLINE};
    }}

    QPushButton[class="ghost"] {{
        background-color: transparent;
        color: {DARK_PRIMARY};
        border: 1px solid {DARK_PRIMARY};
    }}
    QPushButton[class="ghost"]:hover {{
        background-color: {DARK_SURFACE_HIGH};
    }}
    QPushButton[class="ghost"]:pressed {{
        background-color: {DARK_SURFACE};
    }}
    QPushButton[class="ghost"]:disabled {{
        background-color: transparent;
        color: {DARK_OUTLINE};
        border-color: {DARK_BORDER};
    }}

    QLineEdit, QTextEdit {{
        background-color: {DARK_SURFACE};
        color: {DARK_ON_SURFACE};
        border: 1px solid {DARK_BORDER};
        border-radius: {RADIUS_DEFAULT}px;
        padding: {SPACING_SM}px {SPACING_MD}px;
        font-size: {FONT_SIZE_MD}px;
    }}
    QLineEdit:focus, QTextEdit:focus {{
        border: 2px solid {DARK_PRIMARY};
        padding: {SPACING_SM - 1}px {SPACING_MD - 1}px;
    }}
    QLineEdit:disabled, QTextEdit:disabled {{
        background-color: {DARK_SURFACE_LOWEST};
        color: {DARK_OUTLINE};
    }}

    #consoleLogs {{
        font-family: {FONT_MONO_STACK};
        font-size: {FONT_SIZE_SM}px;
        background-color: {DARK_SURFACE_LOWEST};
        color: #9ca3b8;
        border: 1px solid {DARK_BORDER};
        border-radius: {RADIUS_DEFAULT}px;
        padding: {SPACING_SM}px;
    }}

    QTableWidget {{
        background-color: {DARK_SURFACE};
        color: {DARK_ON_SURFACE};
        border: 1px solid {DARK_BORDER};
        border-radius: {RADIUS_MD}px;
        gridline-color: {DARK_BORDER};
        selection-background-color: {DARK_SURFACE_HIGH};
        selection-color: {DARK_ON_SURFACE};
        alternate-background-color: {DARK_SURFACE_LOW};
        font-size: {FONT_SIZE_SM}px;
    }}
    QTableWidget::item {{
        padding: {SPACING_XS}px {SPACING_SM}px;
        border-bottom: 1px solid {DARK_BORDER};
    }}
    QHeaderView::section {{
        background-color: {DARK_SURFACE_CONTAINER};
        color: {DARK_ON_SURFACE_VARIANT};
        border: none;
        border-bottom: 2px solid {DARK_BORDER};
        padding: {SPACING_SM}px;
        font-size: {FONT_SIZE_XS}px;
        font-weight: 600;
        text-transform: uppercase;
    }}

    #sidebar {{
        background-color: {DARK_SURFACE_CONTAINER};
        border-right: 1px solid {DARK_BORDER};
        min-width: {SIDEBAR_WIDTH}px;
        max-width: {SIDEBAR_WIDTH}px;
    }}
    #sidebarTitle {{
        font-size: {FONT_SIZE_LG}px;
        font-weight: 700;
        color: {DARK_PRIMARY};
        padding: {SPACING_MD}px;
    }}
    #sidebarSection {{
        font-size: {FONT_SIZE_XS}px;
        font-weight: 600;
        color: {DARK_OUTLINE};
        padding: {SPACING_MD}px {SPACING_MD}px {SPACING_XS}px {SPACING_MD}px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }}
    #sidebarNavItem {{
        background-color: transparent;
        color: {DARK_ON_SURFACE_VARIANT};
        border: none;
        border-radius: {RADIUS_DEFAULT}px;
        padding: {SPACING_SM}px {SPACING_MD}px;
        text-align: left;
        font-size: {FONT_SIZE_MD}px;
        font-weight: 500;
        min-height: 36px;
    }}
    #sidebarNavItem:hover {{
        background-color: {DARK_SURFACE_HIGH};
        color: {DARK_ON_SURFACE};
    }}
    #sidebarNavItem[active="true"] {{
        background-color: {DARK_SURFACE_HIGH};
        color: {DARK_PRIMARY};
        font-weight: 600;
    }}

    #topBar {{
        background-color: {DARK_SURFACE_CONTAINER};
        border-bottom: 1px solid {DARK_BORDER};
        min-height: {TOPBAR_HEIGHT}px;
        max-height: {TOPBAR_HEIGHT}px;
        padding: 0 {SPACING_LG}px;
    }}
    #topBarTitle {{
        font-size: {FONT_SIZE_XL}px;
        font-weight: 700;
        color: {DARK_ON_SURFACE};
    }}
    #topBarStatus {{
        font-size: {FONT_SIZE_SM}px;
        font-weight: 600;
        color: {DARK_ON_SURFACE_VARIANT};
        padding: {SPACING_XS}px {SPACING_SM}px;
        background-color: {DARK_SURFACE};
        border-radius: {RADIUS_SM}px;
    }}

    #card {{
        background-color: {DARK_SURFACE_CONTAINER};
        border: 1px solid {DARK_BORDER};
        border-radius: {RADIUS_MD}px;
        padding: {SPACING_MD}px;
    }}
    #statValue {{
        font-size: {FONT_SIZE_2XL}px;
        font-weight: 700;
        color: {DARK_ON_SURFACE};
    }}
    #statLabel {{
        font-size: {FONT_SIZE_XS}px;
        font-weight: 600;
        color: {DARK_ON_SURFACE_VARIANT};
        text-transform: uppercase;
    }}
    """


class ThemeManager(QObject):
    theme_changed = pyqtSignal(str)

    def __init__(self, app: QApplication) -> None:
        super().__init__()
        self._app = app
        self._current_theme = "light"

    @property
    def current_theme(self) -> str:
        return self._current_theme

    @property
    def is_dark(self) -> bool:
        return self._current_theme == "dark"

    def apply_theme(self, theme: str) -> None:
        if theme == "dark":
            self._app.setStyleSheet(get_dark_qss())
        else:
            self._app.setStyleSheet(get_light_qss())
        self._current_theme = theme
        self.theme_changed.emit(theme)

    def toggle(self) -> None:
        new_theme = "dark" if self._current_theme == "light" else "light"
        self.apply_theme(new_theme)


class QtLogBridge(QObject, logging.Handler):
    log_signal = pyqtSignal(str)

    def __init__(self) -> None:
        QObject.__init__(self)
        logging.Handler.__init__(self)
        self.setFormatter(
            logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s", "%H:%M:%S")
        )

    def emit(self, record: logging.LogRecord) -> None:
        try:
            msg = self.format(record)
            self.log_signal.emit(msg)
        except Exception:
            self.handleError(record)


class EnvioWorker(QThread):
    progreso_signal = pyqtSignal(str)
    finalizado_signal = pyqtSignal(str)
    error_signal = pyqtSignal(str)

    def __init__(
        self,
        scheduler: SchedulerService,
        personalizador: MessagePersonalizerService,
        parent: QObject | None = None,
    ) -> None:
        super().__init__(parent)
        self.scheduler = scheduler
        self.personalizador = personalizador

    def run(self) -> None:
        try:
            self.progreso_signal.emit("Iniciando despacho diario de mensajes...")
            resumen = self.scheduler.ejecutar_envios_del_dia(self.personalizador)
            self.finalizado_signal.emit(resumen)
        except Exception as exc:
            self.error_signal.emit(str(exc))


class StatCardWidget(QWidget):
    def __init__(self, label: str, value: str = "0", parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("card")
        self.setMinimumWidth(180)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(SPACING_MD, SPACING_MD, SPACING_MD, SPACING_MD)
        layout.setSpacing(SPACING_XS)

        self._lbl_label = QLabel(label)
        self._lbl_label.setObjectName("statLabel")

        self._lbl_value = QLabel(value)
        self._lbl_value.setObjectName("statValue")

        layout.addWidget(self._lbl_label)
        layout.addWidget(self._lbl_value)

    def set_value(self, value: str) -> None:
        self._lbl_value.setText(value)


class MainWindow(QMainWindow):
    def __init__(
        self,
        scheduler: SchedulerService,
        personalizador: MessagePersonalizerService,
        envio_repo: IEnvioRepository,
        theme_manager: ThemeManager | None = None,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        
        from PyQt6.QtGui import QIcon, QPixmap
        from PyQt6.QtCore import Qt
        from pathlib import Path
        
        ruta_logo_real = Path(r"C:\Users\brown\OneDrive\Desktop\lsqraa\Isra Trabajo\trinity-logo.jpg")
        if ruta_logo_real.is_file():
            pixmap = QPixmap(str(ruta_logo_real)).scaled(
                256, 256, 
                Qt.AspectRatioMode.KeepAspectRatio, 
                Qt.TransformationMode.SmoothTransformation
            )
            self.setWindowIcon(QIcon(pixmap))

        self.scheduler = scheduler
        self.personalizador = personalizador
        self.envio_repo = envio_repo
        self.theme_manager = theme_manager

        self._worker: EnvioWorker | None = None
        self._log_bridge = QtLogBridge()
        self._log_bridge.log_signal.connect(self._append_log)
        logger.addHandler(self._log_bridge)

        self.setWindowTitle("Trinity - Control de Prospección WhatsApp")
        self.setMinimumSize(1100, 720)
        self.resize(1200, 800)

        self._init_ui()
        self.refresh_data()

        self._cuota_timer = QTimer(self)
        self._cuota_timer.setInterval(5 * 60 * 1000)
        self._cuota_timer.timeout.connect(self.actualizar_estado_cuota)
        self._cuota_timer.start()

    def _init_ui(self) -> None:
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self._build_sidebar(main_layout)

        content_area = QWidget()
        content_layout = QVBoxLayout(content_area)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        self._build_topbar(content_layout)
        self._build_body(content_layout)

        main_layout.addWidget(content_area)

    def _build_sidebar(self, parent_layout: QHBoxLayout) -> None:
        sidebar = QWidget()
        sidebar.setObjectName("sidebar")
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(SPACING_SM, SPACING_MD, SPACING_SM, SPACING_MD)
        layout.setSpacing(SPACING_XS)

        title = QLabel("TRINITY")
        title.setObjectName("sidebarTitle")
        layout.addWidget(title)

        sec_ops = QLabel("OPERACIONES")
        sec_ops.setObjectName("sidebarSection")
        layout.addWidget(sec_ops)

        self.nav_dashboard = QPushButton("Panel de Control")
        self.nav_dashboard.setObjectName("sidebarNavItem")
        self.nav_dashboard.setProperty("active", "true")
        self.nav_dashboard.setCursor(Qt.CursorShape.PointingHandCursor)
        layout.addWidget(self.nav_dashboard)

        layout.addStretch()

        sec_sys = QLabel("SISTEMA ON-PREMISE")
        sec_sys.setObjectName("sidebarSection")
        layout.addWidget(sec_sys)

        lbl_version = QLabel("v1.0.0 - Sep 2026")
        lbl_version.setObjectName("statLabel")
        lbl_version.setStyleSheet(f"padding-left: {SPACING_MD}px;")
        layout.addWidget(lbl_version)

        parent_layout.addWidget(sidebar)

    def _build_topbar(self, parent_layout: QVBoxLayout) -> None:
        topbar = QWidget()
        topbar.setObjectName("topBar")
        layout = QHBoxLayout(topbar)
        layout.setContentsMargins(SPACING_LG, 0, SPACING_LG, 0)
        layout.setSpacing(SPACING_MD)

        title = QLabel("Campaña de WhatsApp")
        title.setObjectName("topBarTitle")
        layout.addWidget(title)

        layout.addStretch()

        self.lbl_status = QLabel("Listo")
        self.lbl_status.setObjectName("topBarStatus")
        layout.addWidget(self.lbl_status)

        self.btn_theme = QPushButton("Tema")
        self.btn_theme.setProperty("class", "ghost")
        self.btn_theme.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_theme.clicked.connect(self._toggle_theme)
        layout.addWidget(self.btn_theme)

        parent_layout.addWidget(topbar)

    def _build_body(self, parent_layout: QVBoxLayout) -> None:
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        body_widget = QWidget()
        body_layout = QVBoxLayout(body_widget)
        body_layout.setContentsMargins(SPACING_LG, SPACING_LG, SPACING_LG, SPACING_LG)
        body_layout.setSpacing(SPACING_MD)

        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(SPACING_MD)

        self.card_cuota = StatCardWidget("Enviados Hoy (Cuota)")
        self.card_pendientes = StatCardWidget("Pendientes en Cola")
        self.card_total = StatCardWidget("Total Contactos")
        self.card_fallidos = StatCardWidget("Fallidos")

        stats_layout.addWidget(self.card_cuota)
        stats_layout.addWidget(self.card_pendientes)
        stats_layout.addWidget(self.card_total)
        stats_layout.addWidget(self.card_fallidos)
        body_layout.addLayout(stats_layout)

        actions_card = QWidget()
        actions_card.setObjectName("card")
        actions_layout = QHBoxLayout(actions_card)
        actions_layout.setContentsMargins(SPACING_MD, SPACING_MD, SPACING_MD, SPACING_MD)
        actions_layout.setSpacing(SPACING_MD)

        self.btn_cargar_excel = QPushButton("Cargar Archivo Excel")
        self.btn_cargar_excel.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_cargar_excel.clicked.connect(self._on_cargar_excel)

        self.btn_iniciar = QPushButton("Iniciar Campaña Diaria")
        self.btn_iniciar.setProperty("class", "primary")
        self.btn_iniciar.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_iniciar.clicked.connect(self._on_iniciar_campana)

        self.btn_refrescar = QPushButton("Actualizar Métricas")
        self.btn_refrescar.setProperty("class", "ghost")
        self.btn_refrescar.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_refrescar.clicked.connect(self.refresh_data)

        actions_layout.addWidget(self.btn_cargar_excel)
        actions_layout.addWidget(self.btn_iniciar)
        actions_layout.addWidget(self.btn_refrescar)
        actions_layout.addStretch()

        body_layout.addWidget(actions_card)

        content_split = QHBoxLayout()
        content_split.setSpacing(SPACING_MD)

        table_container = QWidget()
        table_container.setObjectName("card")
        table_layout = QVBoxLayout(table_container)
        table_layout.setContentsMargins(SPACING_MD, SPACING_MD, SPACING_MD, SPACING_MD)
        table_layout.setSpacing(SPACING_SM)

        table_header = QLabel("Próximos Envíos en Cola")
        table_header.setStyleSheet("font-weight: 700; font-size: 15px;")
        table_layout.addWidget(table_header)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Teléfono", "Asesor", "Nombre", "Estado"])
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(False)
        self.table.verticalHeader().setDefaultSectionSize(TABLE_ROW_HEIGHT)

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)

        table_layout.addWidget(self.table)
        content_split.addWidget(table_container, 3)

        console_container = QWidget()
        console_container.setObjectName("card")
        console_layout = QVBoxLayout(console_container)
        console_layout.setContentsMargins(SPACING_MD, SPACING_MD, SPACING_MD, SPACING_MD)
        console_layout.setSpacing(SPACING_SM)

        console_header = QLabel("Consola de Eventos")
        console_header.setStyleSheet("font-weight: 700; font-size: 15px;")
        console_layout.addWidget(console_header)

        self.console = QTextEdit()
        self.console.setObjectName("consoleLogs")
        self.console.setReadOnly(True)
        console_layout.addWidget(self.console)

        content_split.addWidget(console_container, 2)
        body_layout.addLayout(content_split)

        scroll.setWidget(body_widget)
        parent_layout.addWidget(scroll)

    def _set_ui_busy(self, is_busy: bool) -> None:
        self.btn_cargar_excel.setEnabled(not is_busy)
        self.btn_refrescar.setEnabled(not is_busy)
        self.lbl_status.setText("Enviando mensajes..." if is_busy else "Listo")
        if is_busy:
            self.btn_iniciar.setEnabled(False)
        else:
            self.actualizar_estado_cuota()

    @pyqtSlot()
    def _on_cargar_excel(self) -> None:
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar archivo de campaña Excel",
            "",
            "Archivos Excel (*.xlsx *.xls)",
        )
        if not file_path:
            return

        try:
            nuevos = self.scheduler.importar_campana_desde_excel(file_path)
            self.refresh_data()
            if nuevos > 0:
                QMessageBox.information(
                    self,
                    "Importación Exitosa",
                    f"Se procesó el archivo correctamente.\nNuevos envíos añadidos a la cola: {nuevos}",
                )
            else:
                QMessageBox.warning(
                    self,
                    "Importación Sin Nuevos Registros",
                    "No se agregaron nuevos registros. Es posible que los números ya existan en la base de datos o el archivo no contenga filas válidas.",
                )
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error al Importar",
                f"Ocurrió un error al procesar el archivo Excel:\n{e}",
            )

    @pyqtSlot()
    def _on_iniciar_campana(self) -> None:
        if self._worker and self._worker.isRunning():
            return

        self._set_ui_busy(True)
        self._append_log("Preparando ejecución de campaña...")

        self._worker = EnvioWorker(self.scheduler, self.personalizador, self)
        self._worker.progreso_signal.connect(self._append_log)
        self._worker.finalizado_signal.connect(self._on_campana_finalizada)
        self._worker.error_signal.connect(self._on_campana_error)
        self._worker.finished.connect(lambda: self._set_ui_busy(False))
        self._worker.start()

    @pyqtSlot(str)
    def _on_campana_finalizada(self, resumen: str) -> None:
        self._append_log(f"Jornada finalizada: {resumen}")
        self.refresh_data()
        QMessageBox.information(self, "Campaña Finalizada", resumen)

    @pyqtSlot(str)
    def _on_campana_error(self, error_msg: str) -> None:
        self._append_log(f"Error crítico en campaña: {error_msg}")
        self.refresh_data()
        QMessageBox.critical(
            self,
            "Error en Campaña",
            f"Ocurrió un fallo durante la ejecución:\n{error_msg}",
        )

    @pyqtSlot(str)
    def _append_log(self, text: str) -> None:
        self.console.append(text)
        scrollbar = self.console.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    @pyqtSlot()
    def _toggle_theme(self) -> None:
        if self.theme_manager:
            self.theme_manager.toggle()

    @pyqtSlot()
    def actualizar_estado_cuota(self) -> None:
        envios_hoy = self.envio_repo.get_envios_hoy_count()
        limite = settings.DAILY_MESSAGE_LIMIT
        if envios_hoy >= limite:
            self.btn_iniciar.setEnabled(False)
            self.btn_iniciar.setText(f"Cuota Diaria Completada ({limite}/{limite})")
        else:
            if not (self._worker and self._worker.isRunning()):
                self.btn_iniciar.setEnabled(True)
                self.btn_iniciar.setText("Iniciar Campaña Diaria")

    def refresh_data(self) -> None:
        stats = self.envio_repo.get_stats()
        envios_hoy = self.envio_repo.get_envios_hoy_count()
        limite = settings.DAILY_MESSAGE_LIMIT

        self.card_cuota.set_value(f"{envios_hoy} / {limite}")
        self.card_pendientes.set_value(str(stats["pendientes"]))
        self.card_total.set_value(str(stats["total"]))
        self.card_fallidos.set_value(str(stats["fallidos"]))

        pendientes = self.envio_repo.get_next_pendientes(limit=50)
        self._populate_table(pendientes)
        self.actualizar_estado_cuota()

    def _populate_table(self, envios: list[Envio]) -> None:
        self.table.setRowCount(len(envios))
        for row_idx, envio in enumerate(envios):
            cliente = envio.cliente
            item_tel = QTableWidgetItem(cliente.telefono)
            item_ase = QTableWidgetItem(cliente.asesor_nombre)
            item_nom = QTableWidgetItem(cliente.nombre or "-")
            item_est = QTableWidgetItem(envio.estado.value)

            for item in (item_tel, item_ase, item_nom, item_est):
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)

            self.table.setItem(row_idx, 0, item_tel)
            self.table.setItem(row_idx, 1, item_ase)
            self.table.setItem(row_idx, 2, item_nom)
            self.table.setItem(row_idx, 3, item_est)

    def closeEvent(self, event: Any) -> None:
        if self._worker and self._worker.isRunning():
            reply = QMessageBox.question(
                self,
                "Confirmar Cierre",
                "Hay una campaña en ejecución. ¿Deseas detenerla y salir?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No,
            )
            if reply == QMessageBox.StandardButton.Yes:
                self._worker.terminate()
                self._worker.wait(3000)
                event.accept()
            else:
                event.ignore()
                return
        event.accept()
