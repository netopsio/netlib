class SSH(object):

    def __init__(self, device_name, username, password, buffer="65535",
                 delay="1"):
        self.device_name = device_name
        self.username = username
        self.password = password
        self.buffer = buffer
        self.delay = delay

    def connect(self):
        import paramiko
        import time

        self.pre_conn = paramiko.SSHClient()
        self.pre_conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.pre_conn.connect(self.device_name, username=self.username,
                              password=self.password, allow_agent=False,
                              look_for_keys=False)
        self.client_conn = self.pre_conn.invoke_shell()
        time.sleep(float(self.delay))
        return self.client_conn.recv(self.buffer)

    def close(self):
        return self.pre_conn.close()

    def clear_buffer(self):
        if self.client_conn.recv_ready():
            return self.client_conn.recv(self.buffer)
        else:
            return None

    def set_enable(self, enable_password):
        import re

        if re.search('>$', self.command('\n')):
            enable = self.command('enable')
            if re.search('Password', enable):
                send_pwd = self.command(enable_password)
                return send_pwd
        elif re.search('#$', self.command('\n')):
            return "Action: None. Already in enable mode."
        else:
            return "Error: Unable to determine user privilege status."

    def disable_paging(self, command='term len 0'):
        self.clear_buffer()
        return self.client_conn.sendall(command + "\n")

    def command(self, command):
        import time

        self.client_conn.sendall(command + "\n")
        not_done = True
        output = ""
        self.clear_buffer()
        while not_done:
            time.sleep(float(self.delay))
            if self.client_conn.recv_ready():
                output += self.client_conn.recv(self.buffer)
            else:
                not_done = False
        return output


class Telnet(object):

    def __init__(self, device_name, username, password, delay="2"):
        self.device_name = device_name
        self.username = username
        self.password = password
        self.delay = float(delay)

    def connect(self):
        import telnetlib
        import sys

        self.access = telnetlib.Telnet(self.device_name)
        login_prompt = self.access.read_until("\(Username: \)|\(login: \)",
                                              self.delay)
        if 'login' in login_prompt:
            self.is_nexus = True
            self.access.write(self.username + '\n')
        elif 'Username' in login_prompt:
            self.is_nexus = False
            self.access.write(self.username + '\n')
        password_prompt = self.access.read_until('Password:',
                                                 self.delay)
        self.access.write(self.password + '\n')
        return self.access

    def close(self):
        return self.access.close()

    def set_enable(self, enable_password):
        import re

        if re.search('>$', self.command('\n')):
            self.access.write('enable\n')
            enable = self.access.read_until('Password')
            return self.access.write(enable_password + '\n')
        elif re.search('#$', self.command('\n')):
            return "Action: None. Already in enable mode."
        else:
            return "Error: Unable to determine user privilege status."

    def disable_paging(self, command='term len 0'):
        self.access.write(command + '\n')
        return self.access.read_until("\(#\)|\(>\)", self.delay)

    def command(self, command):
        self.access.write(command + '\n')
        return self.access.read_until("\(#\)|\(>\)", self.delay)


class SNMP(object):

    def __init__(self, device_name, snmp_community, symbol_name, mib_index="0",
                 mib_name="SNMPv2-MIB", snmp_version="2c", snmp_port="161"):
        self.device_name = device_name
        self.snmp_community = snmp_community
        self.symbol_name = symbol_name
        self.mib_index= mib_index
        self.mib_name = mib_name
        self.snmp_version = snmp_version
        self.snmp_port = snmp_port

    def snmp_get(self):
        from pysnmp.entity.rfc3413.oneliner import cmdgen

        cmdGen = cmdgen.CommandGenerator()
        errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
            cmdgen.CommunityData(self.snmp_community),
            cmdgen.UdpTransportTarget((self.device_name, self.snmp_port)),
            cmdgen.MibVariable(self.mib_name, self.symbol_name,
                               self.mib_index),
            lookupNames=True, lookupValues=True)

        if errorIndication:
            return errorIndication
        elif errorStatus:
            return errorStatus
        else:
            for name, val in varBinds:
                return val.prettyPrint()
