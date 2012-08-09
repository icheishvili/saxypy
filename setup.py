#!/usr/bin/env python

from setuptools import setup

setup(
    name='saxypy',
    version='0.1',
    description='SaxyPy XML utilities',
    long_description=\
        'SaxyPy makes dealing with XML as easy as dealing with JSON.',
    platforms='Platform Independent',
    author='Ilia Cheishvili',
    author_email='ilia.cheishvili@gmail.com',
    url='http://www.github.com/icheishvili/saxypy',
    scripts=[
        'scripts/saxypy-pretty-print',
    ],
    packages=[
        'saxypy',
    ],
)