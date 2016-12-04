#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: hash_verification.py
Description: module for Hash Verification in SHK.
"""
import util
import hashlib
import time
from datetime import datetime

class HashVerification(object):
    """Verifies whether the hash that Arduino sends is from the group associated to the door"""

    def __init__(self, serialConnection):
        super(HashVerification, self).__init__()
        self.ser = serialConnection
        
        firebase = util.FirebaseDB()
        # Object to access firebase database
        self.db = firebase.getDatabase()
        # Access token to database
        self.db_access_token = firebase.getAccessToken()

        # Person group ID of authorized persons in Microsoft API
        self.person_group_id = util.PersonGroupId.get()

    def verify_NFC_tag(self):
        # Key to decrypt NFC tag
        NFC_key = self.db.child("groups").child(self.person_group_id).child("key").get(self.db_access_token).val()

        all_group_users = self.db.child("groups").child(self.person_group_id).child("users").get(self.db_access_token)
        user_id_hashes = {}
        for user in all_group_users.each():
            # Arduino should send one of theese hashes (read from the NFC tag) 
            user_id_hashes[hashlib.sha384(user.key()).hexdigest()] = user.key()

        self.ser.write(NFC_key.encode())
        nfc_hash = self.ser.readline().strip().lower()

        if nfc_hash in user_id_hashes:
            return user_id_hashes[nfc_hash]
        else:
            return None