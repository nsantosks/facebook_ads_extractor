# 1. IMPORTACIONES: Traemos las herramientas que necesitamos
import pandas as pd
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from datetime import datetime, timedelta
import os

# --- CONFIGURACIÓN DE SEGURIDAD (Tu código original, está perfecto) ---
my_app_id = os.environ.get('FACEBOOK_APP_ID_ALLEXCELUP')
my_app_secret = os.environ.get('FACEBOOK_APP_SECRET_ALLEXCELUP')
my_access_token = os.environ.get('FACEBOOK_ACCESS_TOKEN_ALLEXCELUP')
ad_account_id = os.environ.get('FACEBOOK_AD_ACCOUNT_ID_ALLEXCELUP')

if not all([my_app_id, my_app_secret, my_access_token, ad_account_id]):
    print("Error: Una o más variables de entorno no están configuradas.")
    exit()
    
# 2. INICIALIZACIÓN DE LA API (Tu código original, está perfecto) ---
try:
    FacebookAdsApi.init(my_app_id, my_app_secret, my_access_token)
    print("Conexión con la API de Facebook exitosa.")
except Exception as e:
    print(f"Error al conectar con la API: {e}")
    exit()

# ==============================================================================
# ### NUEVO: UNA FUNCIÓN REUTILIZABLE PARA EXTRAER Y PROCESAR DATOS ###
# Creamos una función para no repetir el mismo código una y otra vez.
# Esta función hará una llamada a la API y convertirá el resultado en una tabla (DataFrame).
# ==============================================================================
def fetch_and_process_insights(ad_account_obj, fields, params):
    """
    Realiza una llamada a la API de Facebook Insights, procesa los resultados
    y los devuelve como un DataFrame de pandas.
    """
    data_list = []
    try:
        # Hacemos la llamada a la API con los parámetros que nos pasen
        insights = ad_account_obj.get_insights(fields=fields, params=params)
        
        # Procesamos cada fila de la respuesta
        for insight in insights:
            # Tu lógica original para procesar las conversiones
            conversions = sum([int(action['value']) for action in insight.get('actions', []) if action['action_type'] == 'onsite_conversion.post_save'])
            roas = float(insight.get('purchase_roas', [{}])[0].get('value', 0.0)) if insight.get('purchase_roas') else 0.0

            # Creamos la fila base con los datos
            row = {
                'date': insight.get('date_start'),
                'campaign_name': insight.get('campaign_name'),
                'adset_name': insight.get('adset_name'),
                'ad_name': insight.get('ad_name'),
                'impressions': int(insight.get('impressions', 0)),
                'reach': int(insight.get('reach', 0)),
                'spend': float(insight.get('spend', 0.0)),
                'clicks': int(insight.get('clicks', 0)),
                'cpc': float(insight.get('cpc', 0.0)),
                'ctr': float(insight.get('ctr', 0.0)),
                'conversions': conversions,
                'roas': roas
            }
            
            # Añadimos las columnas de desglose (si existen)
            # Esto hace que la función sea flexible
            if 'breakdowns' in params:
                for breakdown in params['breakdowns']:
                    row[breakdown] = insight.get(breakdown, 'N/A')
            
            data_list.append(row)

        print(f"-> ¡Éxito! Se procesaron {len(data_list)} filas de datos.")

    except Exception as e:
        print(f"-> ERROR durante la llamada a la API: {e}")
        # Si hay un error, la función devolverá una tabla vacía para no detener todo el script
        return pd.DataFrame()
        
    # Convertimos la lista de datos a una tabla de pandas y la devolvemos
    return pd.DataFrame(data_list)

# ==============================================================================
# ### CUERPO PRINCIPAL DEL SCRIPT ###
# Aquí usamos nuestra nueva función para hacer las llamadas de forma ordenada.
# ==============================================================================

# --- Parámetros comunes para todas las llamadas ---
ad_account = AdAccount(ad_account_id)
fields_to_request = [
    'campaign_name', 'adset_name', 'ad_name',
    'reach', 'impressions', 'spend', 'clicks', 'cpc', 'ctr',
    'actions', 'action_values', 'purchase_roas'
]
end_date = datetime.now()
start_date = end_date - timedelta(days=30)
time_range_dict = {'since': start_date.strftime('%Y-%m-%d'), 'until': end_date.strftime('%Y-%m-%d')}


# --- LLAMADA 1: DATOS DEMOGRÁFICOS (EDAD Y GÉNERO) ---
print("\n--- INICIANDO EXTRACCIÓN 1: DATOS DEMOGRÁFICOS ---")
params_demo = {
    'level': 'ad',
    'time_range': time_range_dict,
    'breakdowns': ['age', 'gender']  # Combinación válida
}
df_demographics = fetch_and_process_insights(ad_account, fields_to_request, params_demo)


# --- LLAMADA 2: DATOS GEOGRÁFICOS (PAÍS Y REGIÓN) ---
print("\n--- INICIANDO EXTRACCIÓN 2: DATOS GEOGRÁFICOS ---")
params_geo = {
    'level': 'ad',
    'time_range': time_range_dict,
    'breakdowns': ['country', 'region'] # Combinación válida
}
df_geographics = fetch_and_process_insights(ad_account, fields_to_request, params_geo)


# --- LLAMADA 3: DATOS DE UBICACIÓN (PLATAFORMA Y DISPOSITIVO) ---
print("\n--- INICIANDO EXTRACCIÓN 3: DATOS DE UBICACIÓN ---")
params_placement = {
    'level': 'ad',
    'time_range': time_range_dict,
    'breakdowns': ['publisher_platform', 'device_platform'] # Combinación válida
}
df_placements = fetch_and_process_insights(ad_account, fields_to_request, params_placement)


# --- 6. GUARDADO DE LOS ARCHIVOS CSV ---
print("\n--- GUARDANDO LOS RESULTADOS EN ARCHIVOS CSV ---")

# Guardamos el archivo de datos demográficos
if not df_demographics.empty:
    file_path_demo = 'facebook_data_demographics.csv'
    df_demographics.to_csv(file_path_demo, index=False, encoding='utf-8-sig')
    print(f"Archivo guardado: {file_path_demo}")
else:
    print("No se generó el archivo demográfico (no se obtuvieron datos o hubo un error).")

# Guardamos el archivo de datos geográficos
if not df_geographics.empty:
    file_path_geo = 'facebook_data_geographics.csv'
    df_geographics.to_csv(file_path_geo, index=False, encoding='utf-8-sig')
    print(f"Archivo guardado: {file_path_geo}")
else:
    print("No se generó el archivo geográfico (no se obtuvieron datos o hubo un error).")

# Guardamos el archivo de datos de ubicación
if not df_placements.empty:
    file_path_place = 'facebook_data_placements.csv'
    df_placements.to_csv(file_path_place, index=False, encoding='utf-8-sig')
    print(f"Archivo guardado: {file_path_place}")
else:
    print("No se generó el archivo de ubicaciones (no se obtuvieron datos o hubo un error).")

print("\n¡Proceso de extracción completado!")