import unittest
from spotipyExt import * 
import json 

CLIENT_SECRETS_FILE = "./client_secret.json" #This is the name of your JSON file

with open(CLIENT_SECRETS_FILE,'r') as fid:
    credz = json.load(fid)
    UID = credz['userconfig']['uid']

class TestSpotipyExt(unittest.TestCase):
    
    test_tag = '__test__'
    
    def setUp(self):
        # TODO: Determine why changing scope causes the first call thru to fail
        # Initialize spotify and spotifyExt objects
        scope = 'user-library-read playlist-modify-private playlist-read-private'
        token = util.prompt_for_user_token(username=UID, scope=scope)
        if token:
            self.spotify  = spotipy.Spotify(auth=token)
        else:
            raise Exception('Could not authenticate Spotify User: ', UID)
        
        self.spotifyExt = initializeSpotifyToken(scope, UID)
        self.spotifyExt.username = UID
        
    def test_Return20savedTracks(self):
        trackListOriginal = self.spotify.current_user_saved_tracks(limit=20)
        trackList = self.spotifyExt.current_user_saved_tracks(limit=20)
        
        self.assertEqual(trackListOriginal['items'],trackList['items'])
    
    def test_Return5offsetSavedTracks(self):
        trackListOriginal = self.spotify.current_user_saved_tracks(limit=5,offset=5)
        trackList = self.spotifyExt.current_user_saved_tracks(limit=5,offset=5)
        
        self.assertEqual(trackListOriginal['items'],trackList['items'])
        
    def test_ReturnAllTracks(self):
        trackListOriginal = getAllSavedTracks(self.spotify)
        trackList = self.spotifyExt.current_user_saved_tracks()
        
        self.assertEqual(trackListOriginal['items'],trackList['items'])

    def test_SaveAllTracksToPlaylist(self):
        
        # Create 2 Test playlists
        plNameOriginal = self.test_tag+"saveTracksToPlaylistOriginal"
        plName         = self.test_tag+"saveTracksToPlaylistExt"
        playlistOriginal = self.spotify.user_playlist_create(self.spotifyExt.username,\
                                        plNameOriginal, public=False)
        playlist         = self.spotifyExt.user_playlist_create(self.spotifyExt.username,\
                                        plName , public=False)
                                        
        #TODO: Change to pull a default track list                        
        trackList = getAllSavedTracks(self.spotify) 
        # Create list of track ids
        trackListID = [track['track']['id'] for track in trackList['items']]
        
        # Save Tracks to Playlist
        saveAllTracksToPlaylist(self,playlistOriginal['id'],trackListID)
        self.spotifyExt.user_playlist_add_tracks(self.spotifyExt.username,playlist['id'],trackListID)
        
        # pull playlist data
        playlistOriginal = self.spotify.user_playlist(self.spotifyExt.username,playlistOriginal['id'])
        playlist = self.spotifyExt.user_playlist(self.spotifyExt.username,playlist['id'])
        
        tracksOriginal = [ track['track']  for track in playlistOriginal['tracks']['items']]
        tracks = [ track['track']  for track in playlist['tracks']['items']]
        self.assertEqual(tracksOriginal,tracks)
    
    # TODO: Add user playlists test ( add bunch of playlists and check that they are found) 
        
    def tearDown(self):
        # Find all playlists starting __test__
        playlists = self.spotify.user_playlists(self.spotifyExt.username)
        testPlaylistsID = [playlist['id'] for playlist in playlists['items'] if self.test_tag in playlist['name']]
        
        # delete all playlists found with __test__ tag
        for testPlaylist in testPlaylistsID:
            self.spotify.user_playlist_unfollow(self.spotifyExt.username,testPlaylist)
        
        
def getAllSavedTracks(sp):
        batchSize = 50
        idxOffset = 0
        trackList = dict.fromkeys(['href', 'items', 'limit', 'next', \
                                   'offset', 'previous', 'total'])
        trackList['items'] = []
        
        # First Call needed to determine number of tracks
        batchResults = sp.current_user_saved_tracks(limit=1,offset=0)
        trackList['total'] = batchResults['total']
        while idxOffset < batchResults['total']:
            batchResults = sp.current_user_saved_tracks(limit=batchSize,offset=idxOffset)
            idxOffset += batchSize
            for item in batchResults['items']:
                trackList['items'].append(item)
        return trackList

def saveAllTracksToPlaylist(self, playlistID, trackListID):
        numTracksAdded = 0
        batchSize = 100
        # TODO: Set order of add by date added
        batchedTrackListID = [trackListID[x:x+batchSize] for x in \
                              range(0,len(trackListID)+1,batchSize)]
                              
        for trackID in batchedTrackListID:
            result = self.spotify.user_playlist_add_tracks(self.spotifyExt.username,playlistID,trackID)
            numTracksAdded += len(trackID)
        return numTracksAdded



if __name__ == '__main__':
    unittest.main()
