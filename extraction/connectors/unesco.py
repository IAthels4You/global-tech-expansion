import requests
import pandas as pd
import logging
import sys
import os
from pydantic import ValidationError

# Añadir el directorio 'extraction' al path para poder importar 'utils'
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import UnescoRecord

# Configuración básica de logging para trazabilidad del proceso
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def fetch_preliminary_data():
    """
    Realiza peticiones GET a la API de UNESCO para obtener los datos de sus 
    indicadores principales. Aplica Data Contracts para estandarizar las 
    columnas y filtrar agregados regionales automáticamente.
    """
    
    indicators = {
        "Graduados STEM (ISCED 5-8)": "FOSGP.5T8.F500600700",
        "Gasto en I+D (% PIB)": "EXPGDP.TOT"
    }
    
    headers = {
        'Accept-Encoding': 'gzip'
    }
    
    all_dataframes = []
    
    for name, code in indicators.items():
        url = (
            f"https://api.uis.unesco.org/api/public/data/indicators"
            f"?indicator={code}&start=2000&end=2026"
        )
        
        try:
            logging.info(f"Iniciando petición para: {name} ({code})")
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            payload = response.json()
            
            if 'records' not in payload or not payload['records']:
                logging.warning(f"La API retornó datos vacíos para {code}.")
                continue
                
            raw_data = payload['records']
            valid_records = []
            
            for item in raw_data:
                try:
                    # Validamos el registro usando el Data Contract de UNESCO
                    # Esto descarta agregados, ignora campos innecesarios y estandariza nombres
                    record = UnescoRecord(**item)
                    
                    record_dict = record.model_dump()
                    # Añadimos la columna con el nombre descriptivo del indicador
                    record_dict['indicator_name'] = name
                    
                    valid_records.append(record_dict)
                except ValidationError:
                    # Se descarta silenciosamente si el país es un agregado regional o código inválido
                    pass
            
            if valid_records:
                df = pd.DataFrame(valid_records)
                all_dataframes.append(df)
                logging.info(f"✓ Extraídos {len(df)} registros limpios y validados para {name} (original: {len(raw_data)})")
            else:
                logging.warning(f"Ningún registro superó la validación para {name}.")

        except requests.exceptions.RequestException as e:
            logging.error(f"Error durante la petición HTTP para {code}: {e}")
            
    if all_dataframes:
        df_final = pd.concat(all_dataframes, ignore_index=True)
        logging.info(f"Extracción exitosa. Registros totales unificados: {len(df_final)}")
        return df_final
    else:
        return pd.DataFrame()

if __name__ == "__main__":
    # Ejecución del módulo de exploración
    df_exploracion = fetch_preliminary_data()
    
    if not df_exploracion.empty:
        import dtale
        logging.info("Abriendo D-Tale en el navegador para visualización interactiva...")
        # dtale.show crea un servidor local y open_browser abre la interfaz automáticamente
        d = dtale.show(df_exploracion, enable_custom_filters=True)
        d.open_browser()
        
        # Mantenemos el proceso vivo sin depender de input() para que funcione con el botón "Play"
        import time
        logging.info("Servidor D-Tale activo. Presiona el botón de 'Stop' o Ctrl+C para detenerlo.")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logging.info("Cerrando servidor D-Tale...")
    else:
        logging.warning("No se obtuvieron datos para visualizar.")
