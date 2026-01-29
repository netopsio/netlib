"""Tests for Pydantic models."""

import pytest
from pydantic import ValidationError

from netlib.models import (
    CommandResponse,
    CredentialsData,
    EnableModeResponse,
    SSHConnectionConfig,
    TelnetConnectionConfig,
)


class TestSSHConnectionConfig:
    """Tests for SSH connection configuration."""

    def test_valid_config(self) -> None:
        """Test valid SSH configuration."""
        config = SSHConnectionConfig(
            device_name="router1",
            username="admin",
            password="secret",
        )
        assert config.device_name == "router1"
        assert config.username == "admin"
        assert config.password == "secret"
        assert config.port == 22
        assert config.buffer == 65535
        assert config.delay == 1.0

    def test_custom_port(self) -> None:
        """Test custom SSH port."""
        config = SSHConnectionConfig(
            device_name="router1",
            username="admin",
            password="secret",
            port=2222,
        )
        assert config.port == 2222

    def test_invalid_port(self) -> None:
        """Test invalid port number."""
        with pytest.raises(ValidationError):
            SSHConnectionConfig(
                device_name="router1",
                username="admin",
                password="secret",
                port=70000,
            )

    def test_empty_device_name(self) -> None:
        """Test empty device name."""
        with pytest.raises(ValidationError):
            SSHConnectionConfig(
                device_name="",
                username="admin",
                password="secret",
            )


class TestTelnetConnectionConfig:
    """Tests for Telnet connection configuration."""

    def test_valid_config(self) -> None:
        """Test valid Telnet configuration."""
        config = TelnetConnectionConfig(
            device_name="switch1",
            username="admin",
            password="secret",
        )
        assert config.device_name == "switch1"
        assert config.port == 23
        assert config.delay == 2.0

    def test_custom_delay(self) -> None:
        """Test custom delay value."""
        config = TelnetConnectionConfig(
            device_name="switch1",
            username="admin",
            password="secret",
            delay=5.0,
        )
        assert config.delay == 5.0


class TestCommandResponse:
    """Tests for command response model."""

    def test_successful_response(self) -> None:
        """Test successful command response."""
        response = CommandResponse(output="show version output")
        assert response.output == "show version output"
        assert response.success is True
        assert response.error is None

    def test_error_response(self) -> None:
        """Test error command response."""
        response = CommandResponse(
            output="",
            success=False,
            error="Command not found",
        )
        assert response.success is False
        assert response.error == "Command not found"


class TestCredentialsData:
    """Tests for credentials data model."""

    def test_valid_credentials(self) -> None:
        """Test valid credentials."""
        creds = CredentialsData(
            username="admin",
            password="userpass",
            enable="enablepass",
        )
        assert creds.username == "admin"
        assert creds.password == "userpass"
        assert creds.enable == "enablepass"

    def test_empty_password(self) -> None:
        """Test empty password validation."""
        with pytest.raises(ValidationError):
            CredentialsData(
                username="admin",
                password="",
                enable="enablepass",
            )

    def test_whitespace_password(self) -> None:
        """Test whitespace-only password validation."""
        with pytest.raises(ValidationError):
            CredentialsData(
                username="admin",
                password="   ",
                enable="enablepass",
            )


class TestEnableModeResponse:
    """Tests for enable mode response model."""

    def test_successful_enable(self) -> None:
        """Test successful enable mode entry."""
        response = EnableModeResponse(message="Entered enable mode")
        assert response.message == "Entered enable mode"
        assert response.success is True
        assert response.already_enabled is False

    def test_already_enabled(self) -> None:
        """Test already in enable mode."""
        response = EnableModeResponse(
            message="Already in enable mode",
            already_enabled=True,
        )
        assert response.already_enabled is True
