"""Connect to network devices via Telnet."""
import re
import telnetlib

from netlib.conn import send_commands


class Telnet:
    """Telnet class."""

    def __init__(
        self,
        device_name: str,
        username: str,
        password: str,
        delay: float = 2,
        port: int = 23,
    ):
        """Initialize Telnet class."""
        self.device_name = device_name
        self.username = username
        self.password = password
        self.delay = delay
        self.port = port
        self.access = telnetlib.Telnet(self.device_name, self.port)
        login_prompt = self.access.read_until(b"\(Username: \)|\(login: \)", self.delay)
        if b"login" in login_prompt:
            self.is_nexus = True
            self.access.write(self.username.encode("ascii") + b"\n")
        elif b"Username" in login_prompt:
            self.is_nexus = False
            self.access.write(self.username.encode("ascii") + b"\n")
        self.access.read_until(b"Password:", self.delay)
        self.access.write(self.password.encode("ascii") + b"\n")

    def close(self):
        """Close the telnet connection."""
        return self.access.close()

    def clear_buffer(self) -> None:
        """Clear the buffer."""
        return

    def set_enable(self, enable_password: str):
        """Enter privileged mode."""
        if re.search(b">$", self.command("\n")):  # pylint: disable=no-else-return
            self.access.write(b"enable\n")
            self.access.read_until(b"Password")
            return self.access.write(enable_password.encode("ascii") + b"\n")
        elif re.search(b"#$", self.command("\n")):
            return "Action: None. Already in enable mode."
        return "Error: Unable to determine user privilege status."

    def disable_paging(self, command: str = "term len 0") -> str:
        """Disable paging."""
        self.access.write(command.encode("ascii") + b"\n")
        return self.access.read_until(b"\(#\)|\(>\)", self.delay)

    def command(self, command: str) -> str:
        """Send a single command."""
        self.access.write(command.encode("ascii") + b"\n")
        return self.access.read_until(b"\(#\)|\(>\)", self.delay)

    def commands(self, commands_list: list) -> str:
        """Enter a list of commands."""
        return send_commands(self.command, commands_list)
