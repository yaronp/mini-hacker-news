import sqlite3


def dal_create(post_text):
    print post_text
    pass


def dal_update(post_id, update_text):
    print post_id
    print update_text
    pass


def dal_up_vote(post_id):
    print post_id
    pass


def dal_down_vote(post_id):
    print post_id
    pass


def dal_top_list(num_of_posts=10):
    print num_of_posts
    pass


def dal_open_db():
    conn = sqlite3.connect('posts.db')
    c = conn.cursor()
    # check if table exists
    # SELECT name FROM sqlite_master WHERE type='table' AND name='posts';
    # CREATE TABLE posts (date TEXT, post TEXT, upvote INTEGER, downvote INTEGER)

    pass


def dal_create_posts_tbl():
    pass
