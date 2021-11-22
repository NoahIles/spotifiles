import os
import json
import time
import logging
from logging.handlers import RotatingFileHandler
import models as myModels
from peewee import *
from playhouse.db_url import connect
import pandas as pd

import my_timer

mPL = myModels.Playlists
mT = myModels.Tracks
mPC = myModels.PlaylistContents

class Storage:
    def __init__(self):
        self.db = connect(os.environ.get('DATABASE_URL'))
        self.timeStamps = {}
        self.logger = logging.getLogger('myLogger')
        self.initLogger()
        self.db.close()

    def initLogger(self):
        self.logger.setLevel(logging.DEBUG)
        # create a file handler
        handler = RotatingFileHandler('logs/mylog.log', maxBytes=10000, backupCount=5)
        handler.setLevel(logging.DEBUG)
        # create a logging format
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.handler.setFormatter(formatter)
        # add the handlers to the logger
        self.logger.addHandler(handler)
        return self

    def __del__(self):
        self.db.close()
        self.writeLogs()
    
    # write the timestamps to the logger file
    def writeLogs(self):
        self.logger.info("HELLO?")
        # self.logger.info(self.timeStamps)
        return

    # $ The loaded data has two keys slice-info, and playlists
    def load_data_file(self, fileName):
        # test if the file exists then load it
        data = None
        if os.path.isfile(fileName):
            with open(fileName, 'r') as f:
                data = json.load(f)
        else:
            print("File {} does not exist".format(fileName))
        return data

    # $ insert all the track data
    def insertTracks(self, tracks, pl_id):
        num_tracks = len(tracks)
        self.timeStamps["begin-insert-pl-content"] = {
            "timestamp": time.time(), "pl_id": pl_id, "num_tracks": num_tracks}
        # $ insert Playlist Content data
        pContents = []
        for t in tracks:
            pContents.append(
                {'track_uri': t['track_uri'], 'playlist_id': pl_id})
        self.timeStamps["finish-clean-pContent"] = {
            "timestamp": time.time(), "pl_id": pl_id, "num_tracks": num_tracks}
        mPC.insert_many(pContents).on_conflict_ignore().execute()
        self.timeStamps["after-insert-pl-content"] = {
            "timestamp": time.time(), "pl_id": pl_id, "num_tracks": num_tracks}
        mT.insert_many(tracks).on_conflict_ignore().execute()
        self.timeStamps["after-insert-pl-content"] = {
            "timestamp": time.time(), "pl_id": pl_id, "num_tracks": num_tracks}
        return

    # Takes a data slice from mpd and cleans it up
    def cleanData(self, data):
        clean_pl = []
        for pl in data['playlists']:
            # there is probably a better way to do this.
            cur = {}
            cur['pl_name'] = pl.pop('name', None).replace("'", "\\'")
            cur['pl_modified'] = pl.pop('modified_at', None)
            cur['pl_num_tracks'] = pl.pop('num_tracks', None)
            cur['pl_num_albums'] = pl.pop('num_albums', None)
            cur['pl_followers'] = pl.pop('num_followers', None)
            cur['pl_edits'] = pl.pop('edits', None)
            cur['pl_duration'] = pl.pop('duration_ms', None)
            cur['pl_num_artists'] = pl.pop('num_artists', None)
            cur['pl_id'] = pl['pid']
            # $ Clean the Track data
            for t in pl['tracks']:
                t['artist_name'] = t['artist_name'].replace("'", "\\'")
                t['track_name'] = t['track_name'].replace("'", "\\'")
                t['album_name'] = t['album_name'].replace("'", "\\'")
                t.pop('pos', None)

            cur['tracks'] = pl.pop('tracks', None)
            clean_pl.append(cur)
        return clean_pl

    def handleSliceInfo(self, sliceInfo):
        print("Reading in slice {} ".format(sliceInfo['slice']))
        # TODO: Do Something with the slice information
        return

    def insertLibrary(self, fileName, chunkSize=250, verbose=False):
        self.timeStamps["before-load-File"] = time.time()
        sl = self.load_data_file(fileName)
        self.timeStamps["after-load-File"] = time.time()
        try:
            self.handleSliceInfo(sl['info'])
        except:
            print("CAUGHT EXCEPTION!!!!: ")
            print("No slice info")
            print("Available Keys")
            for k in sl.keys():
                print(k)
            exit(1)

        clean_pl = self.cleanData(sl)
        pl_count = int((fileName.split('.')[2]).split('-')[0])

        fields = [mPL.pl_name, mPL.pl_modified, mPL.pl_num_tracks, mPL.pl_num_albums,
                  mPL.pl_followers, mPL.pl_edits, mPL.pl_duration, mPL.pl_num_artists, mPL.pl_id]
        with self.db.atomic():
            # TODO optimize chunk size for mysql / engine
            for chunk in chunked(clean_pl, chunkSize):
                print('\nInserting Playlists {}-{}'.format(pl_count,
                      pl_count + len(chunk)))
                pl_count += len(chunk)
                # $ insert the tracks for each playlist
                for pl in chunk:
                    if verbose:
                        print("Inserting tracks for playlist {}".format(
                        pl['pl_name']))
                    self.insertTracks(pl.pop('tracks', None), pl['pl_id'])
                # $ Insert 100 playlists into the playlist table
                mPL.insert_many(
                    chunk, fields=fields).on_conflict_ignore().execute()

    # Write the stats to a file store within a log directory write to a new log every time

    def printStats(self):
        with open('logs/stats.txt', 'w+') as f:
            for t in self.timeStamps:
                f.write(str(t) + '\n')
        return self.timeStamps

    @my_timer.timeit
    def loadAllData(self):
        # for each json file in the data directory
        self.timestamps["begin-load-all-data"] = time.time()
        for f in os.listdir('/app/raw_data'):
            if f.endswith('.json'):
                self.timeStamps["begin-load-file"] = {
                    "timestamp": time.time(), "fileName": f}
                s.insertLibrary('/app/raw_data/' + f)
                self.timeStamps["end-load-file"] = {
                    "timestamp": time.time(), "fileName": f}

    @my_timer.timeit
    def loadOneFile(self, fileName):
        self.insertLibrary('/app/raw_data/' + fileName)

    def fetchCounts(self):
        with self.db.atomic():
            return {
                "Playlist content": mPC.select().count(),
                "Tracks": mT.select().count(),
                "Playlists": mPL.select().count()
            }

