import re
import telnetlib


class Telnet:
    device_name: str
    username: str
    password: str
    delay: float = 2
    port: int = 23

    def connect(self):
        self.access = telnetlib.Telnet(self.device_name, self.port)
        login_prompt = self.access.read_until(b"\(Username: \)|\(login: \)", self.delay)
        if b"login" in login_prompt:
            self.is_nexus = True
            self.access.write(self.username.encode("ascii") + b"\n")
        elif b"Username" in login_prompt:
            self.is_nexus = False
            self.access.write(self.username.encode("ascii") + b"\n")
        self.access.read_until(b"Password:", self.delay)
        self.access.write(self.password.encode("ascii") + b"\n")
        return self.access

    def close(self):
        return self.access.close()

    def clear_buffer(self) -> None:
        pass

    def set_enable(self, enable_password: str):
        if re.search(b">$", self.command("\n")):
            self.access.write(b"enable\n")
            enable = self.access.read_until(b"Password")
            return self.access.write(enable_password.encode("ascii") + b"\n")
        elif re.search(b"#$", self.command("\n")):
            return "Action: None. Already in enable mode."
        else:
            return "Error: Unable to determine user privilege status."

    def disable_paging(self, command: str = "term len 0") -> str:
        self.access.write(command.encode("ascii") + b"\n")
        return self.access.read_until(b"\(#\)|\(>\)", self.delay)

    def command(self, command: str) -> str:
        self.access.write(command.encode("ascii") + b"\n")
        return self.access.read_until(b"\(#\)|\(>\)", self.delay)

    def commands(self, commands_list: list) -> str:
        output = str()
        if list(commands_list):
            for command in commands_list:
                output += self.command(command)
        else:
            output += self.command(commands_list)
        return output
