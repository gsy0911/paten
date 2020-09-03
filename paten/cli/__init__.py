import os

import click

from paten.constants import TEMPLATE_APP, GITIGNORE
from .factory import CliFactory


@click.group(invoke_without_command=True)
@click.option('--function-app-dir')
@click.pass_context
def cmd(ctx, function_app_dir: str):
    if function_app_dir is None:
        function_app_dir = os.getcwd()
    if ctx.invoked_subcommand is None:
        click.echo('This is parent!')
    ctx.obj['function_app_dir'] = function_app_dir
    ctx.obj['factory'] = CliFactory(function_app_dir=function_app_dir)


@cmd.command("deploy")
@click.pass_context
def deploy(ctx):
    click.echo('start to deploy')


@cmd.command("build")
@click.pass_context
def build(ctx):
    click.echo('start to build contents')
    cli_factory: CliFactory = ctx.obj['factory']
    paten_app = cli_factory.load_paten_app()
    paten_app.export()


@cmd.command("local")
def local():
    click.echo('hosting at local')


def _create_new_project_skeleton(function_app_name: str):
    paten_dir = os.path.join(function_app_name, '.paten')
    os.makedirs(paten_dir)
    with open(os.path.join(function_app_name, 'requirements.txt'), 'w'):
        pass
    with open(os.path.join(function_app_name, 'app.py'), 'w') as f:
        f.write(TEMPLATE_APP % function_app_name)
    with open(os.path.join(function_app_name, '.gitignore'), 'w') as f:
        f.write(GITIGNORE)


@cmd.command("new-project")
@click.argument('function_app_name')
def new_project(function_app_name: str):
    click.echo('create new project')
    _create_new_project_skeleton(function_app_name=function_app_name)


def main():
    # コンテキストから参照するアトリビュートを渡す
    cmd(obj={})


if __name__ == '__main__':
    main()
