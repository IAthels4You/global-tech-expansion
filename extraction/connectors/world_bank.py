import requests
import pandas as pd
import logging
import sys
import os
from pydantic import ValidationError

# Añadir el directorio 'extraction' al path para poder importar 'utils' si se ejecuta directo
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import WorldBankRecord

# Configuración básica de logging para trazabilidad del proceso
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def fetch_preliminary_data():
    """
    Realiza peticiones GET a la API del World Bank para obtener una muestra inicial 
    de sus 4 indicadores principales. Los unifica en un solo DataFrame para que 
    puedan ser visualizados y filtrados juntos en D-Tale.
    """
    
    indicators = {
        "PIB per cápita (PPP)": "NY.GDP.PCAP.PP.CD",
        "Inflación": "FP.CPI.TOTL.ZG",
        "Población Total": "SP.POP.TOTL",
        "Banda Ancha Fija": "IT.NET.BBND.P2"
    }
    
    all_dataframes = []
    
    import time
    for name, code in indicators.items():
        page = 1
        pages = 1
        per_page = 1000 # Cantidad moderada para evitar bloqueos
        valid_records_for_indicator = []
        total_raw = 0
        
        logging.info(f"Iniciando extracción iterativa para: {name} ({code})")
        
        while page <= pages:
            url = (
                f"https://api.worldbank.org/v2/country/all/indicator/{code}"
                f"?format=json&per_page={per_page}&date=2000:2026&page={page}"
            )
            
            try:
                response = requests.get(url)
                response.raise_for_status()
                
                payload = response.json()
                if len(payload) < 2 or not payload[1]:
                    logging.warning(f"La API retornó datos vacíos en la página {page} para {code}.")
                    break
                    
                # Actualizar el número total de páginas en la primera petición
                if page == 1:
                    pages = payload[0].get('pages', 1)
                    logging.info(f"Se encontraron {pages} páginas en total para {name}.")
                    
                raw_data = payload[1]
                total_raw += len(raw_data)
                
                for item in raw_data:
                    try:
                        # Validamos usando Data Contracts y mapeamos columnas
                        record = WorldBankRecord(**item)
                        record_dict = record.model_dump()
                        record_dict['indicator_name'] = name
                        valid_records_for_indicator.append(record_dict)
                    except ValidationError:
                        # Filtramos los agregados regionales (ej. 'WLD', 'LCN')
                        pass
                
                logging.info(f"  -> Página {page}/{pages} procesada con éxito.")
                page += 1
                
                # Pausa breve para no saturar la API
                time.sleep(0.5)

            except requests.exceptions.RequestException as e:
                logging.error(f"Error durante la petición HTTP en la página {page} para {code}: {e}")
                break
                
        if valid_records_for_indicator:
            df = pd.DataFrame(valid_records_for_indicator)
            all_dataframes.append(df)
            logging.info(f"✓ Extracción completada para {name}. Registros limpios: {len(df)} (crudos totales: {total_raw})")
        else:
            logging.warning(f"Ningún registro superó la validación para {name}.")
            
    if all_dataframes:
        # Unificamos (apilamos) todas las tablas extraídas en una sola
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