#!/usr/bin/env python

defaults = {
    # Rename filename format
    'rename_format': '{Title}',

    # Replace file at destination if already exists
    'overwrite_destination': False,

    # Only looks for files with this extension
    'valid_extensions': ['avi', 'mkv', 'mp4'],

    # Replacement charactater for invalid output filename
    'replace_invalid_characters_with': '_',

    # Move file destination
    # Relative path is relative to file
    # Use String formatting
    'move_file_destination': '.',

    # Move file to directory ?
    'move_file_enable': False,

    # Words not to consider when parsing a filename
    'dirty_words': []
}

Config = dict(defaults)
