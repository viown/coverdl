import click
from coverdl.providers import providers
from coverdl.providers.source import Source

@click.command(context_settings={'show_default': True})
@click.option('-p', '--provider',
              type=Source, multiple=True, default=[Source.DEEZER],
              help='The provider to download cover art from. Multiple providers can be specified by passing this option more than once (by order of preference).')
@click.option('--cover-name',
              default='cover',
              help='The filename for the cover art image.')
@click.option('-r', '--recursive',
              is_flag=True,
              help='Enables recursive download. This will traverse the path you give it and download cover art for albums that don\'t have them.')
@click.argument('path', type=click.Path(exists=True))
def coverdl(path, provider, cover_name):
    # Get and sort the providers based on user preference
    selected_providers = list(filter(lambda p: p.source in provider, providers))
    selected_providers.sort(key=lambda p: provider.index(p.source))

    print(selected_providers)