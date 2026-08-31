from __future__ import annotations
import logging
from pathlib import Path
from typing import Any

from PyQt6.QtCore import QObject, Qt, QThread, QTimer, pyqtSignal, pyqtSlot
from PyQt6.QtGui import QDragEnterEvent, QDropEvent, QIcon, QPixmap
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QApplication,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSizePolicy,
    QStackedWidget,
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

COLOR_BACKGROUND = "#09090b"
COLOR_SURFACE = "#18181b"
COLOR_SURFACE_HOVER = "#27272a"
COLOR_PRIMARY = "#2463eb"
COLOR_PRIMARY_HOVER = "#1d4ed8"
COLOR_BORDER = "#3f3f46"
COLOR_TEXT = "#f4f4f5"
COLOR_MUTED = "#a1a1aa"
COLOR_ACCENT = "#10b981"
COLOR_ZEBRA = "#111113"

FONT_STACK = '"Inter", "Segoe UI", "Helvetica Neue", Arial, sans-serif'
FONT_MONO_STACK = '"JetBrains Mono", "Cascadia Code", "Consolas", monospace'
FONT_HEADING_STACK = '"Space Grotesk", "Inter", sans-serif'


def get_monolith_qss() -> str:
    return f"""
    * {{
        margin: 0;
        padding: 0;
        font-family: {FONT_STACK};
        font-size: 13px;
        color: {COLOR_TEXT};
    }}

    QMainWindow {{
        background-color: {COLOR_BACKGROUND};
    }}

    QWidget {{
        background-color: transparent;
    }}

    #topHeader {{
        background-color: {COLOR_SURFACE};
        border-bottom: 1px solid {COLOR_BORDER};
        min-height: 48px;
        max-height: 48px;
        padding: 0 20px;
    }}

    #appTitle {{
        font-family: {FONT_HEADING_STACK};
        font-size: 16px;
        font-weight: 700;
        color: {COLOR_TEXT};
        letter-spacing: 0.5px;
    }}

    #controlsBar {{
        background-color: {COLOR_BACKGROUND};
        border-bottom: 1px solid {COLOR_BORDER};
        min-height: 56px;
        max-height: 56px;
        padding: 0 20px;
    }}

    #statusBar {{
        background-color: {COLOR_SURFACE};
        border-top: 1px solid {COLOR_BORDER};
        min-height: 32px;
        max-height: 32px;
        padding: 0 20px;
    }}

    #metaPill {{
        background-color: {COLOR_SURFACE};
        border: 1px solid {COLOR_BORDER};
        padding: 4px 12px;
        font-family: {FONT_MONO_STACK};
        font-size: 11px;
        color: {COLOR_MUTED};
        border-radius: 0px;
    }}

    #dropzoneContainer {{
        background-color: {COLOR_SURFACE};
        border: 2px dashed {COLOR_BORDER};
        border-radius: 2px;
    }}
    #dropzoneContainer[dragActive="true"] {{
        border: 2px solid {COLOR_PRIMARY};
        background-color: rgba(36, 99, 235, 0.08);
    }}

    QPushButton {{
        background-color: {COLOR_SURFACE};
        color: {COLOR_TEXT};
        border: 1px solid {COLOR_BORDER};
        border-radius: 0px;
        padding: 6px 14px;
        font-size: 13px;
        font-weight: 500;
        min-height: 28px;
    }}
    QPushButton:hover {{
        background-color: {COLOR_SURFACE_HOVER};
        border-color: {COLOR_MUTED};
    }}
    QPushButton:pressed {{
        background-color: {COLOR_BACKGROUND};
    }}
    QPushButton:disabled {{
        background-color: {COLOR_SURFACE};
        color: #52525b;
        border-color: #27272a;
    }}

    QPushButton[class="primary"] {{
        background-color: {COLOR_PRIMARY};
        color: #ffffff;
        border: none;
        font-weight: 600;
    }}
    QPushButton[class="primary"]:hover {{
        background-color: {COLOR_PRIMARY_HOVER};
    }}
    QPushButton[class="primary"]:pressed {{
        background-color: #1e40af;
    }}
    QPushButton[class="primary"]:disabled {{
        background-color: #27272a;
        color: #52525b;
    }}

    QPushButton[class="ghost"] {{
        background-color: transparent;
        color: {COLOR_MUTED};
        border: 1px solid {COLOR_BORDER};
    }}
    QPushButton[class="ghost"]:hover {{
        background-color: {COLOR_SURFACE_HOVER};
        color: {COLOR_TEXT};
    }}
    QPushButton[class="ghost"]:pressed {{
        background-color: {COLOR_SURFACE};
    }}

    QTableWidget {{
        background-color: {COLOR_BACKGROUND};
        color: {COLOR_TEXT};
        border: 1px solid {COLOR_BORDER};
        border-radius: 0px;
        gridline-color: rgba(63, 63, 70, 0.4);
        selection-background-color: {COLOR_SURFACE_HOVER};
        selection-color: {COLOR_TEXT};
        alternate-background-color: {COLOR_ZEBRA};
        font-family: {FONT_MONO_STACK};
        font-size: 12px;
    }}
    QTableWidget::item {{
        padding: 4px 12px;
        border-bottom: 1px solid rgba(63, 63, 70, 0.4);
    }}
    QHeaderView::section {{
        background-color: {COLOR_SURFACE};
        color: {COLOR_TEXT};
        border: none;
        border-bottom: 1px solid {COLOR_BORDER};
        border-right: 1px solid {COLOR_BORDER};
        padding: 8px 12px;
        font-family: {FONT_STACK};
        font-size: 12px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}

    #consoleLogs {{
        font-family: {FONT_MONO_STACK};
        font-size: 12px;
        background-color: {COLOR_BACKGROUND};
        color: {COLOR_TEXT};
        border: 1px solid {COLOR_BORDER};
        border-radius: 0px;
        padding: 10px;
    }}

    QScrollBar:vertical {{
        background: {COLOR_BACKGROUND};
        width: 8px;
        margin: 0;
        border-left: 1px solid {COLOR_BORDER};
    }}
    QScrollBar::handle:vertical {{
        background: {COLOR_BORDER};
        min-height: 24px;
    }}
    QScrollBar::handle:vertical:hover {{
        background: {COLOR_MUTED};
    }}
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical,
    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
        background: none;
        height: 0;
    }}
    """


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


