import os.path
import re

from .config import Settings

import requests

API_URL = 'http://www.omdbapi.com/?'
UNLIKELY_CHARS = '._()'

IMDB_RE = re.compile(r'(tt[0-9]{7})')
YEAR_RE = re.compile(r'(.*)((19|20)[0-9]{2})')


def _extract_imdbId(name):
    """ Fetch the movie information from extracted imdbId."""
    match = IMDB_RE.search(name)

    if match is None:
        raise ValueError('Could not find an imdbId in filename')

    response = requests.get(
        API_URL,
        {'i': match.group(1)},
        timeout=10.0
    ).json()

    if 'Response' not in response or response['Response'] == 'False':
        raise ValueError('Could not identify the movie with %s' % match.group(1))

    return response


def _extract_before_year(name):
    match = YEAR_RE.search(name)

    if match is None:
        raise ValueError('Could not find a Year')

    movieTitle = ''.join([c if c not in UNLIKELY_CHARS else ' ' for c in match.group(1)])

    response = requests.get(
        API_URL,
        {'t': movieTitle, 'type': 'movie'},
        timeout=10.0
    ).json()

    if 'Response' not in response or response['Response'] == 'False':
        raise ValueError('Could not identify the movie with year %s and name %s' % (movieTitle, match.group(2)))

    return response


def find_likely_movie(filename):
    """Find the most likely movie from the filename."""
    name, _ = os.path.splitext(filename)

    # Check if name contains an imdbId (tt + 7 numbers)
    # example: tt1853728 == Django Unchained
    try:
        return _extract_imdbId(name)
    except ValueError:
        pass

    # Check if name contain a year (4 number). If it does, it's likely
    # that the movie name is to the left of it
    try:
        return _extract_before_year(name)
    except ValueError:
        pass

    raise ValueError('Could not identify the movie %s' % name)


def cleanup_filename(filename):
    for dirty_word in Settings['dirty_words']:
        filename = filename.replace(dirty_word, '')
    return filename
