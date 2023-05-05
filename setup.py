#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
# @Time    : 2023/04/27 21:54:54
# @Author  : 橙橙橙心滴
# @File    : setup.py
'''

from setuptools import find_packages, setup

setup(name='evina',
      author='Ezong',
      version='1.0.1',
      packages=find_packages(),
      include_package_data=True,
      install_requires=['aligo', 'dynaconf', 'Faker', 'loguru', 'paramiko'],
      entry_points={'console_scripts': ['evina=evina.evina:start']})
