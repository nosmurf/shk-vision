from hash_verification.hash_verification import HashVerification
from face.face_verification import FaceVerification
import serial
import time
import util

#Time executing verification script in seconds
VERIFICATION_TIME = 20

if __name__ == "__main__":

    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=5)
    nfc_verification = HashVerification(ser)
    nfc_verified = False
    face_verified = False
    microsoft_id = None
    firebase = util.FirebaseDB()
    face_verification = FaceVerification(VERIFICATION_TIME)
    while True:
        if nfc_verification.verify_NFC_tag():
            nfc_verified = True
            # Verify Face. If Face OK: face_verified = True and send OK to Arduino. Else: send NOT to Arduino
            identified_persons = face_verification.run()
            print "NFC validado"
            if len(identified_persons) > 0:
                print "Identificado :"
                for person_id in identified_persons:
                    print "* " + person_id
                microsoft_id = "68a90cd2-a8c5-4843-9e50-1731efe495c1"
                face_verified = True
                #ser.write("OK")
            else:
                print "Nobody indentified"
                #ser.write("NOT")
            time.sleep(1)
        else:
            print "NFC no validado"
            
        data = {"nfc": nfc_verified, "face": face_verified, "microsoftId": microsoft_id, "datetime": int(round(time.time() * 1000))}
        access_id = firebase.getDatabase().child("groups").child(util.PersonGroupId.get()).child("accesses").push(data, firebase.getAccessToken())