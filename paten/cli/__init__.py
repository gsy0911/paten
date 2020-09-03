import os

import click

from paten.constants import TEMPLATE_APP, GITIGNORE


@click.group(invoke_without_command=True)
@click.pass_context
def cmd(ctx):
    if ctx.invoked_subcommand is None:
        click.echo('This is parent!')


@cmd.command("deploy")
def deploy():
    click.echo('start to deploy')


@cmd.command("build")
def build():
    click.echo('start to build contents')


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
