"""The ring.py file is where the class for establishing a keyring is located.
"""

from getpass import getpass

import keyring


def credential_match(password_type: str) -> str:
    """A function for validating matching passwords."""
    match = False

    while match is False:
        password1 = getpass(f"enter your {password_type} password: ")
        password2 = getpass(f"confirm your {password_type} password: ")

        if password1 == password2:
            match = True

        print(f"Your {password_type} passwords do not match.")

    return password1


class KeyRing:
    """The KeyRing class is used to manage username and password credentials in the OS keyring."""

    username: str

    def get_creds(self) -> dict:
        """Get creds is used to fetch the credentials from the key ring."""
        if keyring.get_password("nl_user_pass", username=self.username) is None:
            print("No credentials keyring exist. Creating new credentials.")
            self.set_creds()

        user_pass = keyring.get_password("nl_user_pass", username=self.username)
        enable_pass = keyring.get_password("nl_enable_pass", username=self.username)
        return {
            "username": self.username,
            "password": str(user_pass),
            "enable": str(enable_pass),
        }

    def set_creds(self) -> dict:
        """Creates keyring credentials."""
        user_password = credential_match("user")
        enable_password = credential_match("enable")

        keyring.set_password(
            "nl_user_pass", username=self.username, password=user_password
        )
        keyring.set_password(
            "nl_enable_pass", username=self.username, password=enable_password
        )
        return self.get_creds()

    def del_creds(self):
        """Delete credentials from a keyring."""
        tries = 0
        max_tries = 5
        while tries <= max_tries:
            user_pass = keyring.get_password("nl_user_pass", username=self.username)
            ask_pass = getpass("Enter your user password: ")
            if user_pass == ask_pass:
                print(f"Deleting keyring credentials for {self.username}")
                keyring.delete_password("nl_user_pass", username=self.username)
                keyring.delete_password("nl_enable_pass", username=self.username)
                tries = max_tries + 1
            else:
                tries += 1
                print("Error: Incorrect password.")
