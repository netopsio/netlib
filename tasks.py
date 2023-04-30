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
