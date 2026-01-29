"""Network device connection classes for SSH and Telnet."""

import re
import time
from typing import Any

import paramiko
import telnetlib
from pydantic import SecretStr

from netlib.models import (
    CommandResponse,
    EnableModeResponse,
    SSHConnectionConfig,
    TelnetConnectionConfig,
)


class SSH:
    """SSH connection handler for network devices."""

    def __init__(
        self,
        device_name: str,
        username: str,
        password: str,
        buffer: int | str = 65535,
        delay: int | str | float = 1,
        port: int | str = 22,
    ) -> None:
        """Initialize SSH connection.

        Args:
            device_name: Device hostname or IP address
            username: Username for authentication
            password: Password for authentication
            buffer: Buffer size for receiving data (default: 65535)
            delay: Delay in seconds between operations (default: 1)
            port: SSH port (default: 22)
        """
        # Validate inputs using Pydantic
        config = SSHConnectionConfig(
            device_name=device_name,
            username=username,
            password=password,
            buffer=int(buffer),
            delay=float(delay),
            port=int(port),
        )

        self.device_name = config.device_name
        self.username = config.username
        self._password = config.password  # SecretStr
        self.buffer = config.buffer
        self.delay = config.delay
        self.port = config.port

        self.pre_conn: paramiko.SSHClient | None = None
        self.client_conn: paramiko.Channel | None = None

    def connect(self) -> bytes:
        """Establish SSH connection to the device.

        Returns:
            Initial output from the device after connection

        Raises:
            paramiko.SSHException: If connection fails
        """
        self.pre_conn = paramiko.SSHClient()
        self.pre_conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.pre_conn.connect(
            self.device_name,
            username=self.username,
            password=self._password.get_secret_value(),
            allow_agent=False,
            look_for_keys=False,
            port=self.port,
        )
        self.client_conn = self.pre_conn.invoke_shell()
        time.sleep(self.delay)
        if self.client_conn:
            return self.client_conn.recv(self.buffer)
        return b""

    def close(self) -> None:
        """Close the SSH connection."""
        if self.pre_conn:
            self.pre_conn.close()

    def clear_buffer(self) -> str | None:
        """Clear the receive buffer.

        Returns:
            Buffer contents if available, None otherwise
        """
        if self.client_conn and self.client_conn.recv_ready():
            return self.client_conn.recv(self.buffer).decode("utf-8", "ignore")
        return None

    def set_enable(self, enable_password: str | SecretStr) -> str:
        """Enter privileged/enable mode.

        Args:
            enable_password: Enable password (can be str or SecretStr)

        Returns:
            Response message from the operation
        """
        # Handle both str and SecretStr
        pwd = (
            enable_password.get_secret_value()
            if isinstance(enable_password, SecretStr)
            else enable_password
        )

        current_prompt = self.command("\n")
        if re.search(r">$", current_prompt):
            enable_output = self.command("enable")
            if re.search("Password", enable_output):
                send_pwd = self.command(pwd)
                return send_pwd
        elif re.search(r"#$", current_prompt):
            return "Action: None. Already in enable mode."
        else:
            return "Error: Unable to determine user privilege status."
        return "Error: Unknown state"

    def disable_paging(self, command: str = "term len 0") -> None:
        """Disable paging on the device.

        Args:
            command: Command to disable paging (default: 'term len 0')
        """
        if self.client_conn:
            self.client_conn.sendall(f"{command}\n")
            self.clear_buffer()

    def command(self, command: str) -> str:
        """Execute a command on the device.

        Args:
            command: Command to execute

        Returns:
            Command output
        """
        if not self.client_conn:
            return ""

        self.client_conn.sendall(f"{command}\n")
        not_done = True
        output = ""
        while not_done:
            time.sleep(self.delay)
            if self.client_conn.recv_ready():
                output += self.client_conn.recv(self.buffer).decode("utf-8")
            else:
                not_done = False
        return output

    def commands(self, commands_list: list[str] | str) -> str:
        """Execute multiple commands.

        Args:
            commands_list: List of commands or single command string

        Returns:
            Combined output from all commands
        """
        output = ""
        if isinstance(commands_list, list):
            for cmd in commands_list:
                output += self.command(cmd)
        else:
            output += self.command(commands_list)
        return output


