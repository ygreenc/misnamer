import os.path
import re

import requests

API_URL = 'http://www.omdbapi.com/?'

IMDB_RE = re.compile(r'(tt[0-9]{7})')
YEAR_RE = re.compile(r'(.*)[0-9]{4}')


def _extract_imdbId(name):
    """ Fetch the movie information from extracted imdbId."""
    match = IMDB_RE.search(name)

    if match is None:
        raise ValueError('Could not find an imdbId in filename')

    response = requests.get(
        API_URL,
        {'i': match.group(1)},
        timeout=3.0
    ).json()

    if 'Response' not in response or response['Response'] == 'False':
        raise ValueError('Could not identify the movie with %s' % match.group(1))

    return response


def _extract_before_year(name):
    match = YEAR_RE.search(name)

    if match is None:
        raise ValueError('Could not find a Year')


def find_likely_movie(filename):
    """Find the most likely movie from the filename."""
    name, extension = os.path.splitext(filename)

    #TODO Check if name contains tt + 7 numbers
    #example: tt1853728 == Django Unchained
    try:
        return  _extract_imdbId(name)
    except ValueError:
        pass

    #TODO Check if name contain a year (4 number). If it does, it's likely
    # that the movie name is to the left of it
    try:
        return _extract_before_year(name)
    except ValueError:
        pass

    raise ValueError('Could not identify the movie')
