import MySQLdb
import json
import logging
import os
from haversine import haversine
import datetime


def get_logger(name):
    # create logger
    logger_ = logging.getLogger(name)
    logger_.setLevel(logging.DEBUG)
    # create formatter
    fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(fmt)
    # create console handler and set level to debug and add formatter to ch
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    # add ch to logger
    logger_.addHandler(ch)
    # do the same with a file handler.
    if not os.path.exists('log'):
        os.makedirs('log')
    f_handler = logging.FileHandler(os.path.join('log', f'{name}.log'))
    f_handler.setLevel(logging.DEBUG)
    f_handler.setFormatter(formatter)
    logger_.addHandler(f_handler)
    return logger_


def parse_epoch(time_):
    """
    :param time_: epoch timestamp
    :return: iso 8601 formatted datetime str.
    """
    return datetime.datetime.fromtimestamp(time_, tz=datetime.timezone.utc)


def home():
    """
    :return: lat, lon tuple of home coordinate.
    """
    with open('credentials.json') as file:
        d = json.loads(file.read())
    return d['home_lat'], d['home_lon']


def is_at_home(lat, lon, delta=(0.001, 0.002)):
    """
        Returns a binary state depending on whether lat lon is within a square
        plus minus the home_latitude and longitude.
    """

    home_latitude, home_longitude = home()
    # load geo-history data
    return (lat > home_latitude - delta[0]) & (lat < home_latitude + delta[0]) & (lon > home_longitude - delta[0]) & (
            lon < home_longitude + delta[0])


def distance_to_home(current):
    return haversine(home(), current)
