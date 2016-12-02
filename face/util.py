#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: util.py
Description: util module for Face Verification in SHK.
"""

from threading import Thread
import os.path

import cognitive_face as CF

UTIL_DIR = os.path.dirname(os.path.abspath(__file__)) + '/'
CONFIG_DIR = UTIL_DIR + 'config/'
SUBSCRIPTION_KEY_FILENAME = CONFIG_DIR + 'Subscription.txt'
PERSON_GROUP_ID_FILENAME = CONFIG_DIR + 'PersonGroupId.txt'

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

class PersonGroupId(object):
    """Person group ID in Microsoft API"""

    @classmethod
    def get(cls):
        """Get the person group ID"""
        if not hasattr(cls, 'person_group_id'):
            cls.person_group_id = ''
        if not cls.person_group_id:
            if os.path.isfile(PERSON_GROUP_ID_FILENAME):
                with file(PERSON_GROUP_ID_FILENAME) as fin:
                    cls.person_group_id = fin.read().strip()
            else:
                cls.person_group_id = ''
        return cls.person_group_id

    @classmethod
    def set(cls, person_group_id):
        """Set the subscription key."""
        cls.person_group_id = person_group_id
        with file(PERSON_GROUP_ID_FILENAME, 'w') as fout:
            print >>fout, person_group_id

    @classmethod
    def delete(cls):
        """Delete the subscription person_group_id."""
        cls.person_group_id = ''
        if os.path.isfile(PERSON_GROUP_ID_FILENAME):
            os.remove(PERSON_GROUP_ID_FILENAME)