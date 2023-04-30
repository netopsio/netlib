from invoke import task


@task
def fmt(context):
    """Format python files."""
    commands = [
        "isort --profile black .",
        "black .",
    ]
    for command in commands:
        context.run(command)


@task
def pylint(context):
    """Run pylint."""
    context.run("pylint netlib/")


@task
def black(context):
    """Run black."""
    context.run("black --check netlib/")