class Telnet:
    """Telnet connection handler for network devices."""

    def __init__(
        self,
        device_name: str,
        username: str,
        password: str,
        delay: int | str | float = 2,
        port: int | str = 23,
    ) -> None:
        """Initialize Telnet connection.

        Args:
            device_name: Device hostname or IP address
            username: Username for authentication
            password: Password for authentication
            delay: Delay in seconds between operations (default: 2)
            port: Telnet port (default: 23)
        """
        # Validate inputs using Pydantic
        config = TelnetConnectionConfig(
            device_name=device_name,
            username=username,
            password=password,
            delay=float(delay),
            port=int(port),
        )

        self.device_name = config.device_name
        self.username = config.username
        self._password = config.password  # SecretStr
        self.delay = config.delay
        self.port = config.port

        self.access: telnetlib.Telnet | None = None
        self.is_nexus: bool = False

    def connect(self) -> telnetlib.Telnet:
        """Establish Telnet connection to the device.

        Returns:
            Telnet connection object

        Raises:
            OSError: If connection fails
        """
        self.access = telnetlib.Telnet(self.device_name, self.port)
        login_prompt = self.access.read_until(
            b"(Username: )|(login: )", self.delay
        )
        if b"login" in login_prompt:
            self.is_nexus = True
            self.access.write(self.username.encode("ascii") + b"\n")
        elif b"Username" in login_prompt:
            self.is_nexus = False
            self.access.write(self.username.encode("ascii") + b"\n")
        self.access.read_until(b"Password:", self.delay)
        self.access.write(self._password.get_secret_value().encode("ascii") + b"\n")
        return self.access

    def close(self) -> None:
        """Close the Telnet connection."""
        if self.access:
            self.access.close()

    def clear_buffer(self) -> None:
        """Clear the receive buffer (no-op for Telnet)."""

    def set_enable(self, enable_password: str | SecretStr) -> str:
        """Enter privileged/enable mode.

        Args:
            enable_password: Enable password (can be str or SecretStr)

        Returns:
            Response message from the operation
        """
        if not self.access:
            return "Error: Not connected"

        # Handle both str and SecretStr
        pwd = (
            enable_password.get_secret_value()
            if isinstance(enable_password, SecretStr)
            else enable_password
        )

        current_prompt = self.command("\n")
        if re.search(b">$", current_prompt):
            self.access.write(b"enable\n")
            self.access.read_until(b"Password")
            self.access.write(pwd.encode("ascii") + b"\n")
            return "Entered enable mode"
        elif re.search(b"#$", current_prompt):
            return "Action: None. Already in enable mode."
        else:
            return "Error: Unable to determine user privilege status."

    def disable_paging(self, command: str = "term len 0") -> bytes:
        """Disable paging on the device.

        Args:
            command: Command to disable paging (default: 'term len 0')

        Returns:
            Command output
        """
        if not self.access:
            return b""
        self.access.write(command.encode("ascii") + b"\n")
        return self.access.read_until(b"(#)|(>)", self.delay)

    def command(self, command: str) -> bytes:
        """Execute a command on the device.

        Args:
            command: Command to execute

        Returns:
            Command output
        """
        if not self.access:
            return b""
        self.access.write(command.encode("ascii") + b"\n")
        return self.access.read_until(b"(#)|(>)", self.delay)

    def commands(self, commands_list: list[str] | str) -> str:
        """Execute multiple commands.

        Args:
            commands_list: List of commands or single command string

        Returns:
            Combined output from all commands
        """
        output = ""
        if isinstance(commands_list, list):
            for cmd in commands_list:
                output += self.command(cmd).decode("utf-8", "ignore")
        else:
            output += self.command(commands_list).decode("utf-8", "ignore")
        return output
