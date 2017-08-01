import os
from collections import Counter
from datetime import datetime
from itertools import islice

from bson import objectid, errors
from pymongo import ASCENDING
from pymongo import MongoClient

from wilson import front_page_rank


def in_docker():
    """ Returns: True if running in a docker container, else False """
    if not os.path.isfile('/proc/1/cgroup'):
        return False
    with open('/proc/1/cgroup', 'rt') as ifh:
        return 'docker' in ifh.read()


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Dal(object):
    __metaclass__ = Singleton

    __slots__ = ['_client', '_db']

    def __init__(self):
        if in_docker():
            self._client = MongoClient("db")
        else:
            self._client = MongoClient()

        self._db = self._client.postdb

    def create(self, post_text):
        item_doc = {
            "date": datetime.utcnow().strftime("%Y-%m-%d_%H:%M:%S"),
            "post": post_text,
            "up_vote": 0,
            "down_vote": 0
        }
        return self._db.postdb.insert_one(item_doc).inserted_id

    def update(self, post_id, update_text):
        if self.get(post_id) is None:
            return False
        self._db.postdb.update_one({'_id': post_id}, {'$set': {'post': update_text}}, upsert=False)
        return True

    def get(self, post_id):
        try:
            return self._db.postdb.find_one({"_id": objectid.ObjectId(post_id)})
        except errors.InvalidId:
            return None

    def up_vote(self, post_id):
        if self.get(post_id) is None:
            return False
        self._db.postdb.update_one({'_id': post_id}, {'$inc': {'up_vote': 1}}, upsert=False)
        return True

    def down_vote(self, post_id):
        if self.get(post_id) is None:
            return False
        self._db.postdb.update_one({'_id': post_id}, {'$inc': {'down_vote': 1}}, upsert=False)
        return True

    def top_list(self, num_of_posts=50):
        now = datetime.utcnow()
        # limit number of records? .limit(num)
        collection = self._db.postdb.find(sort=[('date', ASCENDING)])
        tops = Counter()
        for item in collection:
            past = datetime.strptime(item['date'], "%Y-%m-%d_%H:%M:%S")
            td = now - past
            rank = front_page_rank(item['up_vote'], item['down_vote'], (td.seconds // 60) % 60)
            tops[str(item['_id'])] = rank
        if len(tops) is 0:
            return

        """Return first n items of the iterable as a list"""
        res = list(islice(sorted(tops, key=tops.__getitem__, reverse=True), num_of_posts))
        return res
