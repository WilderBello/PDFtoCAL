import os
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

def Obtener_credenciales(credencial=None, scope=None, tipo='', usuario=''):
    token_path = f'./credenciales_json/token_{tipo}_{usuario}.json'
    creds = None

    # Si existe el token, intentar cargarlo
    if os.path.exists(token_path):
        try:
            creds = Credentials.from_authorized_user_file(token_path, scope)
            if creds and creds.valid:
                return creds
        except Exception:
            print('Error al cargar token existente, generando uno nuevo...')

    # Si no hay credenciales válidas, solicitar nuevas
    print('Creando nuevo Token...\n')
    flow = InstalledAppFlow.from_client_secrets_file(credencial, scope)
    creds = flow.run_local_server(port=0)

    # Guardar nuevas credenciales
    with open(token_path, 'w') as token_file:
        json.dump(json.loads(creds.to_json()), token_file, indent=4)

    print('Token creado correctamente...')
    return creds
