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
IMAGE = 'posters/abgt_gorge.png'
PLAYLIST_NAME = 'ABGT Gorge'
# TODO: Add playlist length limit (adjust track scheduling to match total number of tracks)
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
weird_characters = ['\n','-','»','>','°','*','~','.']
for character in weird_characters:
    poster_text = poster_text.replace(character,'\n')

def promptUserForCorrections(initialText):
    ''' promptUserForCorrections is a GUI that allows the user to modify the text string
    
         Parameters:
            - initialText - initial string of text
    
         Return:
            - finalText - updated string of text submitted by the user
    
    '''
    import tkinter as tk
    from tkinter.scrolledtext import ScrolledText
    # TODO: Better formatting of window, more descriptive labels, add some colors
    finalText = None
    master = tk.Tk()
    master.geometry("300x450")
    L1 = tk.Label(master, text='List of Artists')
    L2 = tk.Label(master, text='Modify as necessary')
    L1.pack(fill=tk.X)
    L2.pack(fill=tk.X)
    e = ScrolledText(master)
    e.insert(tk.INSERT,initialText)
    e.pack(fill=tk.X)
    e.focus_set()
    
    def callback():
        nonlocal finalText
        finalText = e.get(1.0,tk.END)
        master.destroy()
        
    b = tk.Button(master, text = "Submit", width=10, command=callback)

    b.pack()

    tk.mainloop()
    
    return finalText

poster_text = promptUserForCorrections(poster_text)
#parse string into list of possible artists
# TODO: Make this more robust    
setlist = re.split('\W*\n+\W*',poster_text)
setlist = list(filter(None, setlist))

# Verify list of artists via spotipy (using popularity)
scope = 'user-library-read playlist-modify-private playlist-read-private'
spotify = spotipyExt.initializeSpotifyToken(scope)
artistsDict = dict.fromkeys(setlist)

rSlice = lambda x: x[:-1]
lSlice = lambda x: x[1:]
    
trackCountBasedOnPopularity = \
    lambda x,y :(math.ceil((1-(x/y))/0.25)+1)

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
              
matchedArtists = [v for k,v in artistsDict.items() if v is not None]  
unmatchedArtists = [k for k,v in artistsDict.items() if v is None]

print('+ Found %d/%d of possible artists.'%(len(matchedArtists),len(setlist)))
print('-- The following possible artists could not be found: ',unmatchedArtists)

# TODO: Add prompt to resolve unmatchedArtists



playlistTracks = spotify.getTracksByArtists(matchedArtists,numSongs=trackCountBasedOnPopularity)
    
# Create and add songs to playlist
playlist = spotify.user_playlist_create(USERNAME, PLAYLIST_NAME, public=True)
playlistTracksID = [track['id'] for track in playlistTracks]
spotify.user_playlist_add_tracks(USERNAME, playlist['id'], playlistTracksID)
print('+++ Playlist Generated: ',PLAYLIST_NAME)
print('++++ %d tracks added'%len(playlistTracksID))