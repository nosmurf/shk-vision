#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: face_verification.py
Description: main module for Face Verification in SHK.
"""
import util
import StringIO
import cv2
import time
import os
from camera import Camera

class FaceVerification(object):
    """Verifies whether the user is allowed to access or not"""

    IMAGE_FORMAT = ".jpg"
    IMG_WIDTH = 640
    IMG_HEIGHT = 480

    def __init__(self, running_time):
        super(FaceVerification, self).__init__()
        util.SubscriptionKey.get()
        # Time to run detection
        self.running_time = running_time
        # Person group ID of authorized persons in Microsoft API
        self.person_group_id = util.PersonGroupId.get()
        # Haar cascade to detect faces in OpenCV
        self.openCV_face_detector = cv2.CascadeClassifier(os.path.dirname(os.path.abspath(__file__)) + "/HaarCascades/face.xml")

    def detect_face_open_cv(self, image):
        """Detects if there are any faces in the image"""
        faces = self.openCV_face_detector.detectMultiScale(
            image,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(20, 20),
            flags=cv2.cv.CV_HAAR_DO_CANNY_PRUNING
        )

        # Return True if at least a face has been detected
        return len(faces) > 0

    def face_verification(self, path):
        """Send image to Microsoft API to verify whether the user is allowed to access or not"""
        # IDs of the authorized persons that appear in the image
        identified_persons_ids = []

        # Get face ID for each face detected in image
        faces = util.CF.face.detect(path)
        detected_faces_ids = []
        if faces is not None:
            for face in faces:
                detected_faces_ids.append(face["faceId"])

        #If there is any detected face in image
        if len(detected_faces_ids) > 0:
            # Check if any of the faces detected in the image is authorized to enter
            identification_result = util.CF.face.identify(detected_faces_ids, self.person_group_id)
            # For each of the sent faces, check if it is one of the autorized persons
            for entry in identification_result:
                if entry['candidates']:
                    authorized_person_id = entry['candidates'][0]['personId']
                    identified_persons_ids.append(authorized_person_id)

        return identified_persons_ids

    def run(self):
        "Loop which tries to identify authorized persons in video which comes from camera during time setted in self.running_time"

        camera_raspberry = Camera(self.IMG_WIDTH, self.IMG_HEIGHT)

        identified_persons_ids = []

        start_time = time.time()
        actual_time = time.time()

        # Capture video and try to detect faces in each frame. If any is detected, verify if it's authorized
        while actual_time - start_time < self.running_time and len(identified_persons_ids) < 1:
            # Capture frame-by-frame
            gray_frame = camera_raspberry.capture_gray()

            # if openCV detects a face, send to Microsoft API
            if self.detect_face_open_cv(gray_frame):
                # As detection API needs a image file, create a buffer with the encoded image
                ret, image_encoded = cv2.imencode(self.IMAGE_FORMAT, gray_frame)
                image_buffer = StringIO.StringIO()
                # Write to buffer and return reading pointer to beginning
                image_buffer.write(image_encoded.tostring())
                image_buffer.seek(0)
                # Send image to Microsoft to verify if person is authorized
                identified_persons_ids = self.face_verification(image_buffer)
                # Close object and discard memory buffer
                image_buffer.close()

            actual_time = time.time()

        return identified_persons_ids