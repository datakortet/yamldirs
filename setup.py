#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""yamldirs - create directories and files (incl. contents) from yaml spec.
"""
import sys
from setuptools import setup, find_packages


classifiers = """\
Development Status :: 5 - Production/Stable
Intended Audience :: Developers
Programming Language :: Python
Programming Language :: Python :: 2
Programming Language :: Python :: 2.7
Programming Language :: Python :: 3
Programming Language :: Python :: 3.5
Programming Language :: Python :: 3.6
Programming Language :: Python :: 3.7
Programming Language :: Python :: 3.8
Topic :: Software Development :: Libraries
"""

version = '1.1.13'


setup(
    name='yamldirs',
    version=version,
    install_requires=[
        'ruamel.yaml'
    ],
    author='Bjorn Pettersen',
    author_email='bp@datakortet.no',
    url='https://github.com/datakortet/yamldirs',
    description=__doc__.strip(),
    classifiers=[line for line in classifiers.split('\n') if line],
    long_description=open('README.rst').read(),
    entry_points={
        'console_scripts': [
            'yamldirs = yamldirs.yamldirs_cmd:main',
        ]
    },
    packages=find_packages(),
    zip_safe=False,
)
