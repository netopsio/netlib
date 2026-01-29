"""NetLib - Network device connection library."""

__name__ = "netlib"
__version__ = "0.2.0"

from netlib.conn_type import SSH, Telnet
from netlib.user_keyring import KeyRing

__all__ = ["SSH", "Telnet", "KeyRing"]
