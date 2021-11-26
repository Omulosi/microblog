# -*- coding: utf-8 -*-
"""
    mcroblog
    ~~~~~~~
    Microblog is a ... written in python using the
    microframework Flask.
    
    :copyright: (c) 2021 by John Paul.
    :license: BSD, see LICENSE for more details.
"""
__version__ = "1.0.0"

import logging

logger = logging.getLogger(__name__)

from microblog.app import app #noqa

