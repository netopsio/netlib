#!/usr/bin/env python

from setuptools import setup


setup(
    name='netlib',
    version='0.0.3',
    url='https://github.com/jtdub/netlib',
    author='James Williams',
    license='MIT',
    install_requires=[
        'paramiko',
        'pycrypto',
        'pysnmp'
    ],
    description='Simple access to network devices, such as routers and switches, via Telnet, SSH, and SNMP',
    packages=[
        'netlib',
    ],
    package_data={'netlib':['*']},
)