# ===============
# Chunk Size = 500
# Load_10,000 - 12.57 minutes
# ===============

if __name__ == "__main__":
    try: 
        s = Storage()
        s.logger.info("Storage Initialized")
    except Exception as e:
        print(e)
        print("Storage Failed to initialize")
        # s.logger.error("Storage Failed to initialize")
        exit(1)
    status_before = s.fetchCounts()
    print("Before: {}".format(status_before))
    basefileName = 'mpd.slice.'
    fileName = None
    if input("Would you like to run a test on a single data set? (y/n) ") == 'y':
        testNum = int(input("Enter the test number 0-9: "))
        if(testNum < 0 or testNum > 9):
            print("Invalid test number Exiting...")
            exit()
        elif(testNum == 0):
            fileName = basefileName + '0-999.json'
        else:
            fileName = str(basefileName + str(testNum) +
                           '000-' + str(testNum) + '.json')

        if fileName is not None:
            s.loadOneFile(fileName)
    # ask the user if they would like to run tests on entire data set
    elif input("Would you like to run tests on the entire data set? (y/n) ") == 'y':
        s.loadAllData()

    status_after = s.fetchCounts()

    print(status_before)
    print(status_after)

# TODO: add foreign key constraint to the tables after inserting all data
# TODO: Graph the data/time to see how long it takes to load the data
# TODO: Move credentials to a .env file // increase database security
# TODO: Finish the web API
# TODO: Pretty looking web interface?
# TODO: Make import data more efficient


# Create an index for every key (primary, foreign)
# in the playlist content table
