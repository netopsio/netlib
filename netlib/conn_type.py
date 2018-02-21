class SSH(object):

    def __init__(self, device_name, username, password, buffer="65535",
                 delay="1", port="22"):
        import paramiko
        import time
        import re
        self.paramiko = paramiko
        self.time = time
        self.re = re
        self.device_name = device_name
        self.username = username
        self.password = password
        self.buffer = int(buffer)
        self.delay = int(delay)
        self.port = int(port)

    def connect(self):
        self.pre_conn = self.paramiko.SSHClient()
        self.pre_conn.set_missing_host_key_policy(
            self.paramiko.AutoAddPolicy())
        self.pre_conn.connect(self.device_name, username=self.username,
                              password=self.password, allow_agent=False,
                              look_for_keys=False, port=self.port)
        self.client_conn = self.pre_conn.invoke_shell()
        self.time.sleep(float(self.delay))
        return self.client_conn.recv(self.buffer)

    def close(self):
        return self.pre_conn.close()

    def clear_buffer(self):
        if self.client_conn.recv_ready():
            return self.client_conn.recv(self.buffer).decode('utf-8', 'ignore')
        else:
            return None

    def set_enable(self, enable_password):
        if self.re.search('>$', self.command('\n')):
            enable = self.command('enable')
            if self.re.search('Password', enable):
                send_pwd = self.command(enable_password)
                return send_pwd
        elif self.re.search('#$', self.command('\n')):
            return "Action: None. Already in enable mode."
        else:
            return "Error: Unable to determine user privilege status."

    def disable_paging(self, command='term len 0'):
        self.client_conn.sendall(command + "\n")
        self.clear_buffer()

    def command(self, command):
        self.client_conn.sendall(command + "\n")
        not_done = True
        output = str()
        while not_done:
            self.time.sleep(float(self.delay))
            if self.client_conn.recv_ready():
                output += self.client_conn.recv(self.buffer).decode('utf-8')
            else:
                not_done = False
        return output

    def commands(self, commands_list):
        output = str()
        if list(commands_list):
            for command in commands_list:
                output += self.command(command)
        else:
            output += self.command(commands_list)
        return output


class Telnet(object):

    def __init__(self, device_name, username, password, delay="2", port="23"):
        import telnetlib
        import time
        import re
        self.telnetlib = telnetlib
        self.time = time
        self.re = re
        self.device_name = device_name
        self.username = username
        self.password = password
        self.delay = float(delay)
        self.port = int(port)

    def connect(self):
        self.access = self.telnetlib.Telnet(self.device_name, self.port)
        login_prompt = self.access.read_until(b"\(Username: \)|\(login: \)",
                                              self.delay)
        if b'login' in login_prompt:
            self.is_nexus = True
            self.access.write(self.username.encode('ascii') + b'\n')
        elif b'Username' in login_prompt:
            self.is_nexus = False
            self.access.write(self.username.encode('ascii') + b'\n')
        password_prompt = self.access.read_until(b'Password:',
                                                 self.delay)
        self.access.write(self.password.encode('ascii') + b'\n')
        return self.access

    def close(self):
        return self.access.close()

    def clear_buffer(self):
        pass

    def set_enable(self, enable_password):
        if self.re.search(b'>$', self.command('\n')):
            self.access.write(b'enable\n')
            enable = self.access.read_until(b'Password')
            return self.access.write(enable_password.encode('ascii') + b'\n')
        elif self.re.search(b'#$', self.command('\n')):
            return "Action: None. Already in enable mode."
        else:
            return "Error: Unable to determine user privilege status."

    def disable_paging(self, command='term len 0'):
        self.access.write(command.encode('ascii') + b'\n')
        return self.access.read_until(b"\(#\)|\(>\)", self.delay)

    def command(self, command):
        self.access.write(command.encode('ascii') + b'\n')
        return self.access.read_until(b"\(#\)|\(>\)", self.delay)

    def commands(self, commands_list):
        output = str()
        if list(commands_list):
            for command in commands_list:
                output += self.command(command)
        else:
            output += self.command(commands_list)
        return output
