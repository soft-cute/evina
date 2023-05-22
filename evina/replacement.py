#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
# @Time    : 2023/05/01 00:27:19
# @Author  : 橙橙橙心滴
# @File    : replacement.py
'''

import io
import os
from contextlib import contextmanager

from aligo import EMailConfig
from aligo.core.Auth import Auth
from dynaconf.vendor.dotenv.compat import StringIO
from dynaconf.vendor.dotenv.main import DotEnv
from loguru import logger


class ReplaceMent:
    def __init__(self) -> None:
        pass

    @contextmanager
    def new_get_stream(self):
        A = self
        if isinstance(A.dotenv_path, StringIO): yield A.dotenv_path
        elif os.path.isfile(A.dotenv_path):
            with io.open(A.dotenv_path, encoding='utf8') as B:
                yield B
        else:
            if A.verbose:
                logger.info(
                    'Python-dotenv could not find configuration file %s.',
                    A.dotenv_path or '.env')
            yield StringIO('')
