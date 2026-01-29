# NetLib

[![CI](https://github.com/netopsio/netlib/actions/workflows/ci.yml/badge.svg)](https://github.com/netopsio/netlib/actions/workflows/ci.yml)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![Type checked: mypy](https://img.shields.io/badge/type%20checked-mypy-blue.svg)](http://mypy-lang.org/)

NetLib is a modern Python library for establishing SSH and Telnet connections to network devices such as routers and switches. It provides a clean, type-safe API with comprehensive input validation using Pydantic.

## Features

- ✨ **Modern Python**: Built for Python 3.10+ with full type hints
- 🔒 **Type Safety**: Comprehensive type checking with mypy
- ✅ **Input Validation**: Pydantic models for robust input/output validation
- 🧪 **Well Tested**: Extensive test coverage with pytest
- 📦 **Poetry**: Modern dependency management
- 🔍 **Linting**: Code quality ensured with ruff, mypy, and pylint
- 🚀 **CI/CD**: Automated testing with GitHub Actions

## Requirements

- Python 3.10 or higher
- Poetry (for development)

## Installation

### Using pip

```bash
pip install netlib
```

### Using Poetry

```bash
poetry add netlib
```

### From Source

```bash
git clone https://github.com/netopsio/netlib.git
cd netlib
poetry install
```

## Quick Start

### SSH Connection

```python
from netlib import SSH

# Create SSH connection
ssh = SSH('router.example.com', 'admin', 'password')

# Connect to device
ssh.connect()

# Disable paging for long output
ssh.disable_paging()

# Execute commands
output = ssh.command('show version')
print(output)

# Execute multiple commands
outputs = ssh.commands(['show version', 'show interfaces'])

# Enter privileged mode
ssh.set_enable('enable_password')

# Close connection
ssh.close()
```

### Telnet Connection

```python
from netlib import Telnet

# Create Telnet connection
telnet = Telnet('switch.example.com', 'admin', 'password')

# Connect to device
telnet.connect()

# Disable paging
telnet.disable_paging()

# Execute commands
output = telnet.command('show version')
print(output.decode('utf-8'))

# Close connection
telnet.close()
```

### Credential Management with KeyRing

NetLib provides secure credential storage using your operating system's native keyring (Keychain on macOS, Credential Manager on Windows, etc.):

```python
from netlib import KeyRing

# Initialize KeyRing with username
keyring = KeyRing(username='admin')

# Get credentials (will prompt to create if they don't exist)
creds = keyring.get_creds()
# Returns: {'username': 'admin', 'password': 'user_password', 'enable': 'enable_password'}

# Use with SSH/Telnet
ssh = SSH('router.example.com', creds['username'], creds['password'])
ssh.connect()
ssh.set_enable(creds['enable'])

# Update credentials
keyring.set_creds()

# Delete credentials
keyring.del_creds()
```

## API Reference

### SSH Class

**Constructor**:
```python
SSH(device_name: str, username: str, password: str,
    buffer: int = 65535, delay: float = 1.0, port: int = 22)
```

**Methods**:
- `connect()` - Establish SSH connection
- `close()` - Close the connection
- `command(command: str) -> str` - Execute a single command
- `commands(commands_list: list[str] | str) -> str` - Execute multiple commands
- `disable_paging(command: str = 'term len 0')` - Disable output paging
- `set_enable(enable_password: str) -> str` - Enter privileged mode
- `clear_buffer() -> str | None` - Clear the receive buffer

### Telnet Class

**Constructor**:
```python
Telnet(device_name: str, username: str, password: str,
       delay: float = 2.0, port: int = 23)
```

**Methods**:
- `connect()` - Establish Telnet connection
- `close()` - Close the connection
- `command(command: str) -> bytes` - Execute a single command
- `commands(commands_list: list[str] | str) -> str` - Execute multiple commands
- `disable_paging(command: str = 'term len 0') -> bytes` - Disable output paging
- `set_enable(enable_password: str) -> str` - Enter privileged mode

### KeyRing Class

**Constructor**:
```python
KeyRing(username: str)
```

**Methods**:
- `get_creds() -> dict[str, str]` - Retrieve credentials from keyring
- `set_creds()` - Set or update credentials
- `del_creds()` - Delete credentials from keyring

## Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/netopsio/netlib.git
cd netlib

# Install dependencies
poetry install

# Activate virtual environment
poetry shell
```

### Running Tests

```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=netlib

# Run specific test file
poetry run pytest tests/test_ssh.py
```

### Code Quality

```bash
# Format code
poetry run ruff format .

# Lint code
poetry run ruff check .

# Type check
poetry run mypy netlib

# Run pylint
poetry run pylint netlib

# Run all checks
poetry run ruff format --check . && \
poetry run ruff check . && \
poetry run mypy netlib && \
poetry run pylint netlib
```

## What's New in v0.2.0

- 🎯 **Python 3.10+ Only**: Removed Python 2.x support
- 🔒 **Type Hints**: Full type annotations throughout the codebase
- ✅ **Pydantic Validation**: Input/output validation using Pydantic models
- 📦 **Poetry**: Migrated from setuptools to Poetry for package management
- 🧪 **Pytest**: Comprehensive test suite with high coverage
- 🔍 **Modern Linting**: ruff, mypy, and pylint integration
- 🚀 **GitHub Actions**: Automated CI/CD pipeline (replacing Travis CI)
- 📚 **Better Documentation**: Improved API documentation and examples

## Migration from v0.1.x

The API remains largely compatible with v0.1.x, but there are some important changes:

1. **Python Version**: Python 3.10+ is now required
2. **Type Safety**: All methods now have type hints
3. **Validation**: Invalid inputs will now raise Pydantic `ValidationError`
4. **Installation**: Use Poetry or pip (no more `setup.py install`)

### Example Migration

**Before (v0.1.x)**:
```python
ssh = SSH('router', 'admin', 'pass', buffer="8192", delay="2")
```

**After (v0.2.0)**:
```python
# Still works! String values are automatically converted
ssh = SSH('router', 'admin', 'pass', buffer="8192", delay="2")

# But you can now use proper types
ssh = SSH('router', 'admin', 'pass', buffer=8192, delay=2.0)
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and linting (`poetry run pytest && poetry run ruff check .`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Credits

NetLib is a rewrite of [pyRouterLib](https://github.com/jtdub/pyRouterLib) with a focus on modern Python practices, type safety, and maintainability.

## Author

James Williams

## Links

- **GitHub**: https://github.com/netopsio/netlib
- **Issues**: https://github.com/netopsio/netlib/issues
