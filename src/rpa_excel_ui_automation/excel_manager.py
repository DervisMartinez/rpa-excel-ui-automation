import uiautomation as auto
import subprocess
import logging
from pathlib import Path
from .file_explorer import FileExplorer

logger = logging.getLogger(__name__)

class ExcelManager:
    def __init__(self):
        self.app_window = None
        self.file_explorer = None

    def start_app(self):
        logger.info("ExcelManager: Iniciando proceso de Microsoft Excel...")
        subprocess.Popen(["start", "excel"], shell=True)
        
        # Esperar a que la ventana principal de Excel exista
        self.app_window = auto.WindowControl(ClassName="XLMAIN")
        
        if not self.app_window.Exists(30, 1):
            logger.error("ExcelManager: No se pudo localizar la ventana principal de Excel (XLMAIN).")
            raise Exception("Excel window not found")
        
        # Asegurar visibilidad
        if self.app_window.WindowPattern().CurrentWindowVisualState != auto.WindowVisualState.Maximized:
            self.app_window.WindowPattern().SetWindowVisualState(auto.WindowVisualState.Maximized)
            
        self.app_window.SetActive()
        logger.info("ExcelManager: Interfaz de Excel activa y lista.")
        
        self.file_explorer = FileExplorer(self.app_window)

    def open_file(self, file_path: Path):
        logger.info("ExcelManager: Invocando el atajo universal para Abrir archivo (Ctrl+F12)...")
        self.app_window.SetActive()
        self.app_window.SendKeys('{Ctrl}{F12}')
        
        self.file_explorer.open_file(file_path)

    def save_as(self, file_path: Path):
        logger.info("ExcelManager: Invocando atajo nativo (F12) para Guardar como...")
        self.app_window.SetActive()
        self.app_window.SendKeys('{F12}')
        
        self.file_explorer.save_as(file_path)

