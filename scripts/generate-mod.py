#!/usr/bin/env python3
"""Generate the game content from the source name tree."""

import argparse
import json
import shutil
import sys
import unicodedata
from pathlib import Path

# --- Constants ---

REPOSITORY_DIRECTORY = Path(__file__).resolve().parent.parent

SOURCE_NAMES_DIRECTORY = REPOSITORY_DIRECTORY / 'src' / 'names'
SOURCE_THUMBNAIL_PATH = REPOSITORY_DIRECTORY / 'src' / 'thumbnail.png'

OUTPUT_DIRECTORY = REPOSITORY_DIRECTORY / 'out'

MOD_IDENTIFIER = 'ui-star-names'
MOD_NAME = 'Universum Infinitum - Star Names'

STELLARIS_GAME = 'stellaris'
STELLARIS_GAME_VERSION = 'v4.5.*'
STELLARIS_MOD_TAGS = ('Galaxy Generation',)
STELLARIS_NAMES_FILE_NAME = 'universum_infinitum.txt'

GALCIV2_GAME = 'galciv2'
GALCIV2_FILE_ENCODING = 'cp1252'
GALCIV2_NEWLINE = '\r\n'
GALCIV2_STARS_FILE_RELATIVE_PATH = Path('Data') / 'English' / 'STARS.txt'
GALCIV2_TWILIGHT_STARS_FILE_RELATIVE_PATH = Path('Twilight') / GALCIV2_STARS_FILE_RELATIVE_PATH

GALCIV3_GAME = 'galciv3'
GALCIV3_FILE_ENCODING = 'utf-8'
GALCIV3_NEWLINE = '\r\n'
GALCIV3_STARS_FILE_RELATIVE_PATH = Path('Text') / 'StarNamesText.xml'
GALCIV3_STAR_NAME_LABEL_PREFIX = 'RANDOM_STAR_NAME_'
GALCIV3_REQUIRED_DIRECTORIES = ('ParticleScriptDefs', 'Text', 'Core', 'Game')

# The game hashes each label with the 32-bit FNV-1a algorithm over UTF-16 and
# rejects the load when two labels collide. The label RANDOM_STAR_NAME_35997
# collides with the vanilla label Haven_TerranIndustrialSpecialization3_Name,
# so index 35997 is reserved and skipped when assigning label indices.
GALCIV3_RESERVED_STAR_NAME_INDICES = frozenset((35997,))

SUPPORTED_GAMES = (GALCIV2_GAME, GALCIV3_GAME, STELLARIS_GAME)

STARS_CATEGORY_DIRECTORY = 'stars'

STELLARIS_OUTPUT_DIRECTORY = OUTPUT_DIRECTORY / STELLARIS_GAME
STELLARIS_MOD_DIRECTORY = STELLARIS_OUTPUT_DIRECTORY / MOD_IDENTIFIER

GALCIV2_OUTPUT_DIRECTORY = OUTPUT_DIRECTORY / GALCIV2_GAME

GALCIV3_OUTPUT_DIRECTORY = OUTPUT_DIRECTORY / GALCIV3_GAME
GALCIV3_MOD_DIRECTORY = GALCIV3_OUTPUT_DIRECTORY / MOD_IDENTIFIER

CATEGORY_BLOCKS = (
    (STARS_CATEGORY_DIRECTORY, 'star_names'),
    ('nebulae', 'nebula_names'),
    ('black_holes', 'black_hole_names'),
    ('asteroid_prefixes', 'asteroid_prefix'),
    ('asteroid_postfixes', 'asteroid_postfix'),
)
QUOTED_BLOCK_NAMES = frozenset(('star_names', 'nebula_names', 'black_hole_names'))

# --- Source reading ---

def read_category_entries(category_directory):
    entries = []

    for json_path in sorted(SOURCE_NAMES_DIRECTORY.glob(f'{category_directory}/*.json')):
        document = json.loads(json_path.read_text(encoding='utf-8'))

        entries.extend(document['names'])

    return entries


def sort_and_deduplicate(entries):
    unique_entries = set(entries)

    return sorted(unique_entries, key=lambda entry: (entry.casefold(), entry))


def collect_blocks():
    blocks = []

    for category_directory, block_name in CATEGORY_BLOCKS:
        entries = read_category_entries(category_directory)

        blocks.append((block_name, sort_and_deduplicate(entries)))

    return blocks


def collect_star_names():
    return sort_and_deduplicate(read_category_entries(STARS_CATEGORY_DIRECTORY))


def sanitise_galciv2_entry(entry):
    sanitised_entry = None

    try:
        entry.encode(GALCIV2_FILE_ENCODING)

        sanitised_entry = entry
    except UnicodeEncodeError:
        normalised_entry = unicodedata.normalize('NFKD', entry)

        sanitised_entry = normalised_entry.encode('ascii', 'ignore').decode('ascii')

    return sanitised_entry


def collect_galciv2_entries():
    sanitised_entries = [sanitise_galciv2_entry(entry) for entry in collect_star_names()]

    return sort_and_deduplicate(sanitised_entries)

# --- Rendering ---

def render_block(block_name, entries):
    lines = [f'{block_name} = {{']

    for entry in entries:
        if block_name in QUOTED_BLOCK_NAMES:
            lines.append(f'    "{entry}"')
        else:
            lines.append(f'    {entry}')

    lines.append('}')

    return '\n'.join(lines)


def render_stellaris_name_file(blocks):
    rendered_blocks = [render_block(block_name, entries) for block_name, entries in blocks]

    return '\n\n'.join(rendered_blocks) + '\n'