class DropzoneWidget(QFrame):
    file_selected = pyqtSignal(str)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("dropzoneContainer")
        self.setAcceptDrops(True)
        self.setFixedSize(600, 380)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 40, 32, 40)
        layout.setSpacing(16)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        icon_label = QLabel("[]")
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label.setStyleSheet(f"font-size: 36px; color: {COLOR_MUTED}; font-family: {FONT_MONO_STACK};")
        layout.addWidget(icon_label)

        self.title_label = QLabel("Arrastra y suelta archivos .xlsx o .csv aquí")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet(f"font-size: 18px; font-weight: 600; color: {COLOR_TEXT};")
        layout.addWidget(self.title_label)

        subtitle_label = QLabel("Procesamiento On-Premise seguro. Ningún dato sale de tu equipo.")
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_label.setStyleSheet(f"font-size: 13px; color: {COLOR_MUTED};")
        layout.addWidget(subtitle_label)

        layout.addSpacing(8)

        self.btn_browse = QPushButton("Examinar Archivos")
        self.btn_browse.setProperty("class", "primary")
        self.btn_browse.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_browse.setFixedSize(160, 36)
        self.btn_browse.clicked.connect(self._open_file_dialog)
        layout.addWidget(self.btn_browse, alignment=Qt.AlignmentFlag.AlignCenter)

    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if any(url.toLocalFile().lower().endswith((".xlsx", ".xls", ".csv")) for url in urls):
                self.setProperty("dragActive", "true")
                self.style().unpolish(self)
                self.style().polish(self)
                event.acceptProposedAction()
                return
        event.ignore()

    def dragLeaveEvent(self, event: Any) -> None:
        self.setProperty("dragActive", "false")
        self.style().unpolish(self)
        self.style().polish(self)
        event.accept()

    def dropEvent(self, event: QDropEvent) -> None:
        self.setProperty("dragActive", "false")
        self.style().unpolish(self)
        self.style().polish(self)

        urls = event.mimeData().urls()
        for url in urls:
            path = url.toLocalFile()
            if path.lower().endswith((".xlsx", ".xls", ".csv")):
                self.file_selected.emit(path)
                event.acceptProposedAction()
                return
        event.ignore()

    def _open_file_dialog(self) -> None:
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar archivo de campaña",
            "",
            "Archivos de Datos (*.xlsx *.xls *.csv)",
        )
        if file_path:
            self.file_selected.emit(file_path)


