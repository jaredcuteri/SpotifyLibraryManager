'''
This script will generate a spotify playlist from a 1001tracklists.com tracklist
'''
# HTML Track Format
#<span class="trackFormat">
#    <span class="blueTxt">
#        "ARTIST NAME"
#        <span title="open artist page" class="tgHidspL">...</span>
#        </span>
#    <span class> - </span>
#    <span class="blueTxt">
#        "TRACK NAME"
#        <span title="oepn track page" class="tgHidspL">...</span>
#    </span>
#</span>

import spotipyExt
from lxml import html
import requests

PL_URL = 'https://www.1001tracklists.com/tracklist/28v8f871/the-martinez-brothers-ce-la-vi-marina-bay-sands-singapore-cercle-2019-11-18.html'
def PlaylistFrom1001Tracklist(playlistURL):
    class RequestError(Exception):
        pass

    # Header is needed to make Website believe this request is coming from a browser
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'} # This is chrome, you can set whatever browser you like
    
    response = requests.get(playlistURL, headers=headers)
    if response.status_code >= 300:
        raise RequestError("Failed to access webpage. Response Code: {0}".format(response.status_code))

    tree = html.fromstring(response.text)
    setlist_title = tree.xpath('//body/meta[@itemprop="name"]/@content')

    songs = tree.xpath('//div[@class="tlToogleData"][@itemprop="tracks"]/meta[@itemprop="name"]/@content')
            
    sp_scope = 'user-library-read playlist-modify-private playlist-read-private'
    sp = spotipyExt.initializeSpotifyToken(sp_scope)

    setlistIDs, tracksNotFound = [], []
    artists_tracks = [tuple((name) for name in song.split(' - ')) for song in songs]
    for artistName, trackName in artists_tracks:
        trackID = sp.getTrackID(trackName, artistName)
        # TODO: Add way to resolve missing tracks
        if trackID:
            setlistIDs.append(trackID)
        else:
            tracksNotFound.append((artistName,trackName))

    #Need to fix setlist title
    setlist_title = setlist_title[0]

    playlist = sp.user_playlist_create(sp.username,setlist_title,public=False)
    sp.user_playlist_add_tracks(sp.username,playlist['id'],setlistIDs)
    if tracksNotFound:
        print("The following tracks could not be found", tracksNotFound)
    else:
        print("All tracks added successfully")
    
if __name__ == '__main__':
    PlaylistFrom1001Tracklist(PL_URL)