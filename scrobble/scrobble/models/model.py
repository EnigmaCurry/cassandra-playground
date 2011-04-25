import pycassa
import copy
import json
import datetime
import operator
import bcrypt

import db
from track_lists import load_track_list

db_config = dict(
    host = "localhost:9160",
    keyspace = "scrobble",
    column_families = dict(
        User = dict(),
        UserPassword = dict(),
        UserFollowing = dict(),
        UserFollower = dict(),
        UserTrack = dict(
            super=True,
            comparator_type=pycassa.system_manager.TIME_UUID_TYPE
            ),
        UserTrackTag = dict(
            super=True
            ),
        TrackTag = dict(),
        TagTrack = dict(),
        ),
    indexes = dict(
        TrackTag = dict(
            column = "num_times"
            )
        )
    )

class ModelBase(object):
    def __repr__(self):
        key = getattr(self, "key", None)
        return "<{0} key={1}>".format(
            self.__class__.__name__,
            key)
    @classmethod
    def get(cls, key):
        return cls.objects.get(key)
    def persist(self):
        self.__class__.objects.insert(self)

class User(ModelBase):
    fname = pycassa.String()
    lname = pycassa.String()
    email = pycassa.String()
    created = pycassa.DateTimeString()
    #comma seperated group list:
    groups = pycassa.String()
    @classmethod
    def get_all_usernames(cls, limit=100):
        """Get all the usernames (up to limit) without loading the
        entire user object"""
        for user in User.objects.get_range(row_count=limit,columns=[]):
            yield user.key
    def record_track(self, track, date=None):
        if date is None:
            date = datetime.datetime.now()
        track = copy.copy(track)
        track["listen_date"] = date.strftime("%s")
        db.UserTrack.insert(self.key, {date : track})
    def get_tracks(self, limit=100):
        "Get played tracks"
        try:
            return db.UserTrack.get(
                self.key, column_count=limit, column_reversed=True).values()
        except pycassa.NotFoundException:
            return []
    def get_following(self, limit=100):
        "Get the Users that the User is following"
        try:
            return db.UserFollowing.get(
                self.key, column_count=limit).keys()
        except pycassa.NotFoundException:
            return []
    def get_followers(self, limit=100):
        "Get the Users that the User is followed by"
        try:
            return db.UserFollower.get(
                self.key, column_count=limit).keys()
        except pycassa.NotFoundException:
            return []
    def is_following(self, userid):
        try:
            db.UserFollowing.get(self.key, columns=[userid])
        except pycassa.NotFoundException:
            return False
        return True
    def add_following(self, userid):
        user = User.get(userid) #raise NotFoundException if that user doesn't exist.
        db.UserFollowing.insert(self.key, {userid:""})
        db.UserFollower.insert(userid, {self.key:""})
    def remove_following(self, userid):
        db.UserFollowing.remove(self.key, (userid,))
        db.UserFollower.remove(userid, (self.key,))
    def get_groups(self):
        if self.groups is None:
            return []
        return self.groups.split(",")
    def set_groups(self, groups):
        self.groups = ",".join(groups)

class UserFollowers(ModelBase):
    pass

class UserPassword(ModelBase):
    "Seperate password store for accounts"
    password_hash = pycassa.String()
    @classmethod
    def save_password(cls, userid, password):
        User.get(userid) #raise NotFoundException if no user
        user_pw = UserPassword()
        user_pw.key = userid
        user_pw.password_hash = bcrypt.hashpw(password,bcrypt.gensalt())
        user_pw.persist()

class TrackTag(object):
    @classmethod
    def generate_track_id(cls, track):
        "A hash function for generating a track id"
        return track["artist"].replace("|","&#124;") + "|" + \
            track["title"].replace("|","&#124;")
    @classmethod
    def add_track_tag(cls, user, track, tag):
        "Add a tag to a track"
        track_id = cls.generate_track_id(track)
        #Record the user tag:
        db.UserTrackTag.insert(user, {track_id:{tag:""}})
        #Update the global track tags
        times_tagged = "1"
        new_times = "1"
        try:
            times_tagged = str(int(db.TrackTag.get(track_id,columns=[tag])[tag]) + 1)
        except pycassa.NotFoundException:
            pass
        db.TrackTag.insert(track_id, {tag:new_times})
        db.TagTrack.insert(tag, {track_id:new_times})
    @classmethod
    def get_track_tags(cls, track):
        "Get all the tags for a track"
        track_id = cls.generate_track_id(track)
        try:
            return db.TrackTag.get(track_id)
        except pycassa.NotFoundException:
            return []
    @classmethod
    def get_tag_tracks(cls, tag):
        "Get all the tracks for a tag"
        try:
            return db.TagTrack.get(tag)
        except pycassa.NotFoundException:
            return []
        
def setup():
    """Call once to set everything up:"""
    db.connect(db_config)

    #Map all the model objects to the column families:
    for cf in db_config["column_families"]:
        try:
            model_obj = globals()[cf]
            if model_obj.__base__ != ModelBase:
                continue
            cass_cf = getattr(db,cf)
        except KeyError:
            continue
        model_obj.objects = pycassa.ColumnFamilyMap(model_obj, cass_cf)

def test_data():
    db.recreate_default_namespace()
    setup()
    ryan = User()
    ryan.key = "ryan"
    ryan.fname = "Ryan"
    ryan.lname = "McGuire"
    ryan.persist()
    UserPassword.save_password("ryan","asdf")
    
    for track in load_track_list("helios.txt"):
        ryan.record_track(track)
    
    print ryan.get_tracks()

        
if __name__ == "__main__":
    from IPython.Shell import IPShellEmbed
    ipshell = IPShellEmbed()

    setup()
    
    ipshell()
