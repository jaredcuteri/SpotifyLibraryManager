from googleapiclient.discovery import build
from oauth2client import client, tools
from oauth2client.file import Storage
import os

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

CLIENT_SECRETS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'youtube_secret.json')

def get_authenticated_service(client_secret_file=CLIENT_SECRETS_FILE):
    credential_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'credential_sample.json')
    store = Storage('/tmp/youtube_credential_store.json')
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(client_secret_file, SCOPES)
        credentials = tools.run_flow(flow, store)
    return build(API_SERVICE_NAME, API_VERSION, credentials=credentials)
