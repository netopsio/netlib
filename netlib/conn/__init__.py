"""netlib.conn init."""


def send_commands(connection_command: object, commands_list: list) -> str:
    """Enter a list of commands."""
    output = str()
    if list(commands_list):
        for command in commands_list:
            output += connection_command(command)
    else:
        output += connection_command(commands_list)
    return output
