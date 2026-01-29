"""Pydantic models for input and output validation."""

from typing import Any

from pydantic import BaseModel, Field, SecretStr, field_validator


class ConnectionConfig(BaseModel):
    """Configuration for network device connections."""

    device_name: str = Field(..., description="Device hostname or IP address", min_length=1)
    username: str = Field(..., description="Username for authentication", min_length=1)
    password: SecretStr = Field(..., description="Password for authentication")
    port: int = Field(default=22, description="Connection port", ge=1, le=65535)
    buffer: int = Field(default=65535, description="Buffer size for data reception", ge=1024)
    delay: float = Field(default=1.0, description="Delay in seconds", ge=0.1, le=60.0)

    model_config = {"frozen": False, "validate_assignment": True}

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: SecretStr) -> SecretStr:
        """Validate password is not empty."""
        secret_value = v.get_secret_value()
        if not secret_value or not secret_value.strip():
            msg = "Password cannot be empty"
            raise ValueError(msg)
        return v


class SSHConnectionConfig(ConnectionConfig):
    """SSH-specific connection configuration."""

    port: int = Field(default=22, description="SSH port", ge=1, le=65535)
    delay: float = Field(default=1.0, description="Delay in seconds", ge=0.1, le=60.0)


class TelnetConnectionConfig(ConnectionConfig):
    """Telnet-specific connection configuration."""

    port: int = Field(default=23, description="Telnet port", ge=1, le=65535)
    delay: float = Field(default=2.0, description="Delay in seconds", ge=0.1, le=60.0)


class CommandResponse(BaseModel):
    """Response from a device command."""

    output: str = Field(..., description="Command output")
    success: bool = Field(default=True, description="Whether command executed successfully")
    error: str | None = Field(default=None, description="Error message if any")

    model_config = {"frozen": False}


class CredentialsData(BaseModel):
    """User credentials data."""

    username: str = Field(..., description="Username", min_length=1)
    password: SecretStr = Field(..., description="User password")
    enable: SecretStr = Field(..., description="Enable/privileged password")

    model_config = {"frozen": False}

    @field_validator("password", "enable")
    @classmethod
    def validate_password_field(cls, v: SecretStr) -> SecretStr:
        """Validate password is not empty."""
        secret_value = v.get_secret_value()
        if not secret_value or not secret_value.strip():
            msg = "Password cannot be empty"
            raise ValueError(msg)
        return v


class EnableModeResponse(BaseModel):
    """Response from enable mode operations."""

    message: str = Field(..., description="Response message")
    already_enabled: bool = Field(
        default=False, description="Whether already in enable mode"
    )
    success: bool = Field(default=True, description="Whether operation succeeded")

    model_config = {"frozen": False}
