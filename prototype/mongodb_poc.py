import random
import time
from collections import Counter
from datetime import datetime
from itertools import islice

from pymongo import ASCENDING
from pymongo import MongoClient


def front_page_rank(score, sock_votes, age, gravity=1.4, timebase=120):
    effective_score = score - sock_votes - 1
    return effective_score / ((timebase + age) / 60) ** gravity


def take(n, iterable):
    """Return first n items of the iterable as a list"""
    return list(islice(iterable, n))


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class MongoDbDal(object):
    __metaclass__ = Singleton

    def __init__(self):
        # self.client = MongoClient(os.environ['DB_PORT_27017_TCP_ADDR'], 27017)
        self.client = MongoClient()
        self.db = self.client.postdb

    def create(self, post_text):
        # reverse: datetime.strptime(date_str, "%Y-%m-%d_%H:%M:%S")
        item_doc = {
            "date": datetime.utcnow().strftime("%Y-%m-%d_%H:%M:%S"),
            "post": post_text,
            "up_vote": 0,
            "down_vote": 0
        }
        return self.db.postdb.insert_one(item_doc).inserted_id

    def update(self, post_id, update_text):
        self.db.postdb.update_one({'_id': post_id}, {'$set': {'post': update_text}}, upsert=False)

    def up_vote(self, post_id):
        self.db.postdb.update_one({'_id': post_id}, {'$inc': {'up_vote': 1}}, upsert=False)

    def down_vote(self, post_id):
        self.db.postdb.update_one({'_id': post_id}, {'$inc': {'down_vote': 1}}, upsert=False)

    def top_list(self, num_of_posts=500):
        now = datetime.utcnow()
        # limit number of records? .limit(num)
        collection = self.db.postdb.find(sort=[('date', ASCENDING)])
        tops = Counter()
        for item in collection:
            past = datetime.strptime(item['date'], "%Y-%m-%d_%H:%M:%S")
            td = now - past
            rank = front_page_rank(item['up_vote'], item['down_vote'], (td.seconds // 60) % 60)
            tops[str(item['_id'])] = rank
        res = take(num_of_posts, sorted(tops, key=tops.__getitem__, reverse=True))
        print res


def create_test_data():
    dal = MongoDbDal()
    for i in range(0, 100):
        upv = random.randint(1, 100)
        r_id = dal.create("Test")
        print r_id
        if upv % 2:
            dal.update(r_id, "Modified test")
        for j in range(0, upv):
            dal.up_vote(r_id)


if __name__ == '__main__':

    # create_test_data()
    print 'starting'
    start = time.time()
    adal = MongoDbDal()
    adal.top_list()
    end = time.time()
    print(end - start) * 1000