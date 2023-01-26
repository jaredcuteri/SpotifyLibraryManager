import json
import os
from .. import spotipy_ext

CLIENT_SECRETS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'spotify_secret.json')

def get_user_config(client_secret_file = CLIENT_SECRETS_FILE):
    with open(client_secret_file,'r') as fid:
        credz = json.load(fid)
    return credz['spotify']

def get_authenticated_service(client_secret_file=CLIENT_SECRETS_FILE):
    config = get_user_config(client_secret_file)
    return spotipy_ext.initialize_spotify_token(**config)
