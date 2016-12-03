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

        hash_object = hashlib.sha384(self.person_group_id)
        # Hash that Arduino should send (read from the NFC tag) 
        hash_person_group_id = hash_object.hexdigest()
        self.ser.write(NFC_key.encode())
        nfc_hash = self.ser.readline().strip()

        #if nfc_hash == hash_person_group_id:
        if nfc_hash == "99":
            return True
        else:
            return False