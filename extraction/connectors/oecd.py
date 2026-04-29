import requests
import pandas as pd
import logging

# Configuración básica de logging para trazabilidad del proceso
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def fetch_preliminary_data():
    """
    Realiza una petición GET a la API de OECD para obtener una muestra inicial 
    de los registros. El propósito es inspeccionar la estructura de los datos 
    y la calidad de la información antes de definir contratos de validación.
    """
    
    url = (
        "https://sdmx.oecd.org/public/rest/data/OECD.ELS.SAE,DSD_EARNINGS@AV_AN_WAGE,1.0/all"
        "?startPeriod=2000&dimensionAtObservation=AllDimensions"
    )
    headers = {
        'Accept': 'application/vnd.sdmx.data+json; version=1.0.0-wd'
    }
    
    try:
        logging.info("Iniciando petición a la API de OECD...")
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
                    # Obtenemos el valor real ('id' o 'name') según el índice
                    dim_val = dim['values'][indices[i]]['id']
                    record[dim_id] = dim_val
                    
                record['value'] = obs_value[0]
                raw_data.append(record)
                
        except (KeyError, IndexError):
            logging.warning("La API retornó una estructura inesperada o vacía.")
            return pd.DataFrame()
            
        # Normalización a un DataFrame plano
        df = pd.DataFrame(raw_data)
        
        logging.info(f"Extracción exitosa. Registros obtenidos: {len(df)}")
        return df

    except requests.exceptions.RequestException as e:
        logging.error(f"Error durante la petición HTTP: {e}")
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
