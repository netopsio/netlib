"""Tests for KeyRing credential management."""

from unittest.mock import Mock, patch

from netlib.user_keyring import KeyRing


class TestKeyRingInit:
    """Tests for KeyRing initialization."""

    def test_init(self) -> None:
        """Test KeyRing initialization."""
        kr = KeyRing("testuser")
        assert kr.username == "testuser"


class TestKeyRingGetCreds:
    """Tests for retrieving credentials."""

    @patch("netlib.user_keyring.keyring.get_password")
    def test_get_existing_credentials(self, mock_get_password: Mock) -> None:
        """Test retrieving existing credentials."""
        mock_get_password.side_effect = ["userpass123", "enablepass123"]

        kr = KeyRing("testuser")
        creds = kr.get_creds()

        assert creds["username"] == "testuser"
        assert creds["password"] == "userpass123"
        assert creds["enable"] == "enablepass123"

    @patch("netlib.user_keyring.keyring.get_password")
    @patch("netlib.user_keyring.getpass.getpass")
    @patch("netlib.user_keyring.keyring.set_password")
    def test_get_creds_creates_new_when_none_exist(
        self,
        mock_set_password: Mock,
        mock_getpass: Mock,
        mock_get_password: Mock,
    ) -> None:
        """Test creating new credentials when none exist."""
        # First call returns None (no creds), subsequent calls return passwords
        mock_get_password.side_effect = [
            None,  # First check - no password exists
            "newuserpass",  # After setting
            "newenablepass",  # After setting
        ]
        mock_getpass.side_effect = [
            "newuserpass",  # Enter user password
            "newuserpass",  # Confirm user password
            "newenablepass",  # Enter enable password
            "newenablepass",  # Confirm enable password
        ]

        kr = KeyRing("testuser")
        with patch("builtins.print"):
            creds = kr.get_creds()

        assert creds["username"] == "testuser"
        assert creds["password"] == "newuserpass"
        assert creds["enable"] == "newenablepass"


class TestKeyRingSetCreds:
    """Tests for setting credentials."""

    @patch("netlib.user_keyring.keyring.set_password")
    @patch("netlib.user_keyring.keyring.get_password")
    @patch("netlib.user_keyring.getpass.getpass")
    def test_set_credentials_matching_passwords(
        self,
        mock_getpass: Mock,
        mock_get_password: Mock,
        mock_set_password: Mock,
    ) -> None:
        """Test setting credentials with matching passwords."""
        mock_getpass.side_effect = [
            "password1",  # Enter user password
            "password1",  # Confirm user password
            "enablepass1",  # Enter enable password
            "enablepass1",  # Confirm enable password
        ]
        mock_get_password.side_effect = ["password1", "enablepass1"]

        kr = KeyRing("testuser")
        kr.set_creds()

        assert mock_set_password.call_count == 2

    @patch("netlib.user_keyring.keyring.set_password")
    @patch("netlib.user_keyring.keyring.get_password")
    @patch("netlib.user_keyring.getpass.getpass")
    def test_set_credentials_retry_on_mismatch(
        self,
        mock_getpass: Mock,
        mock_get_password: Mock,
        mock_set_password: Mock,
    ) -> None:
        """Test password retry when confirmation doesn't match."""
        mock_getpass.side_effect = [
            "password1",  # Enter user password
            "wrongpass",  # Confirm user password (mismatch)
            "password1",  # Enter user password (retry)
            "password1",  # Confirm user password (match)
            "enablepass1",  # Enter enable password
            "enablepass1",  # Confirm enable password
        ]
        mock_get_password.side_effect = ["password1", "enablepass1"]

        kr = KeyRing("testuser")
        kr.set_creds()

        assert mock_set_password.call_count == 2


class TestKeyRingDelCreds:
    """Tests for deleting credentials."""

    @patch("netlib.user_keyring.keyring.delete_password")
    @patch("netlib.user_keyring.keyring.get_password")
    @patch("netlib.user_keyring.getpass.getpass")
    def test_delete_credentials_correct_password(
        self,
        mock_getpass: Mock,
        mock_get_password: Mock,
        mock_delete_password: Mock,
    ) -> None:
        """Test deleting credentials with correct password."""
        mock_get_password.return_value = "correctpass"
        mock_getpass.return_value = "correctpass"

        kr = KeyRing("testuser")
        with patch("builtins.print"):
            kr.del_creds()

        assert mock_delete_password.call_count == 2

    @patch("netlib.user_keyring.keyring.delete_password")
    @patch("netlib.user_keyring.keyring.get_password")
    @patch("netlib.user_keyring.getpass.getpass")
    def test_delete_credentials_incorrect_password(
        self,
        mock_getpass: Mock,
        mock_get_password: Mock,
        mock_delete_password: Mock,
    ) -> None:
        """Test attempting to delete with incorrect password."""
        mock_get_password.return_value = "correctpass"
        mock_getpass.side_effect = ["wrongpass"] * 6  # Will fail all attempts

        kr = KeyRing("testuser")
        with patch("builtins.print"):
            kr.del_creds()

        # Should not delete anything
        mock_delete_password.assert_not_called()

    @patch("netlib.user_keyring.keyring.delete_password")
    @patch("netlib.user_keyring.keyring.get_password")
    @patch("netlib.user_keyring.getpass.getpass")
    def test_delete_credentials_retry_on_wrong_password(
        self,
        mock_getpass: Mock,
        mock_get_password: Mock,
        mock_delete_password: Mock,
    ) -> None:
        """Test retry mechanism when wrong password is entered."""
        mock_get_password.return_value = "correctpass"
        mock_getpass.side_effect = ["wrongpass", "correctpass"]

        kr = KeyRing("testuser")
        with patch("builtins.print"):
            kr.del_creds()

        # Should delete after second attempt
        assert mock_delete_password.call_count == 2
