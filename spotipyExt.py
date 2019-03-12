import sys
import spotipy
import spotipy.util as util

DEFAULT_USERNAME = "1232863129"

class SpotifyExt(spotipy.Spotify):
    '''
    SpotifyExt is an extension of the spotipy.Spotify class that allows "limitless" 
    getter and setter functions. For example: current_user_saved_tracks is limited
    to pulling 50 tracks at a time with spotipy, spotipyExt removes this limit.
    
    '''
    __doc__ += spotipy.Spotify.__doc__     
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        
    # TODO: Create decorator (for saved tracks and user playlists because wrapping is identical)
    def current_user_saved_tracks(self, limit=float('inf'), offset=0):
        ''' Gets an unlimited list of the tracks saved in the current
            authorized user's "Your Music" library

            Parameters:
                - limit - the number of tracks to return
                - offset - the index of the first track to return

        '''

        # These keys are now useless because we're returning all items
        savedTracks = dict.fromkeys(['href', 'items', 'limit', 'next',\
                                'offset', 'previous', 'total'])
        
        # Maximum batch size allowed Spotipy API
        batchSize = 50
        savedTracks['items'] = []
        
        # First Call needed to determine number of tracks
        # TODO: refactor so there isn't a dangling call
        batchResults = super().current_user_saved_tracks(limit=1,offset=0)
        
        savedTracks['total'] = batchResults['total']
        
        # Calculate number of tracks to be processed
        numTracksToProcess = min(savedTracks['total'],limit)
    
        # Return savedTrackss in batches and append to savedTrackss
        for idxBatch in range(offset,numTracksToProcess+offset,batchSize):
            batchResults = super().current_user_saved_tracks(limit=batchSize,\
                                                             offset=idxBatch)
            for idxTrack, item in enumerate(batchResults['items'],idxBatch):
                if idxTrack < numTracksToProcess+offset:
                    savedTracks['items'].append(item)            
        return savedTracks
    
    def user_playlist_add_tracks(self, user, playlist_id, tracks, position=None):
        ''' Adds an unlimited number of tracks to a playlist

            Parameters:
                - user - the id of the user
                - playlist_id - the id of the playlist
                - tracks - a list of track URIs, URLs or IDs
                - position - the position to add the tracks
            Returns:
                - numTracksAdded - number of tracks added to playlist
        '''
        # TODO: Add parsing for  dictionary of tracks
        # tracks must be a list of track id's
        numTracksAdded = 0
        # Max allowed by spotify api
        batchSize = 100
        
        # TODO: Set order of add by date added
        track_batches = [tracks[x:x+batchSize] for x in \
                              range(0,len(tracks)+1,batchSize)]
                          
        for track_batch in track_batches:
            result = super().user_playlist_add_tracks(user,playlist_id,track_batch)
            numTracksAdded += len(track_batch)
        return numTracksAdded
    
    def user_playlists(self, user, limit=float('inf'), offset=0):
        ''' Gets an unlimited number of user playlists
            
            Parameters:
                - user - username to pull playlists from
                - limit - limit number of playlists returned
                - offset - playlist index offest
            Returns:
                - result - playlists
        '''
        # These keys are now useless because we're returning all items
        playlists = dict.fromkeys(['href', 'items', 'limit', 'next',\
                                'offset', 'previous', 'total'])
        
        # Maximum batch size allowed Spotipy API
        batchSize = 50
        playlists['items'] = []
        
        # First Call needed to determine number of playlists
        # TODO: refactor so there isn't a dangling call
        batchResults = super().user_playlists( user, limit=1,offset=0)
        
        playlists['total'] = batchResults['total']
        
        # Calculate number of playlists to be processed
        numPlaylistsToProcess = min(playlists['total'],limit)
    
        # Return results in batches and append to results
        for idxBatch in range(offset,numPlaylistsToProcess+offset,batchSize):
            batchResults = super().user_playlists( user, limit=batchSize,\
                                                             offset=idxBatch)
            for idxPlaylist, item in enumerate(batchResults['items'],idxBatch):
                if idxPlaylist < numPlaylistsToProcess+offset:
                    playlists['items'].append(item)            
        return playlists
           
    def tracksAddedBefore(self, trackList, date):
        ''' Return list of tracks added before date (YYYYMMDD)

            Parameters:
                - trackList - list of tracks
                - date - cutoff date (formatted YYYYMMDD, YYYYMM, or YYYY)
            Returns:
                - trackListBeforeDate - list of tracks added before date
        '''
        # Input Type handling
        if type(date) == int:
            date = str(date)
        elif type(date) == int:
            pass
        else:
            raise TypeError('Date parameter to tracksAddedBefore must \
                             be str or int type, %s provided', type(date))
                             
        # Round down if date truncated
        date.ljust(8,'0')
        date = int(date)
        
        trackListBeforeDate = []
        for track in trackList:
            data_added_str = track['added_at'][:10]
            date_added_int = int(data_added_str.replace("-",""))
            if date_added_int < date:
                trackListBeforeDate.append(track)
        return trackListBeforeDate

    def tracksAddedAfter(self, trackList, date):
        ''' Return list of tracks added after date (YYYYMMDD)

            Parameters:
                - trackList - list of tracks
                - date - cutoff date (formatted YYYYMMDD, YYYYMM, or YYYY)
            Returns:
                - trackListAfterDate - list of tracks added after date
        '''
        # Input Type handling
        if type(date) == int:
            date = str(date)
        elif type(date) == int:
            pass
        else:
            raise TypeError('Date parameter to tracksAddedAfter must \
                             be str or int type, %s provided', type(date))    
        # Round up if date truncated
        date.ljust(8,'9')
        date = int(date)
        
        trackListAfterDate = []
        for track in trackList:
            data_added_str = track['added_at'][:10]
            date_added_int = int(data_added_str.replace("-",""))
            if date_added_int >= date:
                trackListAfterDate.append(track)
        return trackListAfterDate

    def tracksAddedBetween(self, tracklist, afterDate, beforeDate):
        ''' Return list of tracks added between dates

            Parameters:
                - trackList  - list of tracks
                - afterDate  - cutoff date (formatted YYYYMMDD, YYYYMM, or YYYY)
                - beforeDate - cutoff date (formatted YYYYMMDD, YYYYMM, or YYYY)
            Returns:
                - trackListBetween - list of tracks added between dates
        '''
        trackListAfter = tracksAddedAfter(trackList,afterDate)
        trackListBetween = tracksAddedBefore(trackListAfter,beforeDate)
        return trackListBetween

    def printTracks(self, trackList):
        ''' Prints tracks in human readable format
            
            Parameters:
                - trackList - list of track objects
        '''
        for track in trackLists:
            print(track['track']['name'] + ' - ' 
                + track['track']['artists'][0]['name'])
 
    def erasePlaylistsByNames(self, playlistsToDelete, user=DEFAULT_USERNAME):
        ''' Erase playlists that contain string or substring in there name
        
            Parameters:
                - playlistsToDelete - string or list of strings
                - user - id of user
            Returns:
                - numPlaylistsDeleted - number of playlists deleted
        '''
        # Convert single string to one element list
        if type(playlistsToDelete) is str:
            playlistsToDelete = [playlistsToDelete]
        numPlaylistsDeleted = 0
        # TODO: Alleviate 50 playlist limit
        playlists = self.user_playlists(user, limit=50, offset=0)
        for playlistToDelete in playlistsToDelete:
            for playlist in playlists['items']:
                if playlistToDelete in playlist['name']:
                    self.user_playlist_unfollow(user, playlist['id'])
                    numPlaylistsDeleted += 1
                else:
                    pass
        return numPlaylistsDeleted

    def moveTracksFromLibToPlaylist(self, trackListID, playlistID):
        ''' Move tracks from library to playlist.
        
            Parameters:
                - trackListID - list of track id's
                - playlistID - id of destination playlist
            Returns:
                - flagAllTracksMoved - bool on whether tracks were successfully added
        '''
        # Add tracks to playlist
        numTracksAdded = saveAllTracksToPlaylist(self, trackListID, playlistID)
        
        # Verify all tracks were added before deleting from library
        numTracksDeleted = 0
        if numTracksAdded == len(trackListID):
            # TODO: Update so it's not calling sp every track (is this function batch limited?)
            for track in trackListID:
                result = self.current_user_saved_tracks_delete([track])
                numTracksDeleted += 1
            print('moveTracksFromLibToPlaylist: %d tracks added / %d tracks deleted'\
                  %(numTracksAdded,numTracksDeleted))
            flagAllTracksMoved = True
        else:
            print('Not all tracks were added to the new playlist. \
                   Tracks will remain saved in Library')
            flagAllTracksMoved = False
            
        return flagAllTracksMoved

    def getTrackIDsFromPlaylistName(self, playlistName, username=DEFAULT_USERNAME):
        ''' Get all tracks from playlist by name
        
            Paramters:
                - playlistName - name of playlist
        
            Returns:
                - trackList - list of tracks
        '''
        playlists = self.user_playlists(username, limit=50, offset=0)
        for playlist in playlists['items']:
            if playlist['name'] == playlistName:
                targetPlaylist = playlist
        numTracks = targetPlaylist['tracks']['total']
        batchSize = 100
        trackList = []
        for idxOffset in range(0,numTracks,batchSize):
            tracks_batch = self.user_playlist_tracks(username,targetPlaylist['id'],\
                                        fields=None,limit=batchSize,offset=idxOffset)
            for track in tracks_batch['items']:
                trackList.append(track['track'])
        return trackList

    def savePlaylistToLibrary(self, playlistName):
        ''' Save all tracks from playlist to library
        
            Parameters:
                - playlistName - playlist name to pull tracks 
        '''
        trackIDsFromPlaylist = GetTrackIDsFromPlaylistName(self,playlistName,username=DEFAULT_USERNAME)
        for track in trackIDsFromPlaylist:
            self.current_user_saved_tracks_add([track])

    def removePlaylistFromLibrary(self, playlistName):
        ''' Remove all tracks from playlist in library
        
            Parameters:
                - playlistName - playlist name which contains tracks to remove
                                 from library
        '''
        trackIDsFromPlaylist = GetTrackIDsFromPlaylistName(self,playlistName,username=DEFAULT_USERNAME)
        for track in trackIDsFromPlaylist:
            self.current_user_saved_tracks_delete([track])
    
    @staticmethod
    def compareNames(name1, name2):
        import unicodedata
        def removeAccents(string):
             return ''.join((c for c in unicodedata.normalize('NFD', string) \
                                        if unicodedata.category(c) != 'Mn'))
        def removeCasing(string):
            return string.lower()
            
        def fixName(string):
            return removeCasing(removeAccents(string))
            
        if fixName(name1) == fixName(name2):
            return True
        else:
            return False
    
    @staticmethod
    def fullArtistMatch(artistList, possibleArtist):
        ''' fullArtistMatch takes a list of possible artists and compares it 
                to the possible artists name
    
            Parameters
                -possibleArtistMatches: list of artist objects
                -possibleArtist: string of artist name
    
            Returns
               - matched artist object or none
    
        '''
        # sort artists by popularity
        popThresh = 0 # Popularity Threshold
        artistList = [ x for x in artistList if x['popularity']>=popThresh]
        artistList.sort(key=lambda x: x['popularity'], reverse=True)
        # Check for perfect matches
        # TODO: DRY SpotifyExt should be replaced with self.__class__ (but self isnt in scope)
        for artist in artistList:
            if SpotifyExt.compareNames(artist['name'], possibleArtist):
                return artist
        else:
            return None

    # TODO: Make into static method
    def partialArtistMatch(self,FullName,PartialName=None,slicer=lambda x: x[:-1]):
        ''' partialArtistMatch recursively attempts to find an artist by
                 slicing part of the string
            
            Parameters
                - FullName: Original string
                - PartialName: current string to be evaluated
                - slicer: slicing function for "trimming" down string
        
            Returns:
              - final_result: artist found or none
        
        '''
        print('**In Partial Artist Match')
        # Initializing PartialName for recursion
        if PartialName==None:
            PartialName = FullName
        
        subStringRatio = len(PartialName)/len(FullName)
        
        # Popularity cutoff threshhold
        popThresh = 0
        
        # TODO: not ideal to create spotipy objects for each call
        found_artist = self.search(PartialName,limit=1,type='artist')
    
        # Exit if we've trimmed more than 50% of the name
        if subStringRatio<0.5:
            return None
        # Check for match
        # TODO: is it necessary to check the name again? Does search only return perfect matches?
        # TODO: DRY SpotifyExt should be replaced with self.__class__ (but self isnt in scope)
        elif found_artist['artists']['items'] \
         and SpotifyExt.compareNames(found_artist['artists']['items'][0]['name'], PartialName) \
         and found_artist['artists']['items'][0]['popularity'] >= popThresh:
            return found_artist['artists']['items'][0]   
        # Recurse with partial name
        else:
            final_result = self.partialArtistMatch(FullName,slicer(PartialName),slicer=slicer)
            return final_result
    
    # TODO: Make into static method        
    def getTracksByArtists(self, artists,numSongs=1):
        ''' getTracksByArtists returns a list of tracks containing top tracks from artists
    
            Parameters:
                artists - list of spotipy artists 
                numSongs - function provides number of tracks to add from each artist
    
            Returns:
                playlistTracks - list of tracks
        '''
        # Sort Artists By Popularity
        artists.sort(key=lambda x: x['popularity'], reverse=True)
        # Determine Number of Artists
        numArt=len(artists)
        playlistTracks = []
        for idxArt, art in enumerate(artists):
            # TODO: not ideal to create spotipy objects for each call
            artTopTracks = self.artist_top_tracks(art['id'])
            songCount = numSongs(idxArt,numArt)
            playlistTracks+= artTopTracks['tracks'][:songCount]
        return playlistTracks

    # TODO: Clean up search strategy
    def getTrackID(self, trackName, artistName=None):
        tracks = self.search(trackName,type='track')
        if tracks['tracks']['items']:
            if len(tracks['tracks']['items'])>1:
                # Use artistname to resolve    
                tracks = self.search(artistName + ' ' + trackName,limit=1,type='track')
                if not tracks['tracks']['items']:
                    tracks = self.search(trackName,limit=1,type='track')   
            return tracks['tracks']['items'][0]['id']
        else:
            return None

# Get Spotify Authorization and return user spotify token
def initializeSpotifyToken(scope,username=DEFAULT_USERNAME):
    ''' Initialize the Spotify Authorization token with specified scope
    
        Parameters:
            - scope - Authorization scope
            - username - authorized username
    
        Returns:
            - sp - authorized spotipy object
    '''
    token = util.prompt_for_user_token(username, scope)
    if token:
        sp = SpotifyExt(auth=token)
    else:
        raise Exception('Could not authenticate Spotify User: ', username)

    return sp

