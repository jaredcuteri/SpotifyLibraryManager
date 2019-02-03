
# This function removes old saved songs from the saved songs library and creates an archive playlist

from spotipyExt import * 


sp = initializeSpotifyToken('user-library-read user-library-modify playlist-modify-private playlist-read-private')

playlistName = 'Archive--2018'
#SavePlaylistToLibrary(sp,playlistName)
#RemovePlaylistFromLibrary(sp,playlistName)

# Derived Function Test
trackList = sp.current_user_saved_tracks()
SpotifyExt.printTracks(trackList['items'])

## ARCHIVING FLOW
#trackList = getAllSavedTracks(sp)

# Filter down to all tracks before a certain date
#trackListFiltered = tracksAddedBetween(trackList,20190101,20199999)

# Delete and recreate playlist
#erasePlaylistsByNames(sp, "Archive--2018")
#playlist = sp.user_playlist_create(DEFAULT_USERNAME, "Archive--2018", public=False)

#printTracks(trackListFiltered)
# Extract IDs from trackList
#idTrackList = [track['track']['uri'] for track in trackListFiltered]
#moveTracksFromLibToPlaylist(sp, idTrackList, playlist['id'])
