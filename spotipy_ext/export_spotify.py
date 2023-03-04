import argparse
from spotipy_ext.auth import spotify_auth, youtube_auth
import os
from pathlib import Path
import yt_dlp as youtube_dl

def makeStringName(track):
    return track['name'] + ' - ' + ' - '.join([artist['name'] for artist in track['artists']])

def main(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--playlist', '-p', action='store',
                        default=None, help='Playlist from user library to pull tracks from.')
    parser.add_argument('--ntracks','-n', action='store', type=int,
                        default=float('inf'), help='Number of tracks to pull.')
    args = parser.parse_args(args)

    download_spotify_tracks(args.ntracks, playlist=args.playlist)

def download_spotify_tracks(track_count, playlist=None):
    #Spotipy Auth
    sp = spotify_auth.get_authenticated_service()

    # Google Auth
    yt = youtube_auth.get_authenticated_service()

    if playlist:
        tracks = sp.getTracksFromPlaylistName(playlist,limit=track_count)
    else:
        tracks = sp.current_user_saved_tracks(limit=track_count)

    outputDir = f'/Users/jaredcuteri/Music/Downloads/{playlist.lower().replace(" ","_") if playlist else "recent"}/'
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': outputDir+'%(title)s.%(ext)s',
        'nocheckcertificate': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    trackables = enumerate(tracks['items'])

    for _, track  in trackables:
        trackname = makeStringName(track['track'])
        output_path =  Path(outputDir) / f'{trackname}.mp3'

        # skip if already downloaded
        if output_path.is_file():
            print(f'File already downloaded: {output_path}')
            continue

        query_result = yt.search().list(
                part = 'snippet',
                q = trackname,
                order = 'relevance', # You can consider using viewCount
                maxResults = 1,
                type = 'video', # Channels might appear in search results
                relevanceLanguage = 'en',
                safeSearch = 'moderate',
                ).execute()

        trackURL = "http://www.youtube.com/watch?v=" + query_result['items'][0]['id']['videoId']

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            try:
                ydl.download([trackURL])
                if os.path.isfile(outputDir+'_.mp3'):
                    os.rename(outputDir+'_.mp3', str(output_path))
                    print(f'File downloaded: {output_path}')
            except Exception:
                print("Video unable to be downloaded for "+trackname)

if __name__=='__main__':
    main()
