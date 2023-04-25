"""Top-level package for chatify."""

__author__ = """NeuroMatch"""
__email__ = 'nma@neuromatch.io'
__version__ = '0.1.0'

from .main import Chatify


def load_ipython_extension(ipython):
    ipython.register_magics(Chatify)
