"""Tests for SSH connection class."""

from unittest.mock import MagicMock, Mock, patch

import pytest

from netlib.conn_type import SSH


class TestSSHInit:
    """Tests for SSH initialization."""

    def test_init_with_defaults(self) -> None:
        """Test SSH initialization with default values."""
        ssh = SSH("router1", "admin", "secret")
        assert ssh.device_name == "router1"
        assert ssh.username == "admin"
        assert ssh._password.get_secret_value() == "secret"
        assert ssh.port == 22
        assert ssh.buffer == 65535
        assert ssh.delay == 1.0

    def test_init_with_custom_values(self) -> None:
        """Test SSH initialization with custom values."""
        ssh = SSH(
            "router1",
            "admin",
            "secret",
            buffer=8192,
            delay=2,
            port=2222,
        )
        assert ssh.port == 2222
        assert ssh.buffer == 8192
        assert ssh.delay == 2.0

    def test_init_with_string_values(self) -> None:
        """Test SSH initialization with string numeric values."""
        ssh = SSH("router1", "admin", "secret", buffer="8192", delay="2", port="2222")
        assert ssh.port == 2222
        assert ssh.buffer == 8192
        assert ssh.delay == 2.0


class TestSSHConnect:
    """Tests for SSH connect method."""

    @patch("netlib.conn_type.paramiko.SSHClient")
    @patch("netlib.conn_type.time.sleep")
    def test_connect_success(
        self, mock_sleep: Mock, mock_ssh_client: Mock
    ) -> None:
        """Test successful SSH connection."""
        # Setup mocks
        mock_client = MagicMock()
        mock_ssh_client.return_value = mock_client
        mock_channel = MagicMock()
        mock_client.invoke_shell.return_value = mock_channel
        mock_channel.recv.return_value = b"Router> "

        # Create SSH instance and connect
        ssh = SSH("router1", "admin", "secret")
        result = ssh.connect()

        # Assertions
        mock_client.set_missing_host_key_policy.assert_called_once()
        mock_client.connect.assert_called_once_with(
            "router1",
            username="admin",
            password="secret",
            allow_agent=False,
            look_for_keys=False,
            port=22,
        )
        mock_client.invoke_shell.assert_called_once()
        assert result == b"Router> "


class TestSSHCommand:
    """Tests for SSH command execution."""

    def test_command_no_connection(self) -> None:
        """Test command execution without connection."""
        ssh = SSH("router1", "admin", "secret")
        result = ssh.command("show version")
        assert result == ""

    @patch("netlib.conn_type.time.sleep")
    def test_command_with_connection(self, mock_sleep: Mock) -> None:
        """Test command execution with active connection."""
        ssh = SSH("router1", "admin", "secret")

        # Mock the client connection
        mock_channel = MagicMock()
        ssh.client_conn = mock_channel

        # Setup recv_ready to return True once, then False
        mock_channel.recv_ready.side_effect = [True, False]
        mock_channel.recv.return_value = b"Version output"

        result = ssh.command("show version")

        mock_channel.sendall.assert_called_once_with("show version\n")
        assert "Version output" in result


class TestSSHCommands:
    """Tests for SSH multiple commands execution."""

    def test_commands_with_list(self) -> None:
        """Test executing multiple commands from list."""
        ssh = SSH("router1", "admin", "secret")

        with patch.object(ssh, "command", return_value="output\n") as mock_cmd:
            result = ssh.commands(["show version", "show interfaces"])

            assert mock_cmd.call_count == 2
            assert "output" in result

    def test_commands_with_string(self) -> None:
        """Test executing single command as string."""
        ssh = SSH("router1", "admin", "secret")

        with patch.object(ssh, "command", return_value="output\n") as mock_cmd:
            result = ssh.commands("show version")

            mock_cmd.assert_called_once_with("show version")
            assert "output" in result


class TestSSHClearBuffer:
    """Tests for SSH buffer clearing."""

    def test_clear_buffer_no_data(self) -> None:
        """Test clearing buffer when no data available."""
        ssh = SSH("router1", "admin", "secret")

        mock_channel = MagicMock()
        mock_channel.recv_ready.return_value = False
        ssh.client_conn = mock_channel

        result = ssh.clear_buffer()
        assert result is None

    def test_clear_buffer_with_data(self) -> None:
        """Test clearing buffer with data available."""
        ssh = SSH("router1", "admin", "secret")

        mock_channel = MagicMock()
        mock_channel.recv_ready.return_value = True
        mock_channel.recv.return_value = b"Buffer data"
        ssh.client_conn = mock_channel

        result = ssh.clear_buffer()
        assert result == "Buffer data"


class TestSSHDisablePaging:
    """Tests for disabling paging."""

    def test_disable_paging(self) -> None:
        """Test disable paging command."""
        ssh = SSH("router1", "admin", "secret")

        mock_channel = MagicMock()
        ssh.client_conn = mock_channel

        with patch.object(ssh, "clear_buffer"):
            ssh.disable_paging()
            mock_channel.sendall.assert_called_once_with("term len 0\n")

    def test_disable_paging_custom_command(self) -> None:
        """Test disable paging with custom command."""
        ssh = SSH("router1", "admin", "secret")

        mock_channel = MagicMock()
        ssh.client_conn = mock_channel

        with patch.object(ssh, "clear_buffer"):
            ssh.disable_paging("terminal length 0")
            mock_channel.sendall.assert_called_once_with("terminal length 0\n")


class TestSSHClose:
    """Tests for SSH connection closing."""

    def test_close_connection(self) -> None:
        """Test closing SSH connection."""
        ssh = SSH("router1", "admin", "secret")

        mock_client = MagicMock()
        ssh.pre_conn = mock_client

        ssh.close()
        mock_client.close.assert_called_once()

    def test_close_no_connection(self) -> None:
        """Test closing when no connection exists."""
        ssh = SSH("router1", "admin", "secret")
        ssh.close()  # Should not raise any exception
