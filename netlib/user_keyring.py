"""User credential management using system keyring."""

import getpass

import keyring
from pydantic import SecretStr

from netlib.models import CredentialsData


class KeyRing:
    """Manage user credentials securely using the system keyring."""

    def __init__(self, username: str) -> None:
        """Initialize KeyRing with a username.

        Args:
            username: Username for credential storage
        """
        self.username = username

    def get_creds(self) -> dict[str, str]:
        """Retrieve credentials from the keyring.

        If credentials don't exist, prompts user to create them.

        Returns:
            Dictionary containing username, password, and enable password
        """
        user_pass = keyring.get_password("nl_user_pass", self.username)
        if user_pass is None:
            print("No credentials keyring exist. Creating new credentials.")
            self.set_creds()
            user_pass = keyring.get_password("nl_user_pass", self.username)

        enable_pass = keyring.get_password("nl_enable_pass", self.username)

        # Validate with Pydantic
        creds = CredentialsData(
            username=self.username,
            password=SecretStr(str(user_pass or "")),
            enable=SecretStr(str(enable_pass or "")),
        )

        return {
            "username": creds.username,
            "password": creds.password.get_secret_value(),
            "enable": creds.enable.get_secret_value(),
        }

    def set_creds(self) -> None:
        """Set or update credentials in the keyring.

        Prompts user for password and enable password with confirmation.
        """
        # Get user password with confirmation
        match = False
        while not match:
            password1 = getpass.getpass("Enter your user password: ")
            password2 = getpass.getpass("Confirm your user password: ")
            if password1 == password2:
                user_password = password1
                match = True

        # Get enable password with confirmation
        match = False
        while not match:
            password1 = getpass.getpass("Enter your enable password: ")
            password2 = getpass.getpass("Confirm your enable password: ")
            if password1 == password2:
                enable_password = password1
                match = True

        # Validate with Pydantic before storing
        creds = CredentialsData(
            username=self.username,
            password=SecretStr(user_password),
            enable=SecretStr(enable_password),
        )

        # Store in keyring
        keyring.set_password("nl_user_pass", self.username, creds.password.get_secret_value())
        keyring.set_password("nl_enable_pass", self.username, creds.enable.get_secret_value())

        self.get_creds()

    def del_creds(self) -> None:
        """Delete credentials from the keyring.

        Requires password confirmation. Maximum 5 attempts.
        """
        tries = 0
        max_tries = 5
        while tries <= max_tries:
            user_pass = keyring.get_password("nl_user_pass", self.username)
            ask_pass = getpass.getpass("Enter your user password: ")
            if user_pass == ask_pass:
                print(f"Deleting keyring credentials for {self.username}")
                keyring.delete_password("nl_user_pass", self.username)
                keyring.delete_password("nl_enable_pass", self.username)
                tries = max_tries + 1
            else:
                tries += 1
                print("Error: Incorrect password.")
