import dlib
import scipy.misc
import numpy as np
import os
import utils
import time


#------ Get encoding from owner ------
openning_process = True
image_filenames = filter(lambda x: x.endswith('.jpg'), os.listdir('images/'))
image_filenames = sorted(image_filenames)
paths_to_images = ['images/' + x for x in image_filenames]

# List of face encodings we have
face_encodings = []

for path_to_owner_image in paths_to_images:
    face_encodings_in_image = utils.get_face_encodings(path_to_owner_image)

    if len(face_encodings_in_image) != 1:
        print("Change image: " + path_to_owner_image + " - it has " + str(len(face_encodings_in_image)) + " faces;")
        exit()
    face_encodings.append(utils.get_face_encodings(path_to_owner_image)[0])


#------ Capture environnement pics and compare encodings ------
while True:
    utils.get_environement_pictures()

    test_filenames = filter(lambda x: x.endswith('.jpg'), os.listdir('test/'))
    paths_to_test_images = ['test/' + x for x in test_filenames]
    # Get list of owners names
    names = [x[:-4] for x in image_filenames]
    face_detection = []

    print('-----'+str(len(paths_to_test_images)))
    for path_to_env_image in paths_to_test_images:
        # Get face encodings from the environement image
        face_encodings_in_image = utils.get_face_encodings(path_to_env_image)

        if len(face_encodings_in_image) != 1:
            print("You should be alone")
            face_detection.append('Not Found')
        else:
            match = utils.find_match(face_encodings, names, face_encodings_in_image[0])
            face_detection.append(match)
            print(path_to_env_image, match)
        
    if utils.isAllowed(face_detection, validation_percent=0.6):
        if openning_process:
            print('Openning door...')
            utils.activate_remote_control()
            openning_process = False
            utils.sleepBetweenProcess(15)
        else:
            print('Closing door...')
            utils.activate_remote_control()
            openning_process = True
            utils.sleepBetweenProcess(15)
    else:
        print('Owner is not recognize...')
    
    utils.clean_test_directory()



