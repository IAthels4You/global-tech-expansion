import requests
import pandas as pd
import logging
from pydantic import ValidationError
import sys
import os

# Asegurar que el path del proyecto esté en sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import OecdRecord

# Configuración básica de logging para trazabilidad del proceso
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

OECD_INDICATORS = {
    "Salarios Anuales": {
        "dataset": "OECD.ELS.SAE,DSD_EARNINGS@AV_AN_WAGE,1.0",
        "filters": {
            "PRICE_BASE": "Q"
        }
    },
    "Tax Wedge": {
        "dataset": "OECD.CTP.TPS,DSD_TAX_WAGES_COMP@DF_TW_COMP,1.0",
        "filters": {
            "UNIT_MEASURE": "PT_WG_EARN_G",
            "MEASURE": "NPATR",
            "HOUSEHOLD_TYPE": "S_C0",
            "INCOME_PRINCIPAL": "AW100",
            "INCOME_SPOUSE": "_Z"
        }
    }
}

def fetch_oecd_data():
    """
    Extrae los indicadores de la API de OECD mediante el estándar SDMX,
    aplica filtros de dimensiones y valida con el Data Contract de Pydantic.
    """
    
    headers = {
        'Accept': 'application/vnd.sdmx.data+json; version=1.0.0-wd'
    }
    
    all_valid_records = []

    for indicator_name, config in OECD_INDICATORS.items():
        dataset = config["dataset"]
        filters = config["filters"]
        
        url = (
            f"https://sdmx.oecd.org/public/rest/data/{dataset}/all"
            "?startPeriod=2000&dimensionAtObservation=AllDimensions"
        )
        
        try:
            logging.info(f"Iniciando petición a la API de OECD para {indicator_name}...")
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            payload = response.json()
            
            try:
                # Extraemos la estructura de dimensiones para mapear los índices
                dimensions = payload['data']['structure']['dimensions']['observation']
                obs = payload['data']['dataSets'][0]['observations']
                
                raw_data = []
                for key_str, obs_value in obs.items():
                    # El formato de llave es "0:0:0:0:0:0:0:0", lo separamos por ':'
                    indices = [int(x) for x in key_str.split(':')]
                    
                    record = {}
                    # Mapeamos cada índice con su valor real en la estructura
                    for i, dim in enumerate(dimensions):
                        dim_id = dim['id']
                        dim_val = dim['values'][indices[i]]['id']
                        record[dim_id] = dim_val
                        
                    record['value'] = obs_value[0]
                    record['indicator_name'] = indicator_name
                    
                    # Filtrar según los requerimientos del diccionario
                    keep = True
                    for f_key, f_val in filters.items():
                        if record.get(f_key) != f_val:
                            keep = False
                            break
                    
                    if keep:
                        raw_data.append(record)
                        
            except (KeyError, IndexError):
                logging.warning(f"La API retornó una estructura inesperada o vacía para {indicator_name}.")
                continue
                
            # Validación mediante el Data Contract
            valid_count = 0
            for raw_record in raw_data:
                try:
                    # El modelo descarta automáticamente las dimensiones que no estén definidas
                    # y estandariza los nombres de las columnas
                    validated = OecdRecord(**raw_record).model_dump()
                    all_valid_records.append(validated)
                    valid_count += 1
                except ValidationError:
                    # Se ignoran los registros con códigos de país inválidos (agregados regionales)
                    pass
            
            logging.info(f"Extracción exitosa. Registros válidos para {indicator_name}: {valid_count}")

        except requests.exceptions.RequestException as e:
            logging.error(f"Error durante la petición HTTP para {indicator_name}: {e}")
            continue

    if not all_valid_records:
        logging.warning("No se obtuvieron datos para visualizar.")
        return pd.DataFrame()
        
    # Normalización a un DataFrame con exactamente 5 columnas
    df = pd.DataFrame(all_valid_records)
    return df

if __name__ == "__main__":
    df_exploracion = fetch_oecd_data()
    
    if not df_exploracion.empty:
        import dtale
        logging.info("Abriendo D-Tale en el navegador para visualización interactiva...")
        d = dtale.show(df_exploracion, enable_custom_filters=True)
        d.open_browser()
        
        import time
        logging.info("Servidor D-Tale activo. Presiona el botón de 'Stop' o Ctrl+C para detenerlo.")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logging.info("Cerrando servidor D-Tale...")
