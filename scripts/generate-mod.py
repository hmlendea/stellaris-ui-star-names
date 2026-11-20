#!/usr/bin/env python3
"""Generate the Stellaris mod content from the source name tree."""

import json
import shutil
import sys
from pathlib import Path

# --- Constants ---

REPOSITORY_DIRECTORY = Path(__file__).resolve().parent.parent

SOURCE_NAMES_DIRECTORY = REPOSITORY_DIRECTORY / 'src' / 'names'
SOURCE_THUMBNAIL_PATH = REPOSITORY_DIRECTORY / 'src' / 'thumbnail.png'

MOD_IDENTIFIER = 'ui-star-names'
MOD_NAME = 'Universum Infinitum - Star Names'
GAME_VERSION = 'v4.5.*'
MOD_TAGS = ('Galaxy Generation',)

OUTPUT_DIRECTORY = REPOSITORY_DIRECTORY / 'out' / 'stellaris'
MOD_DIRECTORY = OUTPUT_DIRECTORY / MOD_IDENTIFIER
NAMES_DIRECTORY = MOD_DIRECTORY / 'common' / 'random_names' / 'base'
THUMBNAIL_PATH = MOD_DIRECTORY / 'thumbnail.png'
DESCRIPTOR_PATH = MOD_DIRECTORY / 'descriptor.mod'
MOD_DESCRIPTOR_PATH = OUTPUT_DIRECTORY / f'{MOD_IDENTIFIER}.mod'
NAME_FILE_PATH = NAMES_DIRECTORY / 'universum_infinitum.txt'

CATEGORY_BLOCKS = (
    ('stars', 'star_names'),
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


def render_name_file(blocks):
    rendered_blocks = [render_block(block_name, entries) for block_name, entries in blocks]

    return '\n\n'.join(rendered_blocks) + '\n'


def render_descriptor(version):
    tags = '\n'.join(f'    "{tag}"' for tag in MOD_TAGS)

    return (
        f'version="{version}"\n'
        f'name="{MOD_NAME}"\n'
        f'path="mod/{MOD_IDENTIFIER}"\n'
        f'tags={{\n{tags}\n}}\n'
        f'supported_version="{GAME_VERSION}"\n'
    )

# --- Writing ---

def write_text_file(file_path, text):
    with open(file_path, 'w', encoding='utf-8', newline='\n') as text_file:
        text_file.write(text)

# --- Generation ---

def generate_names_file(blocks):
    NAMES_DIRECTORY.mkdir(parents=True, exist_ok=True)

    for existing_path in NAMES_DIRECTORY.glob('*.txt'):
        existing_path.unlink()

    write_text_file(NAME_FILE_PATH, render_name_file(blocks))


def generate_metadata(version):
    shutil.copyfile(SOURCE_THUMBNAIL_PATH, THUMBNAIL_PATH)

    descriptor = render_descriptor(version)

    write_text_file(DESCRIPTOR_PATH, descriptor)
    write_text_file(MOD_DESCRIPTOR_PATH, descriptor)

# --- Entry point ---

def main():
    if len(sys.argv) != 2:
        print(f'Usage: {Path(__file__).name} <version>')

        sys.exit(1)

    version = sys.argv[1]

    try:
        blocks = collect_blocks()

        MOD_DIRECTORY.mkdir(parents=True, exist_ok=True)

        generate_names_file(blocks)
        generate_metadata(version)
    except (OSError, KeyError, ValueError) as exception:
        print(f'Failed to generate the mod: {exception}')

        sys.exit(1)

    name_count = sum(len(entries) for _, entries in blocks)

    print(f'Generated {NAME_FILE_PATH.relative_to(REPOSITORY_DIRECTORY)} with {name_count} names')


if __name__ == '__main__':
    main()
