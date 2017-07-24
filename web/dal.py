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
        if not self.is_post_exist(post_id):
            return False

        self.open_db()
        c = self.connection.cursor()
        ts = '{:%Y-%m-%d %H:%M}'.format(datetime.datetime.now())
        sql = "UPDATE posts set date='{0}', post='{1}' WHERE id = {2}".format(ts, update_text, post_id)

        try:
            result = c.execute(sql)
            if result is not None:
                self.connection.commit()
            print result
            c.close()
            return True
        except sqlite3.OperationalError:
            return False

        return True

    def up_vote(self, post_id):
        if not self.is_post_exist(post_id):
            return False

        self.open_db()
        c = self.connection.cursor()
        ts = '{:%Y-%m-%d %H:%M}'.format(datetime.datetime.now())
        sql = "UPDATE posts SET upvote=upvote+1 WHERE id={0}".format(post_id)

        try:
            result = c.execute(sql)
            if result is not None:
                self.connection.commit()
            print result
            c.close()
            return True
        except sqlite3.OperationalError:
            return False

    def down_vote(self, post_id):
        if not self.is_post_exist(post_id):
            return False

        self.open_db()
        c = self.connection.cursor()
        ts = '{:%Y-%m-%d %H:%M}'.format(datetime.datetime.now())
        sql = "UPDATE posts SET downvote=downvote+1 WHERE id={0}".format(post_id)

        try:
            result = c.execute(sql)
            if result is not None:
                self.connection.commit()
            print result
            c.close()
            return True
        except sqlite3.OperationalError:
            return False

    def top_list(self, num_of_posts=10):
        # select * from posts order by upvote desc, date limit 15
        pass

    def is_post_exist(self, post_id):
        self.open_db()
        c = self.connection.cursor()

        sql = "SELECT id FROM posts WHERE id = {0}".format(post_id)
        c.execute(sql)
        res = bool(c.fetchone() is not None)
        c.close()
        return res

    def get_field_by_id(self, post_id, field_name):
        self.open_db()
        c = self.connection.cursor()

        sql = "SELECT {0} FROM posts WHERE id = {1}".format(field_name, post_id)
        c.execute(sql)
        res = c.fetchone()
        c.close()
        return res

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
