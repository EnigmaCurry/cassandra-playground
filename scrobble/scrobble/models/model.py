import pycassa
import copy
import json
import datetime

import db
from song_lists import load_song_list

db_config = dict(
    host = "localhost:9160",
    keyspace = "scrobble",
    column_families = dict(
        User = dict(),
        UserPassword = dict(),
        UserSongs = dict(
            super=True,
            comparator_type=pycassa.system_manager.TIME_UUID_TYPE
            )
        )
    )

class ModelBase(object):
    def __repr__(self):
        key = getattr(self, "key", None)
        d = copy.copy(self.__dict__)
        try:
            del d["key"]
        except KeyError:
            pass
        return "<{0} key={1} {2}>".format(
            self.__class__.__name__,
            key,json.dumps(d))
    @classmethod
    def get(cls, key):
        return cls.objects.get(key)
    def persist(self):
        self.__class__.objects.insert(self)
        
class User(ModelBase):
    fname = pycassa.String()
    lname = pycassa.String()
    created = pycassa.DateTimeString()
    @classmethod
    def get_all_usernames(cls, limit=100):
        """Get all the usernames (up to limit) without loading the
        entire user object"""
        for user in User.objects.get_range(row_count=limit,columns=[]):
            yield user.key
    def record_song(self, song, date=None):
        if date is None:
            date = datetime.datetime.now()
        db.UserSongs.insert(self.key, {date : song})
    def get_songs(self, limit=100, start=None, end=None):
        "Get played songs"
        attrs = {}
        songs = db.UserSongs.get(
            self.key, column_count=limit, column_reversed=True)
        return songs.values()

class UserPassword(ModelBase):
    "Seperate password store for accounts"
    password_hash = pycassa.String()
    
def test_data():
    db.recreate_default_namespace()
    ryan = User()
    ryan.key = "ryan"
    ryan.fname = "Ryan"
    ryan.lname = "McGuire"
    ryan.persist()

    for song in load_song_list("helios.txt"):
        ryan.record_song(song)
    
    print ryan.get_songs()
    
def setup():
    """Call once to set everything up:"""
    db.connect(db_config)

    #Map all the model objects to the column families:
    for cf in db_config["column_families"]:
        try:
            model_obj = globals()[cf]
            cass_cf = getattr(db,cf)
        except KeyError:
            continue
        model_obj.objects = pycassa.ColumnFamilyMap(model_obj, cass_cf)

if __name__ == "__main__":
    from IPython.Shell import IPShellEmbed
    ipshell = IPShellEmbed()

    setup()
    
    ipshell()
