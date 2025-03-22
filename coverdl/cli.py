import click
from mutagen import MutagenError
from coverdl.providers import providers
from coverdl.providers.source import Source
from coverdl.metadata import get_metadata_from_file, get_metadata_from_directory
from coverdl.exceptions import TriesExceeded, ProviderRequestFailed
import os
import sys

def error(message):
    click.echo(f"{click.style('Error:', fg='red')} {message}")

@click.command(context_settings={'show_default': True})
@click.option('-p', '--provider',
              type=Source, multiple=True, default=[Source.APPLE_MUSIC, Source.DEEZER],
              help='The provider to download cover art from. Multiple providers can be specified by passing this option more than once (by order of preference).')
@click.option('--cover-name',
              default='cover',
              help='The filename for the cover art image.')
@click.option('-t', '--tag',
              multiple=True,
              help='A tag is an attribute unique to your release. e.g: remastered, expanded. Multiple tags can be specified.')
@click.option('-r', '--recursive',
              is_flag=True,
              help='Enables recursive download. This will traverse the path you give it and download cover art for albums that don\'t have them.')
@click.argument('path', type=click.Path(exists=True))
def coverdl(path, provider, cover_name, recursive, tag):
    # Get and sort the providers based on user preference
    selected_providers = list(filter(lambda p: p.source in provider, providers))
    selected_providers.sort(key=lambda p: provider.index(p.source))

    if recursive and tag:
        error("--recursive and --tag cannot be used together.")
        sys.exit(1)

    path_locations = [path]
    if recursive:
        pass # TODO

    total = 0
    completed = 0
    failed = 0

    for path in path_locations:
        total += 1
        metadata = None

        if os.path.isdir(path):
            click.echo(f"Fetching metadata from album directory {click.style(path, bold=True)}")
            try:
                metadata = get_metadata_from_directory(path)
            except TriesExceeded:
                error(f"Failed to fetch sufficient metadata from directory: {click.style(path, bold=True)}")
                failed += 1
                continue
        elif os.path.isfile(path):
            click.echo(f"Fetching metadata from track {click.style(path, bold=True)}")
            try:
                metadata = get_metadata_from_file(path)
            except MutagenError:
                error(f"Failed to open file: {click.style(path, bold=True)}")
                failed += 1
                continue


        if not metadata:
            error(f"Could not fetch metadata from path: {click.style(path, bold=True)}")
            failed += 1
            continue

        results = []

        for provider in selected_providers:
            try:
                results = results + provider.get_covers(metadata.artist, metadata.album)
            except ProviderRequestFailed as e:
                error(f"Failed to fetch cover art data from provider: {e.args[0].value}. Got error: {e.args[1]}")

        print(results)