#!/usr/bin/env python

import os.path
import json
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
    _, extension = os.path.splitext(filename)

    movie = find_likely_movie(filename)

    # Build destination path
    if config.get('move_file_enable', False):
        directory = os.path.expanduser(config['move_file_destination'])

    destination = os.path.join(directory, config['rename_format'] + extension).format(**movie)

    if os.path.exists(destination) and config['overwrite_destination'] is False:
        raise RuntimeError('File %s already exists' % directory)

    print(destination)


@click.command()
@click.option('--format', help='Ouput format')
@click.option('--config', help='Use configuration file')
@click.argument('in_file', type=click.Path(exists=True))
def main(format, config, in_file):
    try:
        # Configuration parsing
        # Resolution order is:
        # 1- Specified at runtime (cli parameter)
        # 2- ~/.movieren.json
        # 3- Defaults specified in program
        if config is None:
            config = "~/.movieren.json"

        parsed_configuration = Config

        with open(os.path.expanduser(config)) as cnf:
            loaded_configuration = json.load(cnf)
            parsed_configuration.update(loaded_configuration)

        movieren(parsed_configuration, click.format_filename(in_file))
    except ValueError as e:
        print(e)


if __name__ == '__main__':
    main()
