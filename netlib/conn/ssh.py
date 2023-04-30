import re
import time

import paramiko


class SSH:
    device_name: str
    username: str
    password: str
    buffer: int = 65535
    delay: int = 1
    port: int = 22

    def connect(self):
        self.pre_conn = paramiko.SSHClient()
        self.pre_conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.pre_conn.connect(
            self.device_name,
            username=self.username,
            password=self.password,
            allow_agent=False,
            look_for_keys=False,
            port=self.port,
        )
        self.client_conn = self.pre_conn.invoke_shell()
        time.sleep(float(self.delay))
        return self.client_conn.recv(self.buffer)

    def close(self):
        return self.pre_conn.close()

    def clear_buffer(self):
        if self.client_conn.recv_ready():
            return self.client_conn.recv(self.buffer).decode("utf-8", "ignore")

    def set_enable(self, enable_password: str):
        if re.search(">$", self.command("\n")):
            enable = self.command("enable")
            if re.search("Password", enable):
                send_pwd = self.command(enable_password)
                return send_pwd
        elif re.search("#$", self.command("\n")):
            return "Action: None. Already in enable mode."
        else:
            return "Error: Unable to determine user privilege status."

    def disable_paging(self, command: str = "term len 0") -> None:
        self.client_conn.sendall(command + "\n")
        self.clear_buffer()

    def command(self, command: str) -> str:
        self.client_conn.sendall(command + "\n")
        not_done = True
        output = str()
        while not_done:
            time.sleep(float(self.delay))
            if self.client_conn.recv_ready():
                output += self.client_conn.recv(self.buffer).decode("utf-8")
            else:
                not_done = False
        return output

    def commands(self, commands_list: list) -> str:
        output = str()
        if list(commands_list):
            for command in commands_list:
                output += self.command(command)
        else:
            output += self.command(commands_list)
        return output
