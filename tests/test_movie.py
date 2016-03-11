#!/usr/bin/env python

import unittest

from movieren.movie import find_likely_movie, cleanup_filename
from movieren.config import set_option

EXAMPLES = [
    ('Inglourious.Basterds.2009.1080p.BluRay.x264.AC3-ETRG.mp4', 'tt0361748'),
    ('Fury (2014) BDRip 720p HEVC ITA ENG AC3 ITA ENG Sub Pirate.mkv', 'tt2713180'),
    ('django.tt1853728.mkv', 'tt1853728')
]


class TestMovie(unittest.TestCase):
    def test_raw(self):
        for filename, imdbId in EXAMPLES:
            with self.subTest(filename=filename, imdbId=imdbId):
                movie = find_likely_movie(filename)
                self.assertIsNotNone(movie)
                self.assertEqual(imdbId, movie['imdbID'])

    def test_cleanup(self):
        set_option('dirty_words', ['ITA', 'Sub', 'Pirate', 'BluRay', 'AC3', 'ETRG', 'x264'])
        self.assertEqual('Inglourious.Basterds.2009.1080p...-.mp4', cleanup_filename('Inglourious.Basterds.2009.1080p.BluRay.x264.AC3-ETRG.mp4'))


if __name__ == '__main__':
    unittest.main()
