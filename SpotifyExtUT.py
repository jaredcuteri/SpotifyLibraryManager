import unittest
from spotipyExt import * 

class TestCurrentUserSavedTracksMethod(unittest.TestCase):
    def setUp(self):
        # TODO: Determine why changing scope causes the first call thru to fail
        self.sp = initializeSpotifyToken('user-library-read')
        
    def test_Return20savedTracks(self):
        trackListOriginal = self.sp.current_user_saved_tracks_original(limit=20)
        trackList = self.sp.current_user_saved_tracks(limit=20)
        self.assertEqual(trackListOriginal['items'],trackList['items'])
    
    def test_Return5offsetSavedTracks(self):
        trackListOriginal = self.sp.current_user_saved_tracks_original(limit=5,offset=5)
        trackList = self.sp.current_user_saved_tracks(limit=5,offset=5)
        self.assertEqual(trackListOriginal['items'],trackList['items'])
        
    def test_ReturnAllTracks(self):
        trackListOriginal = getAllSavedTracks(self.sp)
        trackList = self.sp.current_user_saved_tracks()
        self.assertEqual(trackListOriginal['items'],trackList['items'])


# Supporting Functions

def getAllSavedTracks(sp):
        batchSize = 50
        idxOffset = 0
        trackList = dict.fromkeys(['href', 'items', 'limit', 'next', 'offset', 'previous', 'total'])
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

if __name__ == '__main__':
    unittest.main()
