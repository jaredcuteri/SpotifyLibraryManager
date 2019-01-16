
# This function removes old saved songs from the saved songs library and creates an archive playlist

import sys
import spotipy
import spotipy.util as util

DEFAULT_USERNAME = "1232863129"

# Get Spotify Authorization and return user spotify token
def initializeSpotifyToken(scope,username=DEFAULT_USERNAME):
    token = util.prompt_for_user_token(username, scope)

    if token:
        sp = spotipy.Spotify(auth=token)
    else:
        raise Exception('Could not authenticate Spotify User: ', username)

    return sp

# Get all saved tracks
def getAllSavedTracks(sp):
    batchSize = 50
    idxOffset = 0
    trackList = []
    # First Call needed to determine number of tracks
    batchResults = sp.current_user_saved_tracks(limit=1,offset=0)
    while idxOffset < batchResults['total']:
        batchResults = sp.current_user_saved_tracks(limit=batchSize,offset=idxOffset)
        idxOffset += batchSize
        for item in batchResults['items']:
            trackList.append(item)
    return trackList

# Find all tracks added before a certain date (formated YYYYMMDD)
def tracksAddedBefore(trackList,date):
    trackListBeforeDate = []
    for track in trackList:
        data_added_str = track['added_at'][:10]
        date_added_int = int(data_added_str.replace("-",""))
        if date_added_int < date:
            trackListBeforeDate.append(track)
    return trackListBeforeDate

# Find all tracks added after a certain date (formated YYYYMMDD)
def tracksAddedAfter(trackList,date):
    trackListAfterDate = []
    for track in trackList:
        data_added_str = track['added_at'][:10]
        date_added_int = int(data_added_str.replace("-",""))
        if date_added_int >= date:
            trackListAfterDate.append(track)
    return trackListAfterDate

# Find all tracks between two dates (formatted YYYYMMDD)
def tracksAddedBetween(tracklist,afterDate,beforeDate):
    trackListAfter = tracksAddedAfter(trackList,afterDate)
    trackListBetween = tracksAddedBefore(trackListAfter,beforeDate)
    return trackListBetween

# Output the track list to the terminal
def printTracks(trackList):
    for track in trackList:
        print(track['track']['name'] + ' - ' + track['track']['artists'][0]['name'])

# Save long track list to playlist
def saveAllTracksToPlaylist(sp, trackListID, playlistID, username=DEFAULT_USERNAME):
    # TODO: Batch together 100 songs per call
    batchSize = 100
    tackListID = reversed(trackListID)
    batchedTrackListID = [trackListID[x+batchSize:x:-1] for x in range(0,len(trackListID),batchSize)]
    for trackID in batchedTrackListID:
        sp.user_playlist_add_tracks(username,playlistID,trackID)

# TODO: Alleviate 50 playlist limit
def erasePlaylistsByNames(sp, playlistsToDelete, username=DEFAULT_USERNAME):
    # Convert single string to one element list
    if type(playlistsToDelete) is str:
        playlistsToDelete = [playlistsToDelete]
    numPlaylistsDeleted = 0
    playlists = sp.user_playlists(username, limit=50, offset=0)
    for playlistToDelete in playlistsToDelete:
        for playlist in playlists['items']:
            if playlist['name'] == playlistToDelete:
                sp.user_playlist_unfollow(username, playlist['id'])
                numPlaylistsDeleted += 1
            else:
                pass
    return numPlaylistsDeleted




sp = initializeSpotifyToken('user-library-read playlist-modify-private playlist-read-private')

trackList = getAllSavedTracks(sp)

# Filter down to all tracks before a certain date
trackListBefore2017 = tracksAddedBefore(trackList,20170101)

# TODO: Need to delete playlist if already exists

# Delete and recreate playlist
erasePlaylistsByNames(sp, "Archive--2016")
playlist = sp.user_playlist_create(DEFAULT_USERNAME, "Archive--2016", public=False)

# Extract IDs from trackList
idTrackList = [track['track']['uri'] for track in trackListBefore2017]
saveAllTracksToPlaylist(sp, idTrackList, playlist['id'])

# Remove tracks from library

printTracks(trackListBefore2017)




# Create new playlist for archived tracks

# Unsave archived tracks from library
