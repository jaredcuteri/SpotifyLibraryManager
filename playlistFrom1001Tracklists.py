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

PL_URL = 'https://www.1001tracklists.com/tracklist/28uj5vr1/luttrell-crssd-fest-united-states-2019-03-03.html'
SCOPE = 'user-library-read playlist-modify-private playlist-read-private'

# Header is needed to make Website believe this request is coming from a browser
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'} # This is chrome, you can set whatever browser you like

class RequestError(Exception):
    pass
    
response = requests.get(PL_URL, headers=headers)
if response.status_code >= 300:
    raise RequestError("Failed to access webpage. Response Code: {0}".format(response.status_code))

tree = html.fromstring(response.content)
setlist_title = tree.xpath('//body/meta[@itemprop="name"]/@content')

songs = tree.xpath('//div[@class="tlToogleData"][@itemprop="tracks"]/meta[@itemprop="name"]/@content')

def getTrackID(sp, trackName, artistName=None):
    tracks = sp.search(trackName,type='track')
    if tracks['tracks']['items']:
        if len(tracks['tracks']['items'])>1:
            # Use artistname to resolve
            tracks = sp.search(artistName + ' ' + trackName,limit=1,type='track')        
        return tracks['tracks']['items'][0]['id']
    else:
        return None    

# TODO: Remove ID - ID

sp = spotipyExt.initializeSpotifyToken(SCOPE)

setlistIDs, tracksNotFound = [], []
artists_tracks = [tuple((name) for name in song.split(' - ')) for song in songs]
for artistName, trackName in artists_tracks:
    trackID = getTrackID(sp, trackName, artistName)
    # TODO: Add way to resolve missing tracks
    if trackID:
        setlistIDs.append(trackID)
    else:
        tracksNotFound.append((artistName,trackName))

#Need to fix setlist title
setlist_title = setlist_title[0]

playlist = sp.user_playlist_create(spotipyExt.DEFAULT_USERNAME,setlist_title,public=False)
sp.user_playlist_add_tracks(spotipyExt.DEFAULT_USERNAME,playlist['id'],setlistIDs)
print("The following tracks could not be found", tracksNotFound)