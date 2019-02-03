import sys
import spotipy
import spotipy.util as util

DEFAULT_USERNAME = "1232863129"
# TODO: Update docstring inheritance to better utilized super()

class SpotifyExt(spotipy.Spotify):
    '''
    SpotifyExt is an extension of the spotipy.Spotify class that allows "limitless" 
    getter and setter functions. For example: current_user_saved_tracks is limited
    to 50 tracks at a time with spotipy, spotipyExt removes this limit.
    
    '''
    __doc__ += spotipy.Spotify.__doc__ 
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        
    # Limitless get current user saved tracks
    def current_user_saved_tracks(self,limit=float('inf'),offset=0):
        ''' Gets an unlimited list of the tracks saved in the current
            authorized user's "Your Music" library

            Parameters:
                - limit - the number of tracks to return
                - offset - the index of the first track to return

        '''

        # These keys are now useless because we're returning all items
        result = dict.fromkeys(['href', 'items', 'limit', 'next',\
                                'offset', 'previous', 'total'])
        
        # Maximum batch size allowed Spotipy API
        batchSize = 50
        result['items'] = []
        
        # First Call needed to determine number of tracks
        # TODO: refactor so there isn't a dangling call
        batchResults = super().current_user_saved_tracks(limit=1,offset=0)
        
        result['total'] = batchResults['total']
        
        # Calculate number of tracks to be processed
        numTracksToProcess = min(result['total'],limit)
    
        # Return results in batches and append to results
        for idxBatch in range(offset,numTracksToProcess+offset,batchSize):
            batchResults = super().current_user_saved_tracks(limit=batchSize,\
                                                             offset=idxBatch)
            for idxTrack, item in enumerate(batchResults['items'],idxBatch):
                if idxTrack < numTracksToProcess+offset:
                    result['items'].append(item)            
        return result
    
    # Limitless save all tracks to playlist
    def user_playlist_add_tracks(self,user, playlist_id, tracks, position=None):
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

    # TODO: override user_playlists to be limitless
    
    def tracksAddedBefore(self, trackList,date):
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

    def tracksAddedAfter(self, trackList,date):
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

    def tracksAddedBetween(tracklist,afterDate,beforeDate):
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

    def getTrackIDsFromPlaylistName(self,playlistName,username=DEFAULT_USERNAME):
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

    def savePlaylistToLibrary(self,playlistName):
        ''' Save all tracks from playlist to library
        
            Parameters:
                - playlistName - playlist name to pull tracks 
        '''
        trackIDsFromPlaylist = GetTrackIDsFromPlaylistName(self,playlistName,username=DEFAULT_USERNAME)
        for track in trackIDsFromPlaylist:
            self.current_user_saved_tracks_add([track])

    def removePlaylistFromLibrary(self,playlistName):
        ''' Remove all tracks from playlist in library
        
            Parameters:
                - playlistName - playlist name which contains tracks to remove
                                 from library
        '''
        trackIDsFromPlaylist = GetTrackIDsFromPlaylistName(self,playlistName,username=DEFAULT_USERNAME)
        for track in trackIDsFromPlaylist:
            self.current_user_saved_tracks_delete([track])



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
