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
        self.timeStamps = {}
        self.db.close()

    def load_data_file(self, fileName):
        #$ The loaded data has two keys slice-info, and playlists
        self.timeStamps["before-load-File"] =  time.time()
        with open(fileName, 'r') as f:
            data = json.load(f)
        self.timeStamps["after-load-File"] =  time.time()
        return data
    
    #$ insert all the track data
    def insertTracks(self, tracks, pl_id):
        num_tracks = len(tracks)
        self.timeStamps["begin-insert-pl-content"] = { "timestamp": time.time(), "pl_id" : pl_id, "num_tracks": num_tracks}        
        #$ insert Playlist Content data 
        pContents = []
        for t in tracks:
            pContents.append({'track_uri': t['track_uri'], 'playlist_id': pl_id})
        self.timeStamps["finish-clean-pContent"] = { "timestamp": time.time(), "pl_id" : pl_id, "num_tracks": num_tracks}        
        mPC.insert_many(pContents).on_conflict_replace().execute()
        self.timeStamps["after-insert-pl-content"] = { "timestamp": time.time(), "pl_id" : pl_id, "num_tracks": num_tracks}        
        mT.insert_many(tracks).on_conflict_replace().execute()
        self.timeStamps["after-insert-pl-content"] = { "timestamp": time.time(), "pl_id" : pl_id, "num_tracks": num_tracks}        
        return

    # Takes a data slice from mpd and cleans it up
    def cleanData(self, data):
        clean_pl = []
        for pl in data['playlists']:
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
            #$ Clean the Track data
            for t in pl['tracks']:
                t['artist_name'] = t['artist_name'].replace("'", "\\'")
                t['track_name'] = t['track_name'].replace("'", "\\'")
                t['album_name'] = t['album_name'].replace("'", "\\'")
                t.pop('pos', None)

            cur['tracks'] = pl.pop('tracks', None)
            clean_pl.append(cur)
        return clean_pl


    def insertLibrary(self, fileName):
        sl = self.load_data_file(fileName)
        # TODO: Do Something with the slice information 
        s_info = sl['info']
        fields =[mPL.pl_name, mPL.pl_modified, mPL.pl_num_tracks, mPL.pl_num_albums, mPL.pl_followers, mPL.pl_edits, mPL.pl_duration, mPL.pl_num_artists, mPL.pl_id]
        print("Reading in slice {} ".format(s_info['slice']))
        plStr = fileName.split('.')[2]
        pl_count = int(plStr[:plStr.find('-')])
        clean_pl = self.cleanData(sl)

        with self.db.atomic():
            #TODO optimize chunk size for mysql / engine
            for chunk in chunked(clean_pl, 250):
                print('\nInserting Playlists {}-{}'.format(pl_count, pl_count + len(chunk)))
                pl_count += len(chunk)
                # $ insert the tracks for each playlist
                for pl in chunk:
                    print("Inserting tracks for playlist {}".format(pl['pl_name']))
                    self.insertTracks(pl.pop('tracks', None), pl['pl_id'])
                # $ Insert 100 playlists into the playlist table 
                mPL.insert_many(chunk, fields=fields).on_conflict_replace().execute()
    

    # Write the stats to a file store within a log directory write to a new log every time
    def printStats(self):
        with open('logs/stats.txt', 'w+') as f:
            for t in self.timeStamps:
                f.write(str(t) + '\n')
        return self.timeStamps

    def loadAllData(self):
    # for each json file in the data directory
        self.timestamps["begin-load-all-data"] = time.time()
        for f in os.listdir('/app/raw_data'):
            if f.endswith('.json'):
                self.timeStamps["begin-load-file"] ={"timestamp": time.time(), "fileName" : f}
                s.insertLibrary('/app/raw_data/' + f)
                self.timeStamps["end-load-file"] ={"timestamp": time.time(), "fileName" : f}
    
    def loadOneFile(fileName = 'mpd.slice.0-999.json'):
        self.insertLibrary('/app/raw_data/' + fileName)

# ===============
# Chunk Size = 500
# Load_10,000 - 12.57 minutes
# ===============


def timeTest(funtion):
    bTime = time.time()
    funtion()
    eTime = time.time()
    print("Time to run function: {} Minutes".format(float(eTime - bTime) / 60))

if __name__ == "__main__":
    if s is None:
        s = Storage()
    basefileName = '/app/raw_data/mpd.slice.'
    # ask the user if they would like to run tests on a single data set?
    # if yes, run the test
    fileName = None
    if input("Would you like to run a test on a single data set? (y/n) ") == 'y':
        testNum = int(input("Enter the test number 0-9: "))
        if(testNum < 0 or testNum > 9):
            print("Invalid test number")
            exit()
        elif(testNum == 0):
            fileName = basefileName + '0-999.json'
        else: 
            fileName = basefileName + str(testNum) + '000-' + str(testNum) + '.json'
    
    
        if fileName is not None:
            timeTest(loadOneFile(fileName))

    # ask the user if they would like to run tests on entire data set 
    elif input("Would you like to run tests on the entire data set? (y/n) ") == 'y':
        timeTest(loadAllData)

# TODO: add foreign key constraint to the tables after inserting all data
# TODO: Graph the data/time to see how long it takes to load the data
# TODO: Finish the web API 
# TODO: Pretty looking web interface? 
# TODO: Make import data more efficient