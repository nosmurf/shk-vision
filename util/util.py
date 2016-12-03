#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: util.py
Description: util module for Access Verification in SHK.
"""
import os.path
import json
import cognitive_face as CF

UTIL_DIR = os.path.dirname(os.path.abspath(__file__)) + '/'
CONFIG_DIR = UTIL_DIR + 'config/'
MS_FACE_API_KEY_FILENAME = CONFIG_DIR + 'MSFaceApiKey.txt'
PERSON_GROUP_ID_FILENAME = CONFIG_DIR + 'PersonGroupId.txt'
FIREBASE_CONFIG_FILENAME = CONFIG_DIR + 'Firebase.json'

class MSFaceApiKey(object):
    """Microsoft Face API Key."""

    @classmethod
    def get(cls):
        """Get the Microsoft Face API key."""
        if not hasattr(cls, 'key'):
            cls.key = ''
        if not cls.key:
            if os.path.isfile(MS_FACE_API_KEY_FILENAME):
                with file(MS_FACE_API_KEY_FILENAME) as fin:
                    cls.key = fin.read().strip()
            else:
                cls.key = ''
        CF.Key.set(cls.key)
        return cls.key

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

class FirebaseConfig(object):
    """Configuration to access to Firebase"""

    @classmethod
    def get(cls):
        """Get the configuration to access to Firebase"""
        if not hasattr(cls, 'firebase_config'):
            cls.firebase_config = {}
        if not cls.firebase_config:
            if os.path.isfile(FIREBASE_CONFIG_FILENAME):
                with file(FIREBASE_CONFIG_FILENAME) as fin:
                    cls.firebase_config = json.loads(fin.read())
            else:
                cls.firebase_config = {}
        return cls.firebase_config