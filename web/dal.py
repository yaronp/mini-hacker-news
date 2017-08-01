import os
from collections import Counter
from datetime import datetime
from itertools import islice

from pymongo import ASCENDING
from pymongo import MongoClient

from wilson import front_page_rank


def take(n, iterable):
    """Return first n items of the iterable as a list"""
    return list(islice(iterable, n))


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
        # self.client = MongoClient(os.environ['DB_PORT_27017_TCP_ADDR'], 27017)
        if in_docker():
            self._client = MongoClient("db")
        else:
            self._client = MongoClient()

        self._db = self._client.postdb

    def create(self, post_text):
        # reverse: datetime.strptime(date_str, "%Y-%m-%d_%H:%M:%S")
        item_doc = {
            "date": datetime.utcnow().strftime("%Y-%m-%d_%H:%M:%S"),
            "post": post_text,
            "up_vote": 0,
            "down_vote": 0
        }
        return self._db.postdb.insert_one(item_doc).inserted_id

    def update(self, post_id, update_text):
        self._db.postdb.update_one({'_id': post_id}, {'$set': {'post': update_text}}, upsert=False)

    def up_vote(self, post_id):
        self._db.postdb.update_one({'_id': post_id}, {'$inc': {'up_vote': 1}}, upsert=False)

    def down_vote(self, post_id):
        self._db.postdb.update_one({'_id': post_id}, {'$inc': {'down_vote': 1}}, upsert=False)

    def get(self, post_id):
        return self._db.postdb.find({"_id" : post_id})

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
        res = take(num_of_posts, sorted(tops, key=tops.__getitem__, reverse=True))
        return res
