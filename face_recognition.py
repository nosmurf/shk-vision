import util
import StringIO
import cv2
import numpy as np

_key = util.SubscriptionKey.get()
_image_format = ".jpg"

face_cascade = cv2.CascadeClassifier("HaarCascades/face.xml")
video_capture = cv2.VideoCapture(0)

global detections
detections = False

def detect_face_open_cv(image):
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(20, 20),
        flags=cv2.cv.CV_HAAR_DO_CANNY_PRUNING
    )

    # Return if at least a face has been detected
    return len(faces) > 0

@util.async
def async_detect(path):
    """Async detection."""

    global detections
    faces = util.CF.face.detect(path)

    if faces is not None:

        print(faces[0]["faceId"])

    # Close object and discard memory buffer
    path.close()
    
    detections = False


# Capture video and try to detect faces in each frame

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # if openCV detects a face, send to Microsoft API
    if detect_face_open_cv(gray):
        if not detections:
            detections = True
            
            # As detection API needs a image file, create a buffer with the encoded image
            ret, image_encoded = cv2.imencode(_image_format, gray)
            output = StringIO.StringIO()
            # Write to buffer and return reading pointer to beginning
            output.write(image_encoded.tostring())
            output.seek(0)
            async_detect(output)

    # Display the resulting frame
    cv2.imshow('Video', gray)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break