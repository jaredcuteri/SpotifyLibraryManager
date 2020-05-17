import os
import sys
import youtube_dl
import spotipyExt
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import json

# TODO: Add playlist name capability
if len(sys.argv) > 1:
    numberOfTracks = int(sys.argv[1])
else:
    numberOfTracks = None
# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret.

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

CLIENT_SECRETS_FILE = "./client_secret.json" #This is the name of your JSON file

def get_authenticated_service():
    credential_path = os.path.join('./','credential_sample.json')
    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRETS_FILE, SCOPES)
        credentials = tools.run_flow(flow, store)
    return build(API_SERVICE_NAME, API_VERSION, credentials=credentials)
    

def makeStringName(track):
    return track['name'] + ' - ' + ' - '.join([artist['name'] for artist in track['artists']])

with open(CLIENT_SECRETS_FILE,'r') as fid:
    credz = json.load(fid)

#Spotipy Auth
sp_scope = 'user-library-read playlist-read-private' 
sp = spotipyExt.initializeSpotifyToken(sp_scope,credz['userconfig']['uid'])
tracks = sp.current_user_saved_tracks(limit=numberOfTracks)#limit=17,offset=0)  #102)
#tracks = sp.getTracksFromPlaylistName("The Future Was Yesterday")
#playlistName = "test_1"
#tracks = sp.getTracksFromPlaylistName(playlistName)

# Google Auth
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
service = get_authenticated_service()


trackURLs = []
outputDir = '/Users/jaredcuteri/Music/Downloads/recent/'
ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': outputDir+'%(title)s.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}

trackables = enumerate(tracks['items'])
    
for count, track  in trackables:
    query_result = service.search().list(
            part = 'snippet',
            q = makeStringName(track['track']),
            order = 'relevance', # You can consider using viewCount
            maxResults = 1,
            type = 'video', # Channels might appear in search results
            relevanceLanguage = 'en',
            safeSearch = 'moderate',
            ).execute()
    print("Searchs "+str(count))
    trackURL = "http://www.youtube.com/watch?v=" + query_result['items'][0]['id']['videoId']
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([trackURL])
            if os.path.isfile(outputDir+'_.mp3'):
                os.rename(outputDir+'_.mp3',outputDir+makeStringName(track['track'])+'.mp3')
        except:
            print("Video unable to be downloaded for "+makeStringName(track['track']))
