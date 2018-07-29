import dlib
import scipy.misc
import numpy as np
import os
import utils
import time



#----------------------------------------------------- Get encoding from owner ------------------------------
openning_process = True
# Get path to all the known images
image_filenames = filter(lambda x: x.endswith('.jpg'), os.listdir('images/'))
# Sort in alphabetical order
image_filenames = sorted(image_filenames)
# Get full paths to images
paths_to_images = ['images/' + x for x in image_filenames]

# List of face encodings we have
face_encodings = []

# Loop over images to get the encoding one by one
for path_to_owner_image in paths_to_images:
    # Get face encodings from the image
    face_encodings_in_image = utils.get_face_encodings(path_to_owner_image)

    # Make sure there's exactly one face in the image
    if len(face_encodings_in_image) != 1:
        print("Change image: " + path_to_owner_image + " - it has " + str(len(face_encodings_in_image)) + " faces; it can only have one")
        exit()

    # Append the face encoding found in that image to the list of face encodings we have
    face_encodings.append(utils.get_face_encodings(path_to_owner_image)[0])


#----------------------------------------------------- Capture environnement pics and compare encodings------------------------------

while True:
    utils.get_environement_pictures()

    test_filenames = filter(lambda x: x.endswith('.jpg'), os.listdir('test/'))
    paths_to_test_images = ['test/' + x for x in test_filenames]
    # Get list of owners names
    names = [x[:-4] for x in image_filenames]
    face_detection = []

    print('-----'+str(len(paths_to_test_images)))
    # Iterate over environement images
    for path_to_env_image in paths_to_test_images:
        # Get face encodings from the environement image
        face_encodings_in_image = utils.get_face_encodings(path_to_env_image)

        # Make sure there's exactly one face in the image
        if len(face_encodings_in_image) != 1:
            print("You should be alone")
            face_detection.append('Not Found')
        else:
            # Find match for the face encoding found in this test image
            match = utils.find_match(face_encodings, names, face_encodings_in_image[0])
            face_detection.append(match)
            # Print the path of test image and the corresponding match
            print(path_to_env_image, match)
        
    if utils.isAllowed(face_detection, validation_percent=0.6):
        if openning_process:
            print('Openning door...')
            openning_process = False
            utils.sleepBetweenProcess(15)
        else:
            print('Closing door...')
            openning_process = True
            utils.sleepBetweenProcess(15)
        #exit()
    else:
        print('Owner is not recognize...')
    
    utils.clean_test_directory()

