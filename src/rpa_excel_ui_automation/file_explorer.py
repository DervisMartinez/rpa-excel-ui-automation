import uiautomation as auto
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class FileExplorer:
    def __init__(self, excel_window: auto.WindowControl):
        self.excel_window = excel_window
        # Configurar un timeout global pequeño (para no bloquear innecesariamente, usaremos los del propio método)
        auto.uiautomation.SetGlobalSearchTimeout(10)

    def open_file(self, file_path: Path):
        logger.info(f"FileExplorer: Preparando para abrir el archivo {file_path}")
        
        # Localizar ventana de diálogo "Abrir"
        # ClassName para diálogos estándar de archivo es #32770
        dialog = self.excel_window.WindowControl(ClassName="#32770")
        if not dialog.Exists(3, 1):
            # Alternativa: Buscar en el Root por si el diálogo no es hijo directo de la ventana principal
            dialog = auto.WindowControl(ClassName="#32770")
            if not dialog.Exists(3, 1):
                logger.error("FileExplorer: No se encontró la ventana de diálogo de Abrir.")
                raise Exception("Dialog not found")
        
        logger.info("FileExplorer: Ventana de diálogo encontrada.")
        
        # Localizar el campo de texto de nombre de archivo
        file_name_edit = dialog.EditControl(AutomationId="1148")
        if not file_name_edit.Exists(3, 1):
            file_name_edit = dialog.EditControl()
        
        logger.info("FileExplorer: Inyectando la ruta del archivo origen sin usar tabulaciones.")
        file_name_edit.GetValuePattern().SetValue(str(file_path.absolute()))
        
        # Localizar botón de Abrir
        open_btn = dialog.ButtonControl(AutomationId="1")
        if not open_btn.Exists(1, 1):
            open_btn = dialog.ButtonControl(Name="Abrir")
            
        logger.info("FileExplorer: Haciendo clic programático en el botón Abrir.")
        open_btn.InvokePattern().Invoke()
        
        # Esperar a que la ventana se cierre dinámicamente
        if dialog.Exists(3, 1):
            dialog.Disappears(5)
        logger.info("FileExplorer: Archivo abierto exitosamente.")


    def save_as(self, file_path: Path):
        logger.info(f"FileExplorer: Preparando para guardar el archivo en {file_path}")
        
        # Localizar ventana de diálogo "Guardar como"
        dialog = self.excel_window.WindowControl(ClassName="#32770")
        if not dialog.Exists(5, 1):
            dialog = auto.WindowControl(ClassName="#32770")
            if not dialog.Exists(5, 1):
                logger.error("FileExplorer: No se encontró la ventana de diálogo de Guardar como.")
                raise Exception("Save As dialog not found")
            
        logger.info("FileExplorer: Ventana de diálogo 'Guardar como' encontrada.")
        
        file_name_edit = dialog.EditControl(AutomationId="1148")
        if not file_name_edit.Exists(3, 1):
            file_name_edit = dialog.EditControl()
            
        logger.info("FileExplorer: Inyectando la ruta absoluta destino.")
        file_name_edit.GetValuePattern().SetValue(str(file_path.absolute()))
        
        # Localizar botón de Guardar
        save_btn = dialog.ButtonControl(AutomationId="1")
        if not save_btn.Exists(1, 1):
             save_btn = dialog.ButtonControl(Name="Guardar")
        
        logger.info("FileExplorer: Haciendo clic programático en el botón Guardar.")
        save_btn.InvokePattern().Invoke()
        
        # Condición de Reemplazo: Evaluar si surge la ventana de confirmación
        confirm_dialog = dialog.WindowControl(ClassName="#32770")
        
        # Espera dinámica muy corta, porque si no existe el archivo se guardará de inmediato
        if confirm_dialog.Exists(2, 0.5):
            logger.warning("FileExplorer: Ventana de advertencia de sobreescritura detectada dinámicamente.")
            
            yes_btn = confirm_dialog.ButtonControl(AutomationId="CommandButton_6")
            if not yes_btn.Exists(1, 0.5):
                yes_btn = confirm_dialog.ButtonControl(Name="Sí")
                if not yes_btn.Exists(1, 0.5):
                     yes_btn = confirm_dialog.ButtonControl(Name="Yes")
            
            logger.info("FileExplorer: Confirmando el reemplazo del archivo existente.")
            if yes_btn.Exists(1, 0.5):
                yes_btn.InvokePattern().Invoke()
            else:
                confirm_dialog.SendKeys("{Alt}s") 
        
        if dialog.Exists(3, 1):
            dialog.Disappears(5)
            
        logger.info("FileExplorer: Archivo exportado de forma segura.")
