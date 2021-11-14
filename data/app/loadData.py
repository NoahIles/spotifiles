import os
import json
import models
# import pandas as pd 
from peewee import *
from playhouse.db_url import connect
# from playhouse.dataset import DataSet
from pydantic import BaseModel



class Storage:
    def __init__(self):
        self.db = connect(os.environ.get('DATABASE_URL'))
        # self.dataset = DataSet(self.db)
        self.db.close()

    def load_data_file(self, fileName):
        # The loaded data has two keys slice-info, and playlists
        with open(fileName, 'r') as f:
            data = json.load(f)
        # library_df = pd.DataFrame(data['playlists'])
        return data
    
    def insertTracks(self, playlist):
        # print(playlist['tracks'][0])
        for t in playlist['tracks']:
            t['artist_name'] = t['artist_name'].replace("'", "\\'")
            t['track_name'] = t['track_name'].replace("'", "\\'")
            t['album_name'] = t['album_name'].replace("'", "\\'")
            # $ Insert the track into the track table

#             self.db.execute_sql("""
# INSERT INTO tracks (t_artists, t_uri, t_artist_uri, t_name, t_album_uri, t_duration, t_album)
#  VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}')""".format(t['artist_name'],t['track_uri'],t['artist_uri'],t['track_name'],t['album_uri'],t['duration_ms'],t['album_name']))

            _track = models.Tracks.create(t_uri=t['track_uri'], t_artists=t['artist_name'], t_artist_uri=t['artist_uri'], t_name=t['track_name'], t_album_uri=t['album_uri'], t_duration=t['duration_ms'], t_album=t['album_name'])
            _track.save()
    def insertLibrary(self, fileName):
        slice = self.load_data_file(fileName)
        # TODO: Do Something with the slice information 
        s_info = slice['info']
        print("Reading in slice {} ".format(s_info['slice'])) 
        for pl in slice['playlists']:
            pl['name'] = pl['name'].replace("'", "\\'")
            # $ Insert the playlist into the playlist table 

            insertPlaylist = """
INSERT INTO playlists (pl_name, pl_modified, pl_num_tracks, pl_num_albums, pl_followers, pl_edits, pl_duration, pl_num_artists)
VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')""".format(pl['name'], pl['modified_at'], pl['num_tracks'], pl['num_albums'], pl['num_followers'], pl['num_edits'], pl['duration_ms'], pl['num_artists'])
            # print(insertPlaylist) 
            # self.db.execute_sql(insertPlaylist)
            # $ Insert the tracks
            self.insertTracks(pl)

if __name__ == "__main__":
    storage = Storage()
    storage.insertLibrary('/app/mpd.0-1.json')
    # slice = storage.load_data_file('/app/mpd.0-1.json')
    # tracks = slice['playlists'][0]
    # print(tracks.keys())
#     for t in tracks[1:]:
#         if t['duration_ms'] == 227600:
#             print("""
# INSERT INTO tracks (t_artists, t_uri, t_artist_uri, t_name, t_album_uri, t_duration, t_album)
#  VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}')""".format(t['artist_name'],t['track_uri'],t['artist_uri'],t['track_name'],t['album_uri'],t['duration_ms'],t['album_name']))
        
#     t = slice['playlists'][0]['tracks'][6]