class UploadView(QWidget):
    file_imported = pyqtSignal(str)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Header
        header = QWidget()
        header.setObjectName("topHeader")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(20, 0, 20, 0)
        header_layout.setSpacing(12)

        logo_label = QLabel()
        logo_path = Path("data/assets/trinity-logo.jpg")
        if not logo_path.is_file():
            logo_path = Path(__file__).resolve().parent.parent / "data" / "assets" / "trinity-logo.jpg"
        if logo_path.is_file():
            pixmap = QPixmap(str(logo_path)).scaled(
                24, 24, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation
            )
            logo_label.setPixmap(pixmap)
        header_layout.addWidget(logo_label)

        title = QLabel("TRINITY | Ingesta de Campaña")
        title.setObjectName("appTitle")
        header_layout.addWidget(title)
        header_layout.addStretch()

        sys_label = QLabel("Modo On-Premise")
        sys_label.setStyleSheet(f"font-size: 11px; color: {COLOR_MUTED}; font-family: {FONT_MONO_STACK};")
        header_layout.addWidget(sys_label)

        layout.addWidget(header)

        # Center Dropzone
        center_area = QWidget()
        center_layout = QVBoxLayout(center_area)
        center_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        center_layout.setContentsMargins(24, 24, 24, 24)

        self.dropzone = DropzoneWidget()
        self.dropzone.file_selected.connect(self.file_imported.emit)
        center_layout.addWidget(self.dropzone)

        layout.addWidget(center_area)


