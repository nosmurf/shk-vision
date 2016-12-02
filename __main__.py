#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: main.py
Description: main script for Face verification.
"""

import face.face_verification as FV
import face.util as util

#Time executing verification script in seconds
VERIFICATION_TIME = 20

if __name__ == "__main__":

    app = FV.FaceVerification(VERIFICATION_TIME);
    identified_persons = app.run();

    if len(identified_persons) > 0:
    	print "Identified :"
    	for person_id in identified_persons:
    		print "* " + person_id
    else:
    	print "Nobody indentified"

    