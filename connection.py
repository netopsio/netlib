from __future__ import unicode_literals

import paramiko
import time


class SSH(object):

    def __init__(self, device_name, username, password, buffer="65535", delay="1"):
        self.device_name = device_name
        self.username = username
        self.password = password 
        self.buffer = buffer
        self.delay = delay

    def connect(self):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(self.device_name, username=self.username,
                            password=self.password, allow_agent=False,
                            look_for_keys=False)

        return self.client

    def close(self):
        return self.client.close() 

    def command(self, command):
        self.client_shell = self.client.invoke_shell()
        output = self.client_shell.recv(self.buffer)
        self.client_shell.send(command + "\n")
        not_done = True
        while not_done:
            time.sleep(float(self.delay))
            if self.client_shell.recv_ready():
                output += self.client_shell.recv(self.buffer)
            else:
                not_done = False

        return output
