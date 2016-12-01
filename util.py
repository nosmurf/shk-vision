#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: util.py
Description: util module for Python SDK sample.
"""

from threading import Thread
import os.path

import wx

try:
    import cognitive_face as CF
except ImportError:
    import sys
    ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, ROOT_DIR)
    import cognitive_face as CF

SUBSCRIPTION_KEY_FILENAME = 'Subscription.txt'

class SubscriptionKey(object):
    """Subscription Key."""

    @classmethod
    def get(cls):
        """Get the subscription key."""
        if not hasattr(cls, 'key'):
            cls.key = ''
        if not cls.key:
            if os.path.isfile(SUBSCRIPTION_KEY_FILENAME):
                with file(SUBSCRIPTION_KEY_FILENAME) as fin:
                    cls.key = fin.read().strip()
            else:
                cls.key = ''
        CF.Key.set(cls.key)
        return cls.key

    @classmethod
    def set(cls, key):
        """Set the subscription key."""
        cls.key = key
        with file(SUBSCRIPTION_KEY_FILENAME, 'w') as fout:
            print >>fout, key
        CF.Key.set(cls.key)

    @classmethod
    def delete(cls):
        """Delete the subscription key."""
        cls.key = ''
        if os.path.isfile(SUBSCRIPTION_KEY_FILENAME):
            os.remove(SUBSCRIPTION_KEY_FILENAME)
        CF.Key.set(cls.key)


def async(func):
    """Async wrapper."""
    def wrapper(*args, **kwargs):
        """docstring for wrapper"""
        thr = Thread(target=func, args=args, kwargs=kwargs)
        thr.start()
    return wrapper
