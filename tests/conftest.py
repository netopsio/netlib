"""Pytest configuration and fixtures."""

import pytest


@pytest.fixture
def mock_device_config() -> dict[str, str | int]:
    """Provide mock device configuration."""
    return {
        "device_name": "test-router",
        "username": "testuser",
        "password": "testpass",
        "port": 22,
    }


@pytest.fixture
def mock_enable_password() -> str:
    """Provide mock enable password."""
    return "enablepass"
