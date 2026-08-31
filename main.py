from __future__ import annotations
import sys
import ctypes
from PyQt6.QtWidgets import QApplication

myappid = 'Elmichi & lsqraa.trinity.1.0'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

from app.infrastructure.database.sqlite_adapter import SQLiteAdapter
from app.infrastructure.excel.pandas_worker import PandasWorker
from app.infrastructure.whatsapp.playwright_bot import PlaywrightWhatsAppBot
from app.services.validator import ContactValidatorService
from app.services.scheduler import SchedulerService
from app.services.message_personalization import MessagePersonalizerService
from app.ui.main_window import MainWindow

def main() -> None:
    app = QApplication(sys.argv)

    envio_repo = SQLiteAdapter()
    excel_reader = PandasWorker()
    whatsapp_sender = PlaywrightWhatsAppBot()
    validator_service = ContactValidatorService()

    scheduler = SchedulerService(
        excel_reader=excel_reader,
        envio_repo=envio_repo,
        whatsapp_sender=whatsapp_sender,
        validator_service=validator_service
    )
    
    personalizador = MessagePersonalizerService()

    window = MainWindow(
        scheduler=scheduler, 
        personalizador=personalizador, 
        envio_repo=envio_repo
    )
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()