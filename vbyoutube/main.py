import click
from .upload import upload
from .update import update
from .sync import sync
from .analytics import stats, videos

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
def main():
    pass


main.add_command(upload)
main.add_command(update)
main.add_command(sync)
main.add_command(stats)
main.add_command(videos)
if __name__ == '__main__':
    main()
