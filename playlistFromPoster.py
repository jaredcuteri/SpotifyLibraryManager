'''

This function will be able to read a festival poster, generate a list of artists performing, look up their most popular tracks and create a playlist with them

'''
try: from PIL import Image, ImageEnhance
except ImportError: import Image, ImageEnhance
import pytesseract
import inspect
import re
import spotipyExt
import math

USERNAME = '1232863129'
IMAGE = 'posters/crssd.jpg'
PLAYLIST_NAME = 'CRSSD Spring 2018'
pytesseract.tesseract_cmd = r'/user/local/Cellar/tesseract/4.0.0/bin/tesseract'

# Open poster
poster = Image.open(IMAGE)

# modify poster to make it readable (monochromatic)
poster_gray = poster.convert('L')
# TODO: Ensure that the poster ends up black on white
poster_bw = poster_gray.point(lambda x: 0 if x<128 else 255,'1')

#save off text from poster
poster_text = pytesseract.image_to_string(poster_bw)

# replace all weird characters with . 
weird_characters = ['\n','-','»','>','°','*','~']
for character in weird_characters:
    poster_text = poster_text.replace(character,'.')

#parse string into list of possible artists
# TODO: Pan-Pot is being split because of weird character replacement    
setlist = re.split('\W*\.+\W*',poster_text)


# Verify list of artists via spotipy (using popularity)
scope = 'user-library-read playlist-modify-private playlist-read-private'
spotify = spotipyExt.initializeSpotifyToken(scope)
artistsDict = dict.fromkeys(setlist)

def lSlice(string):
    return string[1:]
def rSlice(string):
    return string[:-1]

def PartialArtistMatch(FullName,PartialName=None,slicer=rSlice):
    # Initializing PartialName for recursion
    if PartialName==None:
        PartialName = FullName
        
    # Base popularity threshold off how much of name has been removed
    # TODO: tune theshold scheduling
    subStringRatio = len(PartialName)/len(FullName)
    popThresh = 20*(-0.3+(1-subStringRatio))
    
    found_artist = spotify.search(PartialName,limit=1,type='artist')
    
    # Exit if we've trimmed more than 50% of the name
    if subStringRatio<0.5:
        return None
    # Check for match
    # TODO: is it necessary to check the name again? Does search only return perfect matches?
    elif found_artist['artists']['items'] \
     and found_artist['artists']['items'][0]['name'] == PartialName \
     and found_artist['artists']['items'][0]['popularity'] >= popThresh:
        return found_artist['artists']['items'][0]   
    # Recurse with partial name
    else:
        final_result = PartialArtistMatch(FullName,slicer(PartialName),slicer=slicer)
        return final_result

def FullArtistMatch(possibleArtistMatches, possibleArtist):
    # sort artists by popularity
    popThresh = 10 # Popularity Threshold
    possibleArtistMatches = [ x for x in possibleArtistMatches if x['popularity']>=popThresh]
    possibleArtistMatches.sort(key=lambda x: x['popularity'], reverse=True)
    # Check for perfect matches
    for artist in possibleArtistMatches:
        if artist['name'] == possibleArtist:
            return artist
    else:
        return None
  
      
def trackCountBasedOnPopularity(rank,total):
    #TODO: update tracks scheduling
    # Current schedule top 25% - 5 tracks 50% - 4 tracks 75% - 3 tracks 100% - 2 tracks
    return math.ceil((1-(rank/total))/0.25)+1

def getTracksByArtists(artists,numSongs=trackCountBasedOnPopularity):
    ''' getTracksByArtists returns a list of tracks containing top tracks from artists
    
        Parameters:
            artists - list of spotipy artists 
            numSongs - function that determines number of tracks to add from each artist
    
        Returns:
            playlistTracks - list of tracks
    '''
    # Sort Artists By Popularity
    artists.sort(key=lambda x: x['popularity'], reverse=True)
    # Determine Number of Artists
    numArt=len(artists)
    playlistTracks = []
    for idxArt, art in enumerate(artists):
        artTopTracks = spotify.artist_top_tracks(art['id'])
        songCount = numSongs(idxArt,numArt)
        playlistTracks+= artTopTracks['tracks'][:songCount]
    return playlistTracks
      
        
for possibleArtist in setlist:
    
    result = spotify.search(possibleArtist, limit=10, type='artist', market=None)
    possibleArtistMatches = result['artists']['items']
    
    foundArtist = FullArtistMatch(possibleArtistMatches, possibleArtist)
    if foundArtist:
        artistsDict[possibleArtist] = foundArtist
    # Check for a partial match
    else:
        # Add in partial name searching
        foundArtist = PartialArtistMatch(possibleArtist,slicer=rSlice)
        if foundArtist:
            artistsDict[possibleArtist] = foundArtist
        else:
            foundArtist = PartialArtistMatch(possibleArtist,slicer=lSlice)
            if foundArtist:
                artistsDict[possibleArtist] = foundArtist
            else:
                artistsDict[possibleArtist] = None
              
matchedArtists = [v for k,v in artistsDict.items() if v is not None]  
unmatchedArtists = [k for k,v in artistsDict.items() if v is None]

print('**Found %d/%d of possible artists.'%(len(matchedArtists),len(setlist)))
print('**The following possible artists could not be found: ',unmatchedArtists)

# TODO: Add prompt to resolve unmatchedArtists



playlistTracks = getTracksByArtists(matchedArtists)
    
# Create and add songs to playlist
playlist = spotify.user_playlist_create(USERNAME, PLAYLIST_NAME, public=True)
playlistTracksID = [track['id'] for track in playlistTracks]
spotify.user_playlist_add_tracks(USERNAME, playlist['id'], playlistTracksID)
