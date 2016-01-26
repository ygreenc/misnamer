#!/usr/bin/env python

import os.path
import shutil
import json
import click

from config import Config
from movie import find_likely_movie


def movieren(config, in_file):
    """Main movieren function. Process movie files.
    """
    directory, filename = os.path.split(in_file)
    _, extension = os.path.splitext(filename)

    movie = find_likely_movie(filename)

    # Build destination path
    if config.get('move_file_enable', False):
        directory = os.path.expanduser(config['move_file_destination'])

    # Perform replacements on filename
    new_filename = config['rename_format'] + extension
    destination = os.path.join(directory, new_filename).format(**movie)

    if os.path.exists(destination) and config['overwrite_destination'] is False:
        raise RuntimeError('File %s already exists' % destination)

    click.secho('Moving %s -> %s' % (in_file, destination), fg='green')
    shutil.move(in_file, destination)


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
    except RuntimeError as e:
        click.secho(e, fg='red')
    except ValueError as e:
        click.secho(e, fg='red')


if __name__ == '__main__':
    main()
