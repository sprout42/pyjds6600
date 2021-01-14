#!/usr/bin/env python3

from setuptools import setup, find_packages

__version__ = '0.1'

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='jds6600',
    packages=find_packages(),
    install_requires=required,
    version=__version__ ,
    python_requires='>=3.8',
)
