import requests
import pandas as pd
import logging

# Configuración básica de logging para trazabilidad del proceso
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def fetch_preliminary_data():
    """
    Realiza una petición GET a la API del World Bank para obtener una muestra inicial 
    de 300 registros. El propósito es inspeccionar la estructura de los datos 
    y la calidad de la información antes de definir contratos de validación.
    """
    
    url = (
        "https://api.worldbank.org/v2/country/all/indicator/NY.GDP.PCAP.PP.CD"
        "?format=json&per_page=300&date=2000:2026"
    )
    
    try:
        logging.info("Iniciando petición a la API del World Bank...")
        response = requests.get(url)
        response.raise_for_status()
        
        # La respuesta de la API del World Bank es una lista donde:
        # [0] contiene metadatos de paginación
        # [1] contiene el arreglo de registros (Data)
        payload = response.json()
        
        if len(payload) < 2:
            logging.warning("La API retornó una estructura inesperada o vacía.")
            return pd.DataFrame()
            
        raw_data = payload[1]
        
        # Normalización del JSON anidado a un DataFrame plano
        # Esto permite visualizar columnas como 'country.id' y 'indicator.value'
        df = pd.json_normalize(raw_data)
        
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
        d = dtale.show(df_exploracion)
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