import sqlite3
import datetime

conn = sqlite3.connect('posts.db')
c = conn.cursor()

c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='posts';")
print(c.fetchone())

c.execute(
    "CREATE TABLE posts (id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT, post TEXT, upvote INTEGER, downvote INTEGER)")
conn.commit()

c.execute("INSERT INTO posts (date, post, upvote, downvote) VALUES ('%s', 'postsssss',0,0)" % (
    '{:%Y-%m-%d %H:%M}'.format(datetime.datetime.now())
))
c.execute("INSERT INTO posts (post, upvote, downvote) VALUES ('p2',0,0)")

conn.commit()

c.execute("SELECT * FROM posts;")
print(c.fetchall())
