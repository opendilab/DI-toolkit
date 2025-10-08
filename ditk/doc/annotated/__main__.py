from functools import partial

import click
from click.core import Context, Option

from ditk import logging
from ditk.config.meta import __VERSION__
from .generate import generate_annotated_doc, Lang

GLOBAL_CONTEXT_SETTINGS = dict(
    help_option_names=['-h', '--help']
)


def print_version(module, ctx: Context, param: Option, value: bool) -> None:
    """
    Print version information of cli
    :param module: current module using this cli.
    :param ctx: click context
    :param param: current parameter's metadata
    :param value: value of current parameter
    """
    _ = param
    if not value or ctx.resilient_parsing:
        return  # pragma: no cover

    click.echo(f'CLI for {module}, version {__VERSION__}')
    ctx.exit()


@click.group(context_settings={**GLOBAL_CONTEXT_SETTINGS},
             help='Utils for creating annotation documentation.')
@click.option('-v', '--version', is_flag=True,
              callback=partial(print_version, 'ditk.doc.annotated'), expose_value=False, is_eager=True,
              help="Show version information.")
def cli():
    pass


@cli.command('create', context_settings={**GLOBAL_CONTEXT_SETTINGS},
             help='Utils for creating annotation documentation from local code.')
@click.option('-i', '--input_file', 'input_file', type=click.types.Path(dir_okay=False, exists=True),
              required=True, help='Input source code.')
@click.option('-o', '--output_file', 'output_file', type=click.types.Path(dir_okay=False),
              required=True, help='Output annotated documentation code.')
@click.option('-A', '--assets_dir', 'assets_directory', type=click.types.Path(file_okay=False),
              default=None, help='Directory for assets file of this documentation.')
@click.option('-L', '--language', 'language',
              type=click.types.Choice([item.value for item in Lang.__members__.values()]),
              default=Lang.English.value, help='Language for documentation.', show_default=True)
@click.option('-T', '--title', type=str, default='<Untitled Documentation>',
              help='Title of the documentation.', show_default=True)
def main(input_file, output_file, assets_directory, language, title):
    logging.try_init_root(logging.INFO)
    generate_annotated_doc(input_file, output_file, title, assets_directory, language)


if __name__ == '__main__':
    cli()
