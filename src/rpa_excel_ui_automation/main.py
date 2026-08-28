import logging
from pathlib import Path
from rpa_excel_ui_automation.excel_manager import ExcelManager
import sys

def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    logger = logging.getLogger(__name__)
    
    # Rutas usando pathlib
    base_dir = Path(__file__).parent.parent.parent
    data_dir = base_dir / ".data"
    input_dir = data_dir / "input"
    output_dir = data_dir / "output"
    
    origen_path = input_dir / "origen.xlsx"
    destino_path = output_dir / "destino.xlsx"
    
    # Asegurar que las carpetas existan
    output_dir.mkdir(parents=True, exist_ok=True)
    if not origen_path.exists():
        logger.error(f"El archivo origen no existe: {origen_path}")
        logger.info("Por favor, asegúrate de crear el archivo antes de ejecutar el robot.")
        return
        
    logger.info("==== INICIANDO AUTOMATIZACIÓN RPA EXCEL ====")
    manager = ExcelManager()
    
    try:
        # Caso 01
        logger.info("--- Ejecutando Caso 01: Inicialización e Importación Dinámica ---")
        manager.start_app()
        manager.open_file(origen_path)
        
        # Caso 02
        logger.info("--- Ejecutando Caso 02: Procesamiento y Exportación Segura ---")
        manager.save_as(destino_path)
        
    except Exception as e:
        logger.error(f"Error durante la automatización: {e}", exc_info=True)
    finally:
        logger.info("==== AUTOMATIZACIÓN FINALIZADA ====")
        logger.info("Excel debería permanecer abierto según los casos de prueba.")

if __name__ == "__main__":
    main()

