import click
from mutagen import MutagenError
from coverdl import __version__
from coverdl.providers import providers
from coverdl.providers.provider import Cover, Provider
from coverdl.providers.source import Source
from coverdl.metadata import get_metadata_from_file, get_metadata_from_directory
from coverdl.exceptions import TriesExceeded, ProviderRequestFailed
from coverdl.utils import has_cover, download_cover, get_recursive_paths
from coverdl.options import Options
from requests.exceptions import HTTPError
import os
import sys

def error(message):
    click.echo(f"{click.style('Error:', fg='red')} {message}")

def warn(message, silence=False):
    if silence:
        return
    click.echo(f"{click.style('Warn:', fg='yellow')} {message}")

def handle_download(options: Options, path_locations: list[str], selected_providers: list[Provider]):
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
                error(f"Failed to fetch sufficient metadata from album: {click.style(path, bold=True)}")
                failed += 1
                continue
        elif os.path.isfile(path):
            click.echo(f"Fetching metadata from track {click.style(path, bold=True)}")
            try:
                metadata = get_metadata_from_file(path)
            except MutagenError:
                error(f"Failed to open file: {click.style(path, bold=True)}, possibly invalid or corrupt")
                failed += 1
                continue

        if has_cover(path):
            warn(f"{click.style(path, bold=True)} already has a cover. Skipping.", not options.no_silence_warnings)
            continue

        if not metadata:
            error(f"Could not fetch metadata from path: {click.style(path, bold=True)}")
            failed += 1
            continue

        results = []

        for provider in selected_providers:
            try:
                results = results + provider.get_covers(metadata.artist, metadata.album)

                if len(results) != 0:
                    # There is no need to fetch from the next provider if we already have results.
                    break
            except ProviderRequestFailed as e:
                warn(f"Failed to fetch cover art data from provider: {e.args[0].value}. Got error: {e.args[1]}", not options.no_silence_warnings)

        if len(results) == 0:
            error(f"No suitable cover art could be found for {click.style(path, bold=True)}")
            failed += 1
            continue

        cover: Cover = results[0]

        try:
            dir_path = path if os.path.isdir(path) else os.path.dirname(path)
            download_cover(cover.cover_url, dir_path, options.cover_name)
            click.echo(f"Cover art for {click.style(path, bold=True)} successfully downloaded")
            completed += 1
        except HTTPError as e:
            error(f"Failed to download cover art for {click.style(path, bold=True)}, got error: {e.response.status_code}")

    click.echo()
    click.echo(f"{click.style('Completed:', bold=True)} {completed}, {click.style('Failed:', bold=True)} {failed}")

def handle_upgrade(options: Options, path_locations: list[str], selected_providers: list[Provider]):
    pass

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
@click.option('-u', '--upgrade',
              is_flag=True,
              help='Upgrades existing cover art to better quality equivalents.')
@click.option('--max-size',
              type=float, default=10,
              help='Already existing cover art that exceeds the max size will not be considered for upgrade.')
@click.option('--strict',
              help='Enables strict mode (for upgrades). Ensures that only near-perfect comparisons will be upgraded.')
@click.option('--no-silence-warnings',
              default=False,
              is_flag=True)
@click.argument('path', type=click.Path(exists=True))
@click.version_option(__version__)
def coverdl(path: str,
            provider: list[Source],
            cover_name: str,
            recursive: bool,
            upgrade: bool,
            tag: list[str],
            max_size: float,
            strict: bool,
            no_silence_warnings: bool):
    options = Options(
        path=path,
        providers=provider,
        cover_name=cover_name,
        tags=tag,
        recursive=recursive,
        upgrade=upgrade,
        max_size=max_size,
        strict=strict,
        no_silence_warnings=no_silence_warnings
    )
    
    # Get and sort the providers based on user preference
    selected_providers = list(filter(lambda p: p.source in provider, providers))
    selected_providers.sort(key=lambda p: options.providers.index(p.source))

    if options.recursive and options.tags:
        error("--recursive and --tag cannot be used together.")
        sys.exit(1)

    path_locations = get_recursive_paths(options.path) if options.recursive else [options.path]

    if options.upgrade:
        handle_upgrade(options, path_locations, selected_providers)
    else:
        handle_download(options, path_locations, selected_providers)