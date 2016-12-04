from hash_verification.hash_verification import HashVerification
from face.face_verification import FaceVerification
import serial
import time
import util

#Time executing verification script in seconds
VERIFICATION_TIME = 20
DETECTED_NFC = "DETECTED"
VERIFIED = "OK"
FACE_NOT_VERIFIED = "NO_FACE"
NFC_NOT_VERIFIED = "NO_NFC"

if __name__ == "__main__":

    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=2)
    nfc_verification = HashVerification(ser)
    firebase = util.FirebaseDB()
    face_verification = FaceVerification(VERIFICATION_TIME)
    while True:
        if ser.readline().strip() == DETECTED_NFC:
            nfc_verified = False
            face_verified = False
            user_id = nfc_verification.verify_NFC_tag()
            if user_id:
                nfc_verified = True
                # Verify Face. If Face OK: face_verified = True and send OK to Arduino. Else: send NOT to Arduino
                identified_persons = face_verification.run()
                print "NFC verified"
                if len(identified_persons) > 0:
                    # Get the Microsoft Person Id for the User Id verified by NFC
                    nfc_user_microsoft_id = firebase.getDatabase().child("groups").child(util.PersonGroupId.get()).child("users").child(user_id).child("microsoftId").get(firebase.getAccessToken()).val()
                    # If the person who was verified by NFC appears in camera, face is verified
                    if nfc_user_microsoft_id in identified_persons:
                        face_verified = True

                    if face_verified:
                        print "Face verified :" + user_id
                        ser.write(VERIFIED.encode())
                    else: # If not, face not verified
                        print "Face not verified"
                        ser.write(FACE_NOT_VERIFIED.encode())
                else:
                    print "Face not verified"
                    ser.write(FACE_NOT_VERIFIED.encode())
            else:
                print "NFC not verified"
                ser.write(NFC_NOT_VERIFIED.encode())
            
            data = {"nfc": nfc_verified, "face": face_verified, "uid": user_id, "datetime": int(round(time.time() * 1000))}
            access_id = firebase.getDatabase().child("groups").child(util.PersonGroupId.get()).child("accesses").push(data, firebase.getAccessToken())