'''
This script will generate a playlist with popular tracks
of each artist on a poster.
'''
import math

import setlistExtractor
import spotipyExt


USERNAME = '1232863129'
IMAGE = 'posters/shaky.jpg'
PLAYLIST_NAME = 'Shaky Beats'

# Inline functions
rSlice = lambda x: x[:-1]
lSlice = lambda x: x[1:]
trackCountBasedOnPopularity = lambda x,y :(math.ceil((1-(x/y))/0.25)+1)

# Get setlist from image
setlist = setlistExtractor.generateSetlistFromImage(IMAGE)

# spotipy auth/init
scope = 'user-library-read playlist-modify-private playlist-read-private'
spotify = spotipyExt.initializeSpotifyToken(scope)

# Find artists
artistsDict = dict.fromkeys(setlist)
for possibleArtist in setlist:
    result = spotify.search(possibleArtist, limit=10, type='artist', market=None)
    possibleArtistMatches = result['artists']['items']
    
    foundArtist = spotify.fullArtistMatch(possibleArtistMatches, possibleArtist)
    if foundArtist:
        artistsDict[possibleArtist] = foundArtist
    # Check for a partial match
    else:
        # Add in partial name searching
        foundArtist = spotify.partialArtistMatch(possibleArtist,slicer=rSlice)
        if foundArtist:
            artistsDict[possibleArtist] = foundArtist
        else:
            foundArtist = spotify.partialArtistMatch(possibleArtist,slicer=lSlice)
            if foundArtist:
                artistsDict[possibleArtist] = foundArtist
            else:
                artistsDict[possibleArtist] = None
    #TODO: Add progress bar of matches and misses

matchedArtists = [v for k,v in artistsDict.items() if v is not None]  
unmatchedArtists = [k for k,v in artistsDict.items() if v is None]

print('+ Found %d/%d of possible artists.'%(len(matchedArtists),len(setlist)))
print('-- The following possible artists could not be found: ',unmatchedArtists)

playlistTracks = spotify.getTracksByArtists(matchedArtists,numSongs=trackCountBasedOnPopularity)
    
# Create playlist and add songs
playlist = spotify.user_playlist_create(USERNAME, PLAYLIST_NAME, public=True)
playlistTracksID = [track['id'] for track in playlistTracks]
spotify.user_playlist_add_tracks(USERNAME, playlist['id'], playlistTracksID)
print('+++ Playlist Generated: ',PLAYLIST_NAME)
print('++++ %d tracks added'%len(playlistTracksID))