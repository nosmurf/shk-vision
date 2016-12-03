# shk-vision

This is an Face detection part for "shk" project.

In this repo We are working in Face detector application, this App should do:

- Check if the user can login with his face, if he can, open the door, else, send an error.

We are using Raspberry PI with camera for do this.

# Hardware requisites

This project has to be executed in a **Raspberry Pi** with the **picamera** module. Moreover, it has to be conected by USB with an **Arduino** running the code in [shk-Arduino](https://github.com/nosmurf/shk-arduino)

# Install dependencies

To use the software, it's necessary to install OpenCV for Python, Python SDK for the Microsoft Face API and PiCamera module:

```bash
sudo apt-get install ipython python-opencv python-numpy python-dev
sudo easy_install pip
sudo pip install cognitive_face
sudo pip install "picamera[array]"
sudo pip install pyrebase
sudo pip install pyserial
```

# Execution

## Before execution

1. [Create a Person Group in Microsoft Face API](https://dev.projectoxford.ai/docs/services/563879b61984550e40cbbe8d/operations/563879b61984550f30395244). This will return a Person Group ID which will be used later.

2. [Create Persons for that Person Group](https://dev.projectoxford.ai/docs/services/563879b61984550e40cbbe8d/operations/563879b61984550f3039523c)

3. [Add faces for each of the Persons created in the Person Group](https://dev.projectoxford.ai/docs/services/563879b61984550e40cbbe8d/operations/563879b61984550f3039523b)

4. [Train Person Group](https://dev.projectoxford.ai/docs/services/563879b61984550e40cbbe8d/operations/563879b61984550f30395249)

## To run the project

1. Clone the repo: `git clone https://github.com/nosmurf/shk-vision.git`

2. Go to shk-vision\face\config and:
  1. Write Microsoft Face API key in subscription.txt
  2. Write the Microsoft Person Group ID in PersonGroupId.txt
  3. Write configuration to access Firebase in Firebase.json
  
3. Go to the folder which contains the cloned repo

3. Execute the program: `python shk-vision`

# License

![his work is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License](https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png)

Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License
