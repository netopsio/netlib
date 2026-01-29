"""Tests for Telnet connection class."""

from unittest.mock import MagicMock, Mock, patch

from netlib.conn_type import Telnet


class TestTelnetInit:
    """Tests for Telnet initialization."""

    def test_init_with_defaults(self) -> None:
        """Test Telnet initialization with default values."""
        telnet = Telnet("switch1", "admin", "secret")
        assert telnet.device_name == "switch1"
        assert telnet.username == "admin"
        assert telnet._password.get_secret_value() == "secret"
        assert telnet.port == 23
        assert telnet.delay == 2.0

    def test_init_with_custom_values(self) -> None:
        """Test Telnet initialization with custom values."""
        telnet = Telnet("switch1", "admin", "secret", delay=5, port=2323)
        assert telnet.port == 2323
        assert telnet.delay == 5.0

    def test_init_with_string_values(self) -> None:
        """Test Telnet initialization with string numeric values."""
        telnet = Telnet("switch1", "admin", "secret", delay="3", port="2323")
        assert telnet.port == 2323
        assert telnet.delay == 3.0


class TestTelnetConnect:
    """Tests for Telnet connect method."""

    @patch("netlib.conn_type.telnetlib.Telnet")
    def test_connect_with_username_prompt(self, mock_telnet_class: Mock) -> None:
        """Test Telnet connection with Username prompt."""
        mock_telnet = MagicMock()
        mock_telnet_class.return_value = mock_telnet
        mock_telnet.read_until.side_effect = [
            b"Username: ",
            b"Password:",
        ]

        telnet = Telnet("switch1", "admin", "secret")
        result = telnet.connect()

        mock_telnet_class.assert_called_once_with("switch1", 23)
        assert telnet.is_nexus is False
        assert result == mock_telnet

    @patch("netlib.conn_type.telnetlib.Telnet")
    def test_connect_with_login_prompt(self, mock_telnet_class: Mock) -> None:
        """Test Telnet connection with login prompt (Nexus)."""
        mock_telnet = MagicMock()
        mock_telnet_class.return_value = mock_telnet
        mock_telnet.read_until.side_effect = [
            b"login: ",
            b"Password:",
        ]

        telnet = Telnet("switch1", "admin", "secret")
        result = telnet.connect()

        assert telnet.is_nexus is True
        assert result == mock_telnet


class TestTelnetCommand:
    """Tests for Telnet command execution."""

    def test_command_no_connection(self) -> None:
        """Test command execution without connection."""
        telnet = Telnet("switch1", "admin", "secret")
        result = telnet.command("show version")
        assert result == b""

    def test_command_with_connection(self) -> None:
        """Test command execution with active connection."""
        telnet = Telnet("switch1", "admin", "secret")

        mock_connection = MagicMock()
        mock_connection.read_until.return_value = b"Version output\nSwitch#"
        telnet.access = mock_connection

        result = telnet.command("show version")

        mock_connection.write.assert_called_once_with(b"show version\n")
        assert b"Version output" in result


class TestTelnetCommands:
    """Tests for Telnet multiple commands execution."""

    def test_commands_with_list(self) -> None:
        """Test executing multiple commands from list."""
        telnet = Telnet("switch1", "admin", "secret")

        with patch.object(telnet, "command", return_value=b"output\n") as mock_cmd:
            result = telnet.commands(["show version", "show interfaces"])

            assert mock_cmd.call_count == 2
            assert "output" in result

    def test_commands_with_string(self) -> None:
        """Test executing single command as string."""
        telnet = Telnet("switch1", "admin", "secret")

        with patch.object(telnet, "command", return_value=b"output\n") as mock_cmd:
            result = telnet.commands("show version")

            mock_cmd.assert_called_once_with("show version")
            assert "output" in result


class TestTelnetDisablePaging:
    """Tests for disabling paging."""

    def test_disable_paging_no_connection(self) -> None:
        """Test disable paging without connection."""
        telnet = Telnet("switch1", "admin", "secret")
        result = telnet.disable_paging()
        assert result == b""

    def test_disable_paging(self) -> None:
        """Test disable paging command."""
        telnet = Telnet("switch1", "admin", "secret")

        mock_connection = MagicMock()
        mock_connection.read_until.return_value = b"Switch#"
        telnet.access = mock_connection

        result = telnet.disable_paging()

        mock_connection.write.assert_called_once_with(b"term len 0\n")
        assert result == b"Switch#"


class TestTelnetClearBuffer:
    """Tests for Telnet buffer clearing."""

    def test_clear_buffer(self) -> None:
        """Test clear buffer is a no-op for Telnet."""
        telnet = Telnet("switch1", "admin", "secret")
        result = telnet.clear_buffer()
        assert result is None


class TestTelnetClose:
    """Tests for Telnet connection closing."""

    def test_close_connection(self) -> None:
        """Test closing Telnet connection."""
        telnet = Telnet("switch1", "admin", "secret")

        mock_connection = MagicMock()
        telnet.access = mock_connection

        telnet.close()
        mock_connection.close.assert_called_once()

    def test_close_no_connection(self) -> None:
        """Test closing when no connection exists."""
        telnet = Telnet("switch1", "admin", "secret")
        telnet.close()  # Should not raise any exception
