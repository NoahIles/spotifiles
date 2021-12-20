import os
import json
from time import perf_counter
from peewee import *
from playhouse.db_url import connect
# import pandas as pd

from connectDB import connectPooledDB
import models as myModels
from my_logger import *
import my_timer

mPL = myModels.Playlists
mT = myModels.Tracks
mPC = myModels.PlaylistContents

class Storage:
    def __init__(self):
        self.db = connectPooledDB()
        # self.db = connect(os.environ['DATABASE_URL'])
        self.timeStamps = []
        self.eLog = initEvent_Logger()
        self.db.close()
        self.sliceInfo = None

    def __del__(self):
        self.db.close()

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
    # @my_timer.timeit
    def insertTracks(self, tracks, pid):
        num_tracks = len(tracks)
        # $ insert Playlist Content data
        pContents = []
        for t in tracks:
            pContents.append(
                {'track_uri': t['track_uri'], 'playlist_id': pid})
        mPC.insert_many(pContents).on_conflict_ignore().execute()
        mT.insert_many(tracks).on_conflict_ignore().execute()
        return

    #$ Takes a data slice from mpd and cleans it up
    def cleanData(self, data):
        cleaned = data['playlists']
        for pl in cleaned:
            pl.pop('collaborative', None)
            pl.pop('edits', None)
            # TODO: check the difference between edits and num_edits
            pl['_name'] = pl.pop('name', None).replace("'", "\\'")
            # $ Clean the Track data
            for t in pl['tracks']:
                t['artist_name'] = t['artist_name'].replace("'", "\\'")
                t['track_name'] = t['track_name'].replace("'", "\\'")
                t['album_name'] = t['album_name'].replace("'", "\\'")
                t.pop('pos', None)
        return cleaned

    # Returns true if the database doesn't have the slice 
    def handleSliceInfo(self, sliceInfo):
        print("Reading in slice {} ".format(sliceInfo['slice']))
        self.sliceInfo = sliceInfo['slice']
        bounds = self.sliceInfo.split('-')
        self.eLog.info("Slice info: {}".format(self.sliceInfo))
        try:
            mPL.get(mPL.pid == bounds[0])
            mPL.get(mPL.pid == bounds[1])
            return False
        except DoesNotExist:
            return True

    def insertLibrary(self, fileName, chunkSize, verbose=False):
        sl = self.load_data_file(fileName)
        # check if the slice is already loaded
        if(not self.handleSliceInfo(sl['info'])):
            self.eLog.info(f"Slice {self.sliceInfo} already exists Skipping...")
            return 

        clean_pl = self.cleanData(sl)
        pl_count = int((fileName.split('.')[2]).split('-')[0])
        with self.db.atomic():
            # TODO optimize chunk size for mysql / engine
            for chunk in chunked(clean_pl, chunkSize):
                print('Inserting Playlists {}-{}'.format(pl_count,
                      pl_count + len(chunk)))
                pl_count += len(chunk)
                # $ insert the tracks for each playlist
                for pl in chunk:
                    if verbose:
                        print("Inserting tracks for playlist {}".format(
                        pl['pl_name']))
                    tb = perf_counter()
                    self.insertTracks(pl.pop('tracks', None), pl['pid'])
                    te = perf_counter()
                    t = te - tb
                    _t = f"{t / 60} minutes" if (t > 60) else f"{t} seconds"  
                    # self.eLog.info(f"Inserted tracks for playlist {pl['pid']}:{pl['_name']} in {_t}")
                Fields = pl.keys()

                # $ Insert chunkSize playlists into the playlist table
                mPL.insert_many(chunk, Fields).on_conflict_ignore().execute()

    # Write the stats to a file store within a log directory write to a new log every time

    @my_timer.timeit
    def loadAllData(self):
        self.remForeignKeys()
        #* for each json file in the data directory
        for f in os.listdir('/app/raw_data'):
            if f.endswith('.json'):
                self.loadOneFile(f)
        self.addForeignKeys()


    @my_timer.timeit
    def loadOneFile(self, fileName, chunkSize=250):
        self.remForeignKeys()
        self.insertLibrary('/app/raw_data/' + fileName, chunkSize)
        self.addForeignKeys()

    def addForeignKeys(self):
        mPC.playlist_id.foreign_key = mPL.pid
        mPC.track_uri.foreign_key = mT.track_uri

    def remForeignKeys(self):
        mPC.playlist_id.foreign_key = None
        mPC.track_uri.foreign_key = None

    def fetchCounts(self):
        with self.db.atomic():
            return {
                "Playlist content": mPC.select().count(),
                "Tracks": mT.select().count(),
                "Playlists": mPL.select().count()
            }
    def resetDB(self):
        self.db.drop_tables([mPL, mT, mPC])
        self.db.create_tables([mPL, mT, mPC])
        self.eLog.info("Database Reset")            

def main():
    try: 
        s = Storage()
    except Exception as e:
        print(e)
        print("Storage Failed to initialize")
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
            fileName = f"{basefileName}{testNum}000-{testNum}999.json"

        if fileName is not None:
            s.loadOneFile(fileName)
    # ask the user if they would like to run tests on entire data set
    elif input("Would you like to run tests on the entire data set? (y/n) ") == 'y':
        s.loadAllData()

    status_after = s.fetchCounts()

    print(status_before)
    print(status_after)

def findBestChunkSize(increment=25, initial=25, max=300, iterations=3):
    s = Storage()
    tL = initTimeAnalysis_logger()
    s.resetDB()
    fName = "mpd.slice.0-999.json"
    chunkSize=initial
    while chunkSize < max:
        sum = 0
        for i in range(0, iterations):
            curTime = s.loadOneFile(fName, chunkSize)
            sum += curTime
            s.resetDB()
        tL.info(f"Chunk Size: {chunkSize} Time: {sum/3}")
        chunkSize+=increment



if __name__ == "__main__":
    # findBestChunkSize()
    main()




# TODO: Finish the web API
# TODO: Pretty looking web interface?
# TODO: Make import data more efficient
# TODO: Remove Extra requirements from the requirements.txt file


# Create an index for every key (primary, foreign)
# in the playlist content table
