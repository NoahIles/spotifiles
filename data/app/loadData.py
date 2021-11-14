import os
import json
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

    # class PlaylistModel(BaseModel):
    #     class meta:
    #         database = self.db

    # class TrackModel(BaseModel):
    #     name: str
    #     track_uri: str
    #     artist: str
    #     artist_uri: str
    #     album: str
    #     album_uri: str
    #     duration: int
    #     class meta:
    #         database = self.db

    def load_data_file(self, fileName):
        # The loaded data has two keys slice-info, and playlists
        with open(fileName, 'r') as f:
            data = json.load(f)
        # library_df = pd.DataFrame(data['playlists'])
        return data
    
    def insertTracks(self, playlist):
        for t in pl['tracks'][1:]:
                t['artist_name'] = t['artist_name'].replace("'", "\\'")
                t['track_name'] = t['track_name'].replace("'", "\\'")
                t['album_name'] = t['album_name'].replace("'", "\\'")
                self.db.execute_sql("""
INSERT INTO tracks (t_artists, t_uri, t_artist_uri, t_name, t_album_uri, t_duration, t_album)
 VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}')""".format(t['artist_name'],t['track_uri'],t['artist_uri'],t['track_name'],t['album_uri'],t['duration_ms'],t['album_name']))


    def insertLibrary(self, fileName):
        slice = self.load_data_file(fileName)
        # TODO: Do Something with the slice information 
        s_info = slice['info']
        print("Reading in slice {} ".format(s_info['slice'])) 
        for pl in slice['playlists']:
            
            self.insertTracks(pl)
            
if __name__ == "__main__":
    storage = Storage()
    # storage.insertLibrary('/app/mpd.0-1.json')
    slice = storage.load_data_file('/app/mpd.0-1.json')
    tracks = slice['playlists'][0]
    print(tracks.keys())
#     for t in tracks[1:]:
#         if t['duration_ms'] == 227600:
#             print("""
# INSERT INTO tracks (t_artists, t_uri, t_artist_uri, t_name, t_album_uri, t_duration, t_album)
#  VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}')""".format(t['artist_name'],t['track_uri'],t['artist_uri'],t['track_name'],t['album_uri'],t['duration_ms'],t['album_name']))
        
#     t = slice['playlists'][0]['tracks'][6]


    # storage.insertLibrary('/app/mpd.0-1.json')


# {'pos': 0,
#  'artist_name': 'Missy Elliott',
#  'track_uri': 'spotify:track:0UaMYEvWZi0ZqiDOoHU3YI',
#  'artist_uri': 'spotify:artist:2wIVse2owClT7go1WT98tk',
#  'track_name': 'Lose Control (feat. Ciara & Fat Man Scoop)',
#  'album_uri': 'spotify:album:6vV5UrXcfyQD1wu4Qo2I9K',
#  'duration_ms': 226863,
#  'album_name': 'The Cookbook'}