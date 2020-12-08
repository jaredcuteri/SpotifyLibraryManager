import os
import sys
import youtube_dl
from spotipyExt.auth import SpotifyAuth, YoutubeAuth
import json

def makeStringName(track):
    return track['name'] + ' - ' + ' - '.join([artist['name'] for artist in track['artists']])

# TODO: Add playlist name capability
if len(sys.argv) > 1:
    numberOfTracks = int(sys.argv[1])
else:
    numberOfTracks = 0

#Spotipy Auth
sp_scope = 'user-library-read playlist-read-private' 
sp = SpotifyAuth.get_authenticated_service(scope=sp_scope)

# Google Auth
yt = YoutubeAuth.get_authenticated_service()

tracks = sp.current_user_saved_tracks(limit=numberOfTracks)
#tracks = sp.getTracksFromPlaylistName("")

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
    trackname = makeStringName(track['track'])
    query_result = yt.search().list(
            part = 'snippet',
            q = trackname, 
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
                os.rename(outputDir+'_.mp3',outputDir+trackname+'.mp3')
        except:
            print("Video unable to be downloaded for "+trackname)
