import dlib
import scipy.misc
import numpy as np
import os
import time 
import RPi.GPIO as GPIO

#------ INIT GPIO ------
# Use GPIO pin numbers
GPIO.setmode(GPIO.BOARD)
# set up GPIO pin 7 as an output, pin 6 is GROUND
GPIO.setup(7, GPIO.OUT, initial=GPIO.LOW)

#------ INIT PRETRAINED NETWORK ------
# Get Face Detector from dlib
face_detector = dlib.get_frontal_face_detector()
# Detect landmark points in faces and angle of it
shape_predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
# Get the face recognition model
face_recognition_model = dlib.face_recognition_model_v1('dlib_face_recognition_resnet_model_v1.dat')
TOLERANCE = 0.6


def get_face_encodings(path_to_image):
    '''
    Return face encodings
    '''
    image = scipy.misc.imread(path_to_image)
    detected_faces = face_detector(image, 1)
    shapes_faces = [shape_predictor(image, face) for face in detected_faces]
    return [np.array(face_recognition_model.compute_face_descriptor(image, face_pose, 1)) for face_pose in shapes_faces]


def compare_face_encodings(known_faces, face):
    '''
    Finds the difference between each known face and the given face
    '''
    return (np.linalg.norm(known_faces - face, axis=1) <= TOLERANCE)


def find_match(known_faces, names, face):
    '''
    Get a list of True/False values indicating whether or not there's a match
    '''
    matches = compare_face_encodings(known_faces, face)

    count = 0
    for match in matches:
        if match:
            return names[count]
        count += 1
    return 'Not Found'

def get_environement_pictures(nb_sec=2):
    '''
    Capture an image each 0.1 second, and store them it in the ./test folder
    '''
    os.system('cd ./test; gtimeout '+str(nb_sec)+' imagesnap -t 0.1')

def clean_test_directory():
    '''
    Delete images in the ./test folder
    '''
    os.system('cd ./test; rm *.jpg')

def isAllowed(match_array, validation_percent=0.6):
    '''
    Return if an action of closing or openning is allowed according to the TOLERANCE
    '''
    nb_prediction = 0

    for match in match_array:
        if 'owner' in match:
            nb_prediction += 1

    if (nb_prediction / len(match_array)) > validation_percent:
        return True
    else:
        return False

def activate_remote_control():
    '''
    Activate the remote control for 1 sec
    '''
    GPIO.output(7, True)
    sleepBetweenProcess(1)
    GPIO.output(7, False)

def sleepBetweenProcess(nbSec):
    '''
    Sleep the main thread for nbSec
    '''
    print('Timer : '+str(time.time()))
    time.sleep(nbSec)
    print('Timer : '+str(time.time()))
    