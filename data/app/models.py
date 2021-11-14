from peewee import *
# Generated with peewee's pwiz module 
# python3 -m pwiz -e mysql -u root -H db -P db1 > models.py 
database = MySQLDatabase('db1', **{'charset': 'utf8', 'sql_mode': 'PIPES_AS_CONCAT', 'use_unicode': True, 'host': 'db', 'user': 'root', 'password': 'example'})

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class Playlists(BaseModel):
    pl_description = CharField(null=True)
    pl_duration = IntegerField(constraints=[SQL("DEFAULT 0")])
    pl_edits = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    pl_followers = IntegerField(constraints=[SQL("DEFAULT 0")])
    pl_id = CharField(null=True)
    pl_modified = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    pl_name = CharField()
    pl_num_albums = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    pl_num_artists = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    pl_num_tracks = IntegerField(constraints=[SQL("DEFAULT 0")])
    pl_owner = CharField(null=True)
    pl_owner_url = CharField(null=True)

    class Meta:
        table_name = 'playlists'
        primary_key = False

class Tracks(BaseModel):
    t_album = CharField()
    t_album_uri = CharField()
    t_artist_uri = CharField()
    t_artists = CharField()
    t_duration = IntegerField()
    t_name = CharField()
    t_uri = CharField(primary_key=True)

    class Meta:
        table_name = 'tracks'

