#!/usr/bin/env python

import os.path
import shutil
import click

from .movie import find_likely_movie, cleanup_filename
from .config import Settings, update_settings


def misnamer(in_file):
    """Main misnamer function. Process movie files.
    """
    directory, filename = os.path.split(in_file)
    _, extension = os.path.splitext(filename)

    movie = find_likely_movie(cleanup_filename(filename))

    # Build destination path
    if Settings.get('move_file_enable', False):
        directory = os.path.expanduser(Settings['move_file_destination'])

    # Perform replacements on filename
    new_filename = Settings['rename_format'] + extension
    destination = os.path.join(directory, new_filename).format(**movie)

    if os.path.exists(destination) and not Settings['overwrite_destination']:
        raise RuntimeError('File %s already exists' % destination)

    click.secho('Moving %s -> %s' % (in_file, destination), fg='green')
    shutil.move(in_file, destination)


@click.command()
@click.option('--out_format', help='Ouput format')
@click.option('--configuration', help='Configuration file location')
@click.argument('in_file', type=click.Path(exists=True))
def main(out_format, configuration, in_file):
    try:
        update_settings(configuration)

        if out_format is not None:
            Settings['rename_format'] = out_format

        misnamer(click.format_filename(in_file))
    except RuntimeError as e:
        click.secho(str(e), bg='red')
    except ValueError as e:
        click.secho(str(e), bg='red')


if __name__ == '__main__':
    main()