def render_stellaris_descriptor(version):
    tags = '\n'.join(f'    "{tag}"' for tag in STELLARIS_MOD_TAGS)

    return (
        f'version="{version}"\n'
        f'name="{MOD_NAME}"\n'
        f'path="mod/{MOD_IDENTIFIER}"\n'
        f'tags={{\n{tags}\n}}\n'
        f'supported_version="{STELLARIS_GAME_VERSION}"\n'
    )


def render_galciv2_stars_file(entries):
    return ''.join(f'{entry}{GALCIV2_NEWLINE}' for entry in entries)


def escape_xml_text(text):
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def galciv3_star_name_index(ordinal):
    index = ordinal

    for reserved_index in sorted(GALCIV3_RESERVED_STAR_NAME_INDICES):
        if reserved_index <= index:
            index += 1

    return index


def render_galciv3_stars_file(entries):
    lines = [
        '<?xml version="1.0" encoding="utf-8"?>',
        '<StringTableList',
        'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"',
        'xsi:noNamespaceSchemaLocation="../../Schema/Lib/StringTable.xsd">',
    ]

    for ordinal, entry in enumerate(entries):
        index = galciv3_star_name_index(ordinal)

        lines.append('  <StringTable>')
        lines.append(f'    <Label>{GALCIV3_STAR_NAME_LABEL_PREFIX}{index}</Label>')
        lines.append(f'    <String>{escape_xml_text(entry)}</String>')
        lines.append('  </StringTable>')

    lines.append('</StringTableList>')

    return GALCIV3_NEWLINE.join(lines) + GALCIV3_NEWLINE

# --- Writing ---

def write_text_file(file_path, text):
    with open(file_path, 'w', encoding='utf-8', newline='\n') as text_file:
        text_file.write(text)


def write_galciv2_text_file(file_path, text):
    file_path.write_bytes(text.encode(GALCIV2_FILE_ENCODING))


def write_galciv3_text_file(file_path, text):
    file_path.write_bytes(text.encode(GALCIV3_FILE_ENCODING))

# --- Generation ---

def generate_stellaris_mod(version):
    names_directory = STELLARIS_MOD_DIRECTORY / 'common' / 'random_names' / 'base'
    names_file_path = names_directory / STELLARIS_NAMES_FILE_NAME
    descriptor_path = STELLARIS_MOD_DIRECTORY / 'descriptor.mod'
    mod_descriptor_path = STELLARIS_OUTPUT_DIRECTORY / f'{MOD_IDENTIFIER}.mod'
    thumbnail_path = STELLARIS_MOD_DIRECTORY / 'thumbnail.png'

    blocks = collect_blocks()

    names_directory.mkdir(parents=True, exist_ok=True)

    for existing_path in names_directory.glob('*.txt'):
        existing_path.unlink()

    write_text_file(names_file_path, render_stellaris_name_file(blocks))

    shutil.copyfile(SOURCE_THUMBNAIL_PATH, thumbnail_path)

    descriptor = render_stellaris_descriptor(version)

    write_text_file(descriptor_path, descriptor)
    write_text_file(mod_descriptor_path, descriptor)

    name_count = sum(len(entries) for _, entries in blocks)

    return names_file_path, name_count


def generate_galciv2_data():
    stars_file_path = GALCIV2_OUTPUT_DIRECTORY / GALCIV2_STARS_FILE_RELATIVE_PATH
    twilight_stars_file_path = GALCIV2_OUTPUT_DIRECTORY / GALCIV2_TWILIGHT_STARS_FILE_RELATIVE_PATH

    entries = collect_galciv2_entries()

    stars_file_path.parent.mkdir(parents=True, exist_ok=True)
    twilight_stars_file_path.parent.mkdir(parents=True, exist_ok=True)

    write_galciv2_text_file(stars_file_path, render_galciv2_stars_file(entries))

    shutil.copyfile(stars_file_path, twilight_stars_file_path)

    return stars_file_path, len(entries)


def generate_galciv3_data():
    stars_file_path = GALCIV3_MOD_DIRECTORY / GALCIV3_STARS_FILE_RELATIVE_PATH

    entries = collect_star_names()

    for required_directory in GALCIV3_REQUIRED_DIRECTORIES:
        (GALCIV3_MOD_DIRECTORY / required_directory).mkdir(parents=True, exist_ok=True)

    write_galciv3_text_file(stars_file_path, render_galciv3_stars_file(entries))

    return stars_file_path, len(entries)

# --- Entry point ---

def normalise_game(game):
    return game.strip().casefold()


def parse_arguments():
    description = 'Generate the game content from the source name tree.'
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument(
        '--version',
        help='version of the generated content',
        required=True,
    )
    parser.add_argument(
        '--game',
        choices=SUPPORTED_GAMES,
        help='game to build the content for',
        required=True,
        type=normalise_game,
    )

    return parser.parse_args()


def main():
    arguments = parse_arguments()

    try:
        if arguments.game == STELLARIS_GAME:
            generated_path, name_count = generate_stellaris_mod(arguments.version)
        elif arguments.game == GALCIV2_GAME:
            generated_path, name_count = generate_galciv2_data()
        elif arguments.game == GALCIV3_GAME:
            generated_path, name_count = generate_galciv3_data()
        else:
            raise ValueError(f'Unsupported game: {arguments.game}')
    except (OSError, KeyError, ValueError) as exception:
        print(f'Failed to generate the content: {exception}')

        sys.exit(1)

    relative_path = generated_path.relative_to(REPOSITORY_DIRECTORY)

    print(f'Generated {relative_path} with {name_count} names')


if __name__ == '__main__':
    main()
