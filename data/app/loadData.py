import os
import json
import models as myModels
from peewee import *
from playhouse.db_url import connect
import pandas as pd
import time

mPL = myModels.Playlists
mT = myModels.Tracks
mPC = myModels.PlaylistContents

class Storage:
    def __init__(self):
        self.db = connect(os.environ.get('DATABASE_URL'))
        self.timeStamps = []
        self.db.close()

    def load_data_file(self, fileName):
        #$ The loaded data has two keys slice-info, and playlists
        self.timeStamps.append({"before-load-File", time.time()})
        with open(fileName, 'r') as f:
            data = json.load(f)
        self.timeStamps.append({"after-load-File", time.time()})
        return data
    
    def insertTracks(self, playlist, pl_id):
        num_tracks = len(playlist['tracks'])
        self.timeStamps.append({"begin-insert-pl-tracks" : time.time(), "pl_id" : pl_id, "num_tracks": num_tracks})
        #$ insert all the track data
        with self.db.atomic():
            for t_batch in chunked(playlist['tracks'], 100):
                #$ Clean the Track data
                for t in t_batch:
                    t['artist_name'] = t['artist_name'].replace("'", "\\'")
                    t['track_name'] = t['track_name'].replace("'", "\\'")
                    t['album_name'] = t['album_name'].replace("'", "\\'")
                    t.pop('pos', None)
                mT.insert_many(t_batch).on_conflict_replace().execute()
        
        self.timeStamps.append({"after-insert-pl-tracks" : time.time(), "pl_id" : pl_id, "num_tracks": num_tracks})
        #$ insert Playlist Content data 
        with self.db.atomic():
            _pl = mPL.get(mPL.pl_id == pl_id)
            for batch in chunked(playlist['tracks'], 100):
                pContents = []
                print("Inserting tracks for playlist {}".format(_pl.pl_name))
                for t in batch:
                    _tr = mT.get(mT.track_uri == t['track_uri']) # get track id obj from track table
                    pContents.append({'track_uri' : _tr, 'playlist_id' : _pl})

                    mPC.insert_many(pContents).on_conflict_replace().execute()
                    print("Inserting 100 Tracks")
        self.timeStamps.append({"after-insert-pl-content" : time.time(), "pl_id" : pl_id, "num_tracks": num_tracks})
        return

    def insertLibrary(self, fileName):
        sl = self.load_data_file(fileName)
        # TODO: Do Something with the slice information 
        s_info = sl['info']
        fields =[mPL.pl_name, mPL.pl_modified, mPL.pl_num_tracks, mPL.pl_num_albums, mPL.pl_followers, mPL.pl_edits, mPL.pl_duration, mPL.pl_num_artists, mPL.pl_id]
        print("Reading in slice {} ".format(s_info['slice']))
        with self.db.atomic():
            for chunk in chunked(sl['playlists'], 100):
                print("Inserting 100 Playlists")
                clean_pl_Chunk = []
                for pl in chunk:
                    # there is probably a better way to do this. 
                    cur = {}
                    cur['pl_name'] = pl.pop('name', None).replace("'", "\\'")
                    cur['pl_modified'] = pl.pop('modified_at',None)
                    cur['pl_num_tracks'] = pl.pop('num_tracks',None)
                    cur['pl_num_albums'] = pl.pop('num_albums',None)
                    cur['pl_followers'] = pl.pop('num_followers',None)
                    cur['pl_edits'] = pl.pop('edits',None)
                    cur['pl_duration'] = pl.pop('duration_ms',None)
                    cur['pl_num_artists'] = pl.pop('num_artists',None)
                    cur['pl_id'] = pl['pid']
                    # print(cur['pl_id'])
                    clean_pl_Chunk.append(cur)
                # $ Insert 100 playlists into the playlist table 
                mPL.insert_many(clean_pl_Chunk, fields=fields).on_conflict_replace().execute()
                # $ insert the tracks for each playlist
                for pl in chunk:
                    self.insertTracks(pl, pl['pid'])

if __name__ == "__main__":
    storage = Storage()
    some = storage.insertLibrary('/app/raw_data/mpd.slice.0-999.json')
    df = pd.DataFrame(some)
    print(df)
    # slice = storage.load_data_file('/app/mpd.0-1.json')
    # slice = slice['playlists']
    # print(testDel(slice))
    # print("idk")
    
    # tracks = slice['playlists'][0]
    # print(tracks.keys())
#     for t in tracks[1:]:
#         if t['duration_ms'] == 227600:
#             print("""
# INSERT INTO tracks (t_artists, t_uri, t_artist_uri, t_name, t_album_uri, t_duration, t_album)
#  VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}')""".format(t['artist_name'],t['track_uri'],t['artist_uri'],t['track_name'],t['album_uri'],t['duration_ms'],t['album_name']))
        
#     t = slice['playlists'][0]['tracks'][6]
