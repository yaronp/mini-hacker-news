import json
from datetime import datetime

import redis
from math import sqrt
import operator

def days_hours_minutes(td):
    return (td.seconds//60)%60

datetime.now()


def front_page_rank(score, sock_votes, age, gravity=1.4, timebase=120):
    """
    Hacker News Ranking Algorithm
    http://sangaline.com/post/reverse-engineering-the-hacker-news-ranking-algorithm/

    :param score:
    :param sock_votes: up-1 - down
    :param age: in minutes
    :param gravity:
    :param timebase:
    :return:
    """
    effective_score = score - sock_votes - 1
    return effective_score / ((timebase + age) / 60) ** gravity


def confidence(ups, downs):
    """
    http://www.evanmiller.org/how-not-to-sort-by-average-rating.html
    https://en.wikipedia.org/wiki/Binomial_proportion_confidence_interval

    Score = Lower bound of Wilson score confidence interval for a Bernoulli parameter

    :param ups: up votes
    :param downs: down votes
    :return: rank

    """
    n = ups + downs

    if n == 0:
        return 0

    z = 1.0  # 1.44 = 85%, 1.96 = 95%
    phat = float(ups) / n
    return (phat + z * z / (2 * n) - z * sqrt((phat * (1 - phat) + z * z / (4 * n)) / n)) / (1 + z * z / n)


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


def calc_score(r):
    post = json.loads(conn.get(r))

    date.fromtimestamp(time.time())
    date.fromtimestamp(post['time'])
    post['score'] = front_page_rank(post['up_vote'], post['dn_vote'], 1)
    return r


def top_list():
    rec = conn.scan(0, 'post:*')

    posts_db = [calc_score(x) for x in rec[1]]
    post_db = {}
    for r in rec[1]:
        post_str = conn.get(r)
        post = json.loads(post_str)
        post['score'] = confidence(int(post['up_vote']), int(post['dn_vote']))
        post_db[post['score']] = post
        print confidence(
            int(post['up_vote']),
            int(post['dn_vote']))
    pass

    # sorted_posts = sorted(post_db.items(), key=lambda (k,v): int(v['score']))
    sorted_posts = sorted(post_db.items(), reverse=True)

    print sorted_posts

    for i in sorted_posts:
        print i[1]['score']


# for i in range(1, 10):
#     print create("post %s" % i)



top_list()


def load_some_date():
    for j in xrange(1, 100):
        i = create("post %s" % str(j))
        update(i, 'new post text')
        for x in range(0, j):
            up_vote(i)
        down_vote(i)

# load_some_date()