class ProcessingDashboardView(QWidget):
    iniciar_clicked = pyqtSignal()
    cargar_otro_clicked = pyqtSignal()
    refrescar_clicked = pyqtSignal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._init_ui()

    def _init_ui(self) -> None:
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 1. Top Navigation Bar
        header = QWidget()
        header.setObjectName("topHeader")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(20, 0, 20, 0)
        header_layout.setSpacing(12)

        logo_label = QLabel()
        logo_path = Path("data/assets/trinity-logo.jpg")
        if not logo_path.is_file():
            logo_path = Path(__file__).resolve().parent.parent / "data" / "assets" / "trinity-logo.jpg"
        if logo_path.is_file():
            pixmap = QPixmap(str(logo_path)).scaled(
                24, 24, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation
            )
            logo_label.setPixmap(pixmap)
        header_layout.addWidget(logo_label)

        title = QLabel("TRINITY | Control de Prospección")
        title.setObjectName("appTitle")
        header_layout.addWidget(title)

        header_layout.addStretch()

        self.btn_cargar_otro = QPushButton("Cargar Nuevo Archivo")
        self.btn_cargar_otro.setProperty("class", "ghost")
        self.btn_cargar_otro.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_cargar_otro.clicked.connect(self.cargar_otro_clicked.emit)
        header_layout.addWidget(self.btn_cargar_otro)

        self.btn_refrescar = QPushButton("Actualizar Métricas")
        self.btn_refrescar.setProperty("class", "ghost")
        self.btn_refrescar.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_refrescar.clicked.connect(self.refrescar_clicked.emit)
        header_layout.addWidget(self.btn_refrescar)

        main_layout.addWidget(header)

        # 2. Controls & Metadata Bar
        controls = QWidget()
        controls.setObjectName("controlsBar")
        controls_layout = QHBoxLayout(controls)
        controls_layout.setContentsMargins(20, 0, 20, 0)
        controls_layout.setSpacing(16)

        self.btn_iniciar = QPushButton("Iniciar Campaña Diaria")
        self.btn_iniciar.setProperty("class", "primary")
        self.btn_iniciar.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_iniciar.clicked.connect(self.iniciar_clicked.emit)
        controls_layout.addWidget(self.btn_iniciar)

        self.lbl_status = QLabel("Listo")
        self.lbl_status.setStyleSheet(f"font-size: 12px; color: {COLOR_MUTED}; font-family: {FONT_MONO_STACK};")
        controls_layout.addWidget(self.lbl_status)

        controls_layout.addStretch()

        self.pill_cuota = QLabel("Cuota Hoy: 0 / 45")
        self.pill_cuota.setObjectName("metaPill")
        controls_layout.addWidget(self.pill_cuota)

        self.pill_pendientes = QLabel("Pendientes: 0")
        self.pill_pendientes.setObjectName("metaPill")
        controls_layout.addWidget(self.pill_pendientes)

        self.pill_total = QLabel("Total: 0")
        self.pill_total.setObjectName("metaPill")
        controls_layout.addWidget(self.pill_total)

        self.pill_fallidos = QLabel("Fallidos: 0")
        self.pill_fallidos.setObjectName("metaPill")
        controls_layout.addWidget(self.pill_fallidos)

        main_layout.addWidget(controls)

        # 3. Main Split View: Table (Left) + Live Event Console (Right)
        split_widget = QWidget()
        split_layout = QHBoxLayout(split_widget)
        split_layout.setContentsMargins(20, 16, 20, 16)
        split_layout.setSpacing(16)

        # Left Column: Table
        table_container = QWidget()
        table_col_layout = QVBoxLayout(table_container)
        table_col_layout.setContentsMargins(0, 0, 0, 0)
        table_col_layout.setSpacing(8)

        table_header = QLabel("COLA DE ENVÍOS PROGRAMADOS")
        table_header.setStyleSheet(f"font-size: 11px; font-weight: 700; color: {COLOR_MUTED}; letter-spacing: 1px;")
        table_col_layout.addWidget(table_header)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["TELÉFONO", "ASESOR", "NOMBRE", "ESTADO"])
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(False)
        self.table.verticalHeader().setDefaultSectionSize(36)

        header_view = self.table.horizontalHeader()
        header_view.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header_view.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header_view.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        header_view.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)

        table_col_layout.addWidget(self.table)
        split_layout.addWidget(table_container, 3)

        # Right Column: Console
        console_container = QWidget()
        console_col_layout = QVBoxLayout(console_container)
        console_col_layout.setContentsMargins(0, 0, 0, 0)
        console_col_layout.setSpacing(8)

        console_header = QLabel("CONSOLA DE EVENTOS EN VIVO")
        console_header.setStyleSheet(f"font-size: 11px; font-weight: 700; color: {COLOR_MUTED}; letter-spacing: 1px;")
        console_col_layout.addWidget(console_header)

        self.console = QTextEdit()
        self.console.setObjectName("consoleLogs")
        self.console.setReadOnly(True)
        console_col_layout.addWidget(self.console)

        split_layout.addWidget(console_container, 2)
        main_layout.addWidget(split_widget)

        # 4. Status Bar
        status_bar = QWidget()
        status_bar.setObjectName("statusBar")
        status_layout = QHBoxLayout(status_bar)
        status_layout.setContentsMargins(20, 0, 20, 0)

        self.lbl_footer_info = QLabel("Monitoreo activo | SQLite Persistencia Local")
        self.lbl_footer_info.setStyleSheet(f"font-size: 11px; color: {COLOR_MUTED}; font-family: {FONT_MONO_STACK};")
        status_layout.addWidget(self.lbl_footer_info)

        status_layout.addStretch()

        lbl_engine = QLabel("Trinity Engine v1.0")
        lbl_engine.setStyleSheet(f"font-size: 11px; color: {COLOR_MUTED}; font-family: {FONT_MONO_STACK};")
        status_layout.addWidget(lbl_engine)

        main_layout.addWidget(status_bar)

    def populate_table(self, envios: list[Envio]) -> None:
        self.table.setRowCount(len(envios))
        for row_idx, envio in enumerate(envios):
            cliente = envio.cliente
            item_tel = QTableWidgetItem(cliente.telefono)
            item_ase = QTableWidgetItem(cliente.asesor_nombre)
            item_nom = QTableWidgetItem(cliente.nombre or "-")

            for item in (item_tel, item_ase, item_nom):
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)

            self.table.setItem(row_idx, 0, item_tel)
            self.table.setItem(row_idx, 1, item_ase)
            self.table.setItem(row_idx, 2, item_nom)

            badge = QLabel(envio.estado.value)
            badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
            if envio.estado == EstadoEnvio.ENVIADO:
                badge.setStyleSheet(
                    "background-color: rgba(16, 185, 129, 0.15); color: #10b981; "
                    "border: 1px solid rgba(16, 185, 129, 0.4); border-radius: 4px; "
                    "padding: 2px 8px; font-family: 'JetBrains Mono'; font-size: 11px; font-weight: 600;"
                )
            elif envio.estado == EstadoEnvio.FALLIDO:
                badge.setStyleSheet(
                    "background-color: rgba(239, 68, 68, 0.15); color: #ef4444; "
                    "border: 1px solid rgba(239, 68, 68, 0.4); border-radius: 4px; "
                    "padding: 2px 8px; font-family: 'JetBrains Mono'; font-size: 11px; font-weight: 600;"
                )
            else:
                badge.setStyleSheet(
                    "background-color: rgba(234, 179, 8, 0.15); color: #eab308; "
                    "border: 1px solid rgba(234, 179, 8, 0.4); border-radius: 4px; "
                    "padding: 2px 8px; font-family: 'JetBrains Mono'; font-size: 11px; font-weight: 600;"
                )
            self.table.setCellWidget(row_idx, 3, badge)

    def append_log(self, text: str) -> None:
        self.console.append(text)
        scrollbar = self.console.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())


