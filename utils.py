import dlib
import scipy.misc
import numpy as np
import os
import time 

#----------------------------------------------------- INIT ------------------------------

# Get Face Detector from dlib
# This allows us to detect faces in images
face_detector = dlib.get_frontal_face_detector()

# Get Pose Predictor from dlib
# This allows us to detect landmark points in faces and understand the pose/angle of the face
shape_predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

# Get the face recognition model
# This is what gives us the face encodings (numbers that identify the face of a particular person)
face_recognition_model = dlib.face_recognition_model_v1('dlib_face_recognition_resnet_model_v1.dat')

# This is the tolerance for face comparisons
# The lower the number - the stricter the comparison
# To avoid false matches, use lower value
# To avoid false negatives (i.e. faces of the same person doesn't match), use higher value
# 0.5-0.6 works well
TOLERANCE = 0.6

# This function will take an image and return its face encodings using the neural network
def get_face_encodings(path_to_image):
    # Load image using scipy
    image = scipy.misc.imread(path_to_image)

    # Detect faces using the face detector
    detected_faces = face_detector(image, 1)

    # Get pose/landmarks of those faces
    # Will be used as an input to the function that computes face encodings
    # This allows the neural network to be able to produce similar numbers for faces of the same people, regardless of camera angle and/or face positioning in the image
    shapes_faces = [shape_predictor(image, face) for face in detected_faces]

    # For every face detected, compute the face encodings
    return [np.array(face_recognition_model.compute_face_descriptor(image, face_pose, 1)) for face_pose in shapes_faces]


# This function takes a list of known faces
def compare_face_encodings(known_faces, face):
    # Finds the difference between each known face and the given face (that we are comparing)
    # Calculate norm for the differences with each known face
    # Return an array with True/Face values based on whether or not a known face matched with the given face
    # A match occurs when the (norm) difference between a known face and the given face is less than or equal to the TOLERANCE value
    return (np.linalg.norm(known_faces - face, axis=1) <= TOLERANCE)


# This function returns the name of the person whose image matches with the given face (or 'Not Found')
# known_faces is a list of face encodings
# names is a list of the names of people (in the same order as the face encodings - to match the name with an encoding)
# face is the face we are looking for
def find_match(known_faces, names, face):
    # Call compare_face_encodings to get a list of True/False values indicating whether or not there's a match
    matches = compare_face_encodings(known_faces, face)

    # Return the name of the first match
    count = 0
    for match in matches:
        if match:
            return names[count]
        count += 1

    # Return not found if no match found
    return 'Not Found'

def get_environement_pictures(nb_sec=2):
    os.system('cd ./test; gtimeout '+str(nb_sec)+' imagesnap -t 0.1')

def clean_test_directory():
    os.system('cd ./test; rm *.jpg')

def isAllowed(match_array, validation_percent=0.6):
    nb_prediction = 0

    for match in match_array:
        if 'owner' in match:
            nb_prediction += 1

    if (nb_prediction / len(match_array)) > validation_percent:
        return True
    else:
        return False

def sleepBetweenProcess(nbSec):
    print('Timer : '+str(time.time()))
    time.sleep(nbSec)
    print('Timer : '+str(time.time()))
    