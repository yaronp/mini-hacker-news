from math import sqrt


def confidence(ups, downs):
    """
    http://www.evanmiller.org/how-not-to-sort-by-average-rating.html
    https://en.wikipedia.org/wiki/Binomial_proportion_confidence_interval

    :param ups:
    :param downs:
    :return:
    Score = Lower bound of Wilson score confidence interval for a Bernoulli parameter
    """
    n = ups + downs

    if n == 0:
        return 0

    z = 1.0  # 1.44 = 85%, 1.96 = 95%
    phat = float(ups) / n
    return (phat + z * z / (2 * n) - z * sqrt((phat * (1 - phat) + z * z / (4 * n)) / n)) / (1 + z * z / n)
