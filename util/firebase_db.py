import pyrebase
import util

class FirebaseDB(object):
    """Provides access to Firebase Database"""

    def __init__(self):
        super(FirebaseDB, self).__init__()
        # Connect to Firebase database
        firebase_config = util.FirebaseConfig.get()
        firebase = pyrebase.initialize_app(firebase_config["appConfig"])
        # Log in firebase to get the token
        self.access_token = firebase.auth().sign_in_with_email_and_password(firebase_config["email"], firebase_config["password"])['idToken']
        self.db = firebase.database()

    def getDatabase(self):
        "Returns firebase database object"
        return self.db

    def getAccessToken(self):
        "Returns token to access to Firebase database"
        return self.access_token