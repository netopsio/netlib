class KeyRing(object):

    def __init__(self, username):
        import keyring
        import getpass
        self.username = username
        self.keyring = keyring
        self.getpass = getpass

    def get_creds(self):
        if self.keyring.get_password('nl_user_pass',
                                     username=self.username) is None:
            print('No credentials keyring exist. Creating new credentials.')
            self.set_creds()
        else:
            user_pass = self.keyring.get_password('nl_user_pass',
                                                  username=self.username)
            enable_pass = self.keyring.get_password('nl_enable_pass',
                                                    username=self.username)
            return {'username': self.username,
                    'password': str(user_pass),
                    'enable': str(enable_pass)}

    def set_creds(self):
        match = False
        while match is False:
            password1 = self.getpass.getpass('Enter your user password: ')
            password2 = self.getpass.getpass('Confirm your user password: ')
            if password1 == password2:
                user_password = password1
                match = True
        match = False
        while match is False:
            password1 = self.getpass.getpass('Enter your enable password: ')
            password2 = self.getpass.getpass('Confirm your enable password: ')
            if password1 == password2:
                enable_password = password1
                match = True
        user_pass = self.keyring.set_password('nl_user_pass',
                                              username=self.username,
                                              password=user_password)
        enable_pass = self.keyring.set_password('nl_enable_pass',
                                                username=self.username,
                                                password=enable_password)
        self.get_creds()

    def del_creds(self):
        tries = 0
        max_tries = 5
        while tries <= max_tries:
            user_pass = self.keyring.get_password('nl_user_pass',
                                                  username=self.username)
            ask_pass = self.getpass.getpass('Enter your user password: ')
            if user_pass == ask_pass:
                print('Deleting keyring credentials for {}'.format(
                    self.username))
                self.keyring.delete_password('nl_user_pass',
                                             username=self.username)
                self.keyring.delete_password('nl_enable_pass',
                                             username=self.username)
                tries = max_tries + 1
            else:
                tries += 1
                print('Error: Incorrect password.')
