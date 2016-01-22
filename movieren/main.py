#!/usr/bin/env python

import os.path
import click

from config import Config
from movie import find_likely_movie

def build_output_filename(config, movie):
    """Select the output filename.
    """
    return config['rename_format'].format(**movie)


def movieren(config, in_file):
    """Main movieren function. Process movie files.
    """
    directory, filename = os.path.split(in_file)
    movie = find_likely_movie(filename)
    output_filename = build_output_filename(config, movie)
    print(output_filename)


@click.command()
@click.option('--format', help='Ouput format')
@click.argument('in_file', type=click.Path(exists=True))
def main(format, in_file):
    try:
        movieren(Config, click.format_filename(in_file))
    except ValueError as e:
        print(e)


if __name__ == '__main__':
    main()
