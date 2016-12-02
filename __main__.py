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
    idenfitied_persons = app.run();
    print "Identified :"
    print idenfitied_persons