class MainWindow(QMainWindow):
    def __init__(
        self,
        scheduler: SchedulerService,
        personalizador: MessagePersonalizerService,
        envio_repo: IEnvioRepository,
        theme_manager: Any | None = None,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.scheduler = scheduler
        self.personalizador = personalizador
        self.envio_repo = envio_repo
        self.theme_manager = theme_manager

        self._worker: EnvioWorker | None = None
        self._log_bridge = QtLogBridge()
        self._log_bridge.log_signal.connect(self._on_log_received)
        logger.addHandler(self._log_bridge)

        self.setWindowTitle("Trinity - Monolith DataGrid WhatsApp")
        self.setMinimumSize(1100, 720)
        self.resize(1280, 800)

        # Set Window Icon
        from config.settings import settings
        
        logo_path = Path(settings.BASE_DIR) / "data" / "trinity-logo.ico"
        if not logo_path.is_file():
            logo_path = Path(settings.BASE_DIR) / "data" / "assets" / "trinity-logo.ico"
            
        if logo_path.is_file():
            pixmap = QPixmap(str(logo_path)).scaled(
                256, 256, 
                Qt.AspectRatioMode.KeepAspectRatio, 
                Qt.TransformationMode.SmoothTransformation
            )
            self.setWindowIcon(QIcon(pixmap))

        self.setStyleSheet(get_monolith_qss())

        self._init_ui()
        self.refresh_data()

        # Passive 5-minute timer for midnight rollover
        self._cuota_timer = QTimer(self)
        self._cuota_timer.setInterval(5 * 60 * 1000)
        self._cuota_timer.timeout.connect(self.actualizar_estado_cuota)
        self._cuota_timer.start()

    def _init_ui(self) -> None:
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.upload_view = UploadView(self)
        self.upload_view.file_imported.connect(self._handle_file_import)
        self.stacked_widget.addWidget(self.upload_view)

        self.dashboard_view = ProcessingDashboardView(self)
        self.dashboard_view.iniciar_clicked.connect(self._on_iniciar_campana)
        self.dashboard_view.cargar_otro_clicked.connect(self._on_cargar_otro_excel)
        self.dashboard_view.refrescar_clicked.connect(self.refresh_data)
        self.stacked_widget.addWidget(self.dashboard_view)

        # If data already exists in database, show dashboard immediately
        stats = self.envio_repo.get_stats()
        if stats["total"] > 0:
            self.stacked_widget.setCurrentIndex(1)
        else:
            self.stacked_widget.setCurrentIndex(0)

    @pyqtSlot(str)
    def _handle_file_import(self, file_path: str) -> None:
        try:
            nuevos = self.scheduler.importar_campana_desde_excel(file_path)
            self.refresh_data()
            self.stacked_widget.setCurrentIndex(1)
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
        except Exception as exc:
            QMessageBox.critical(
                self,
                "Error al Importar",
                f"Ocurrió un error al procesar el archivo Excel:\n{exc}",
            )

    @pyqtSlot()
    def _on_cargar_otro_excel(self) -> None:
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar archivo de campaña",
            "",
            "Archivos de Datos (*.xlsx *.xls *.csv)",
        )
        if file_path:
            self._handle_file_import(file_path)

    @pyqtSlot()
    def _on_iniciar_campana(self) -> None:
        if self._worker and self._worker.isRunning():
            return

        self._set_ui_busy(True)
        self.dashboard_view.append_log("Iniciando despacho de envíos...")

        self._worker = EnvioWorker(self.scheduler, self.personalizador, self)
        self._worker.progreso_signal.connect(self.dashboard_view.append_log)
        self._worker.finalizado_signal.connect(self._on_campana_finalizada)
        self._worker.error_signal.connect(self._on_campana_error)
        self._worker.finished.connect(lambda: self._set_ui_busy(False))
        self._worker.start()

    @pyqtSlot(str)
    def _on_campana_finalizada(self, resumen: str) -> None:
        self.dashboard_view.append_log(f"Jornada finalizada: {resumen}")
        self.refresh_data()
        QMessageBox.information(self, "Campaña Finalizada", resumen)

    @pyqtSlot(str)
    def _on_campana_error(self, error_msg: str) -> None:
        self.dashboard_view.append_log(f"Error crítico: {error_msg}")
        self.refresh_data()
        QMessageBox.critical(
            self,
            "Error en Campaña",
            f"Ocurrió un fallo durante la ejecución:\n{error_msg}",
        )

    def _set_ui_busy(self, is_busy: bool) -> None:
        self.dashboard_view.btn_cargar_otro.setEnabled(not is_busy)
        self.dashboard_view.btn_refrescar.setEnabled(not is_busy)
        self.dashboard_view.lbl_status.setText("Enviando mensajes..." if is_busy else "Listo")
        if is_busy:
            self.dashboard_view.btn_iniciar.setEnabled(False)
        else:
            self.actualizar_estado_cuota()

    @pyqtSlot(str)
    def _on_log_received(self, msg: str) -> None:
        self.dashboard_view.append_log(msg)

    @pyqtSlot()
    def actualizar_estado_cuota(self) -> None:
        envios_hoy = self.envio_repo.get_envios_hoy_count()
        limite = settings.DAILY_MESSAGE_LIMIT
        if envios_hoy >= limite:
            self.dashboard_view.btn_iniciar.setEnabled(False)
            self.dashboard_view.btn_iniciar.setText(f"Cuota Diaria Completada ({limite}/{limite})")
        else:
            if not (self._worker and self._worker.isRunning()):
                self.dashboard_view.btn_iniciar.setEnabled(True)
                self.dashboard_view.btn_iniciar.setText("Iniciar Campaña Diaria")

    def refresh_data(self) -> None:
        stats = self.envio_repo.get_stats()
        envios_hoy = self.envio_repo.get_envios_hoy_count()
        limite = settings.DAILY_MESSAGE_LIMIT

        self.dashboard_view.pill_cuota.setText(f"Cuota Hoy: {envios_hoy} / {limite}")
        self.dashboard_view.pill_pendientes.setText(f"Pendientes: {stats['pendientes']}")
        self.dashboard_view.pill_total.setText(f"Total Contactos: {stats['total']}")
        self.dashboard_view.pill_fallidos.setText(f"Fallidos: {stats['fallidos']}")

        pendientes = self.envio_repo.get_next_pendientes(limit=50)
        self.dashboard_view.populate_table(pendientes)
        self.actualizar_estado_cuota()

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
