from math import sqrt


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
