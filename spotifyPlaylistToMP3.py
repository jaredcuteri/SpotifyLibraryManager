from __future__ import unicode_literals
import os
import youtube_dl
import spotipyExt
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret.
CLIENT_SECRETS_FILE = "client_secret.json" #This is the name of your JSON file

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

def get_authenticated_service():
  flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
  credentials = flow.run_console()
  return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)

def makeStringName(track):
    return track['name'] + ' - ' + ' - '.join([artist['name'] for artist in track['artists']])


#Spotipy Auth
sp_scope = 'user-library-read playlist-read-private'
sp = spotipyExt.initializeSpotifyToken(sp_scope)
tracks = sp.current_user_saved_tracks(limit=20)  #102)
#playlistName = "This Is Lane 8"
#tracks =  sp.getTracksFromPlaylistName(playlistName)

# Google Auth
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
service = get_authenticated_service()


trackURLs = []
outputDir = '/Users/jaredcuteri/Music/Downloads/'
ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': outputDir+'%(title)s.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}


for count, track  in enumerate(tracks['items']):
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
        ydl.download([trackURL])
