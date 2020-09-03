import click


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


@cmd.command("new-project")
def new_project():
    click.echo('create new project')


def main():
    # コンテキストから参照するアトリビュートを渡す
    cmd(obj={})


if __name__ == '__main__':
    main()
