"""Tests for module imports."""

# ruff: noqa: PLC0415


class TestImports:
    """Tests for importing netlib modules."""

    def test_import_keyring(self) -> None:
        """Test importing KeyRing class."""
        from netlib.user_keyring import KeyRing

        assert KeyRing is not None

    def test_import_ssh(self) -> None:
        """Test importing SSH class."""
        from netlib.conn_type import SSH

        assert SSH is not None

    def test_import_telnet(self) -> None:
        """Test importing Telnet class."""
        from netlib.conn_type import Telnet

        assert Telnet is not None

    def test_import_from_package(self) -> None:
        """Test importing from main package."""
        from netlib import SSH, KeyRing, Telnet

        assert SSH is not None
        assert Telnet is not None
        assert KeyRing is not None

    def test_import_models(self) -> None:
        """Test importing Pydantic models."""
        from netlib.models import (
            CommandResponse,
            CredentialsData,
            EnableModeResponse,
            SSHConnectionConfig,
            TelnetConnectionConfig,
        )

        assert SSHConnectionConfig is not None
        assert TelnetConnectionConfig is not None
        assert CommandResponse is not None
        assert CredentialsData is not None
        assert EnableModeResponse is not None
