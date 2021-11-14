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
    
    def insertLibrary(self, fileName):
        slice = self.load_data_file(fileName)
        # TODO: Do Something with the slice information 
        s_info = slice['info']
        print("Reading in slice {} ".format(s_info['slice'])) 
        for pl in slice['playlists']:
            for t in pl['tracks'][1:]:
                self.db.execute_sql("""
INSERT INTO tracks (t_artists, t_uri, t_artists_uri, t_name, t_album_uri, t_duration, t_album)
 VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}')""".format(t['artist_name'],t['track_uri'],t['artist_uri'],t['track_name'],t['album_uri'],t['duration_ms'],t['album_name']))
