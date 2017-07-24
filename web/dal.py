import datetime
import sqlite3


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Dal(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.connection = None

    def create(self, post_text):
        self.open_db()
        c = self.connection.cursor()
        ts = '{:%Y-%m-%d %H:%M}'.format(datetime.datetime.now())
        sql = "INSERT INTO posts (date, post, upvote, downvote) VALUES ('{0}', '{1}',0,0)".format(ts, post_text)

        try:
            result = c.execute(sql)
            if result is not None:
                self.connection.commit()
            print result
            c.close()
            return True
        except sqlite3.OperationalError:
            return False

    def update(self, post_id, update_text):
        pass

    def up_vote(self, post_id):
        pass

    def down_vote(self, post_id):
        pass

    def top_list(self, num_of_posts=10):
        # select * from posts order by upvote desc, date limit 15
        pass

    def open_db(self):
        if self.connection is not None:
            return
        self.connection = sqlite3.connect('posts.db')
        self.create_posts_tbl()

    def create_posts_tbl(self):
        c = self.connection.cursor()
        c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='posts';")
        if c.fetchone() is None:
            c.execute(
                "CREATE TABLE posts (id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT, post TEXT, upvote INTEGER, downvote INTEGER)")
            self.connection.commit()
        c.close()
