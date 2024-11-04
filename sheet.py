from config import KEY, SCOPES # Importamos las credenciales de config.py
from googleapiclient.discovery import build # importamos el modulo de API de google
from google.oauth2 import service_account # importamos el módulo de credenciales de google para cuentas de Servicios

creds = None # Inicializamos las credenciales
creds = service_account.Credentials.from_service_account_file(KEY, scopes=SCOPES) # Cargamos las credenciales

service = build('sheets', 'v4', credentials=creds) # Cargamos la API

sheet = service.spreadsheets() # Cargamos la hoja de calculo