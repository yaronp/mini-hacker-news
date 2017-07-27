import json
import time

import redis

conn = redis.StrictRedis(host='localhost')


def create(post_text):
    post_id = str(conn.incr('post:'))
    now = time.time()
    post = 'post:' + post_id
    post_rec = {
        'post': post_text, 'time': now, 'up_vote': 1, 'dn_vote': 0
    }
    conn.set(post, json.dumps(post_rec))
    return post_id


def update(post_id, new_text):
    current_record = conn.get("post:" + str(post_id))
    # record does not exists
    if current_record is None:
        return False
    modified_record = json.loads(current_record)
    modified_record['post'] = new_text
    conn.set("post:" + str(post_id), json.dumps(modified_record))
    return True


def up_vote(post_id):
    current_record = conn.get("post:" + str(post_id))
    # record does not exists
    if current_record is None:
        return False
    modified_record = json.loads(current_record)
    modified_record['up_vote'] = str((int(modified_record['up_vote']) + 1))
    conn.set("post:" + str(post_id), json.dumps(modified_record))
    return True


def down_vote(post_id):
    current_record = conn.get("post:" + str(post_id))
    # record does not exists
    if current_record is None:
        return False
    modified_record = json.loads(current_record)
    modified_record['dn_vote'] = str((int(modified_record['dn_vote']) + 1))
    conn.set("post:" + str(post_id), json.dumps(modified_record))
    return True


def top_list():
    rec = conn.scan(0, 'post:*')

    for r in rec[1]:
        post = conn.get(r)
    pass


# for i in range(1, 10):
#     print create("post %s" % i)


top_list()

'''
    i = create("post %s" % '3')
    update(i, 'new post text')
    up_vote(i)
    up_vote(i)
    up_vote(i)
    up_vote(i)
    down_vote(i)
    down_vote(i)
'''
