'''
This file contains all the functions to get the informations from the .mat files.
'''

from scipy.io import loadmat
import numpy as np
import os

############################################################################################ get infoo files
# given the directory of all .mat files, return the path of all the files
def get_files(directory):
    filenames = []
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        filenames.append(filepath)
    
    return filenames


############################################################################################ extract infoo from files
# extract useful informations from mat
def extract_infoo(mat_file):
    # take useful informations and check them
    event = mat_file['event'][0]
    base = mat_file['from'] # it contains: "base", "\kinect2_rgb_optical_frame"
    to = mat_file['to']     # it contains: "tool0_controller", "tag_0", "tag_1", "tag_2", "tag_3", "tag_4"

    # take translation
    translation_x = mat_file['translation_x'][0]
    translation_y = mat_file['translation_y'][0]
    translation_z = mat_file['translation_z'][0]
    translation = np.array([translation_x[0], translation_y[0], translation_z[0]])
    for i in range(1, len(translation_x)):
        translation = np.vstack((translation, np.array([translation_x[i], translation_y[i], translation_z[i]])))

    # take rotation
    rotation_x = mat_file['rotation_x'][0]
    rotation_y = mat_file['rotation_y'][0]
    rotation_z = mat_file['rotation_z'][0]
    rotation_w = mat_file['rotation_w'][0]
    rotation = np.array([rotation_x[0], rotation_y[0], rotation_z[0], rotation_w[0]])
    for i in range(1, len(rotation_x)):
        rotation = np.vstack((rotation, np.array([rotation_x[i], rotation_y[i], rotation_z[i], rotation_w[i]])))
    
    # check the length
    try:
        compare_lens(event, base, to, translation, rotation)
        return [event, base, to, translation, rotation]
    except NotEqualLenException as e:
        print("Caught NotEqualLenException: ", e)


# initial exception class
class NotEqualLenException(Exception):
    pass

# check if the length of the passed parameters are equals
def compare_lens(event, base, to, translation_x, translation_y):
    if len(event) != len(base) or len(base) != len(to) or len(to) != len(translation_x) or len(translation_x) != len(translation_y):
        err_string = f"One of the vectors has a different length.\n  event size: {len(event)},\n  base size: {len(base)},\n  to size: {len(to)}, \
        \n  translation_x size: {len(translation_x)}, \n  translation_y size: {len(translation_y)}."
        raise NotEqualLenException(err_string)

def get_translation_rotations_ee(events, base, to, translations, rotations, trial_pointer = False, events_required=[781,33549], \
     base_str= "base", to_str="tool0_controller"):
    trials_translations = np.empty((0, 3))
    trials_rotations = np.empty((0,4))
    trial_pos = np.array([], dtype=int)
    first = True
    for i in range(len(to)):

        # check if correct event according to the one searched
        if events[i] in events_required: 
            # check for frames
            if base[i].replace(" ", "") == base_str.replace(" ", "") and to[i].replace(" ", "") == to_str.replace(" ", ""):
                if first:
                    first = False
                    if len(trial_pos) == 0:
                        trial_pos = np.append(trial_pos, 0)
                    else:
                        trial_pos = np.append(trial_pos, trials_translations.shape[0]-1)
                trials_rotations = np.vstack((trials_rotations, rotations[i,:]))
                trials_translations = np.vstack((trials_translations, translations[i,:]))

        # update the flag used to save first element of the trial
        else: 
            first = True

    if trial_pointer:
        return [trials_translations, trials_rotations, trial_pos]
    else:
        return [trials_translations, trials_rotations]

def get_cue(events, events_cue=[5000,5001,5002,5003,5004]):
    find_cue = True
    cues = np.array([])
    for event in events:
        if event in events_cue and find_cue:
            find_cue = False
            cues = np.append(cues, event)
        elif not (event in events_cue):
            find_cue = True
    
    return cues

