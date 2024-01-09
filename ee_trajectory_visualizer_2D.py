from scipy.io import loadmat
import matplotlib.pyplot as plt
import numpy as np
import os

# initial exception class
class NotEqualLenException(Exception):
    pass

# check if the length of the passed parameters are equals
def compare_lens(event, base, to, translation_x, translation_y):
    if len(event) != len(base) or len(base) != len(to) or len(to) != len(translation_x) or len(translation_x) != len(translation_y):
        err_string = f"One of the vectors has a different length.\n  event size: {len(event)},\n  base size: {len(base)},\n  to size: {len(to)}, \
        \n  translation_x size: {len(translation_x)}, \n  translation_y size: {len(translation_y)}."
        raise NotEqualLenException(err_string)

# given the directory of all .mat files, return the path of all the files
def getFiles(directory):
    filenames = []
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        filenames.append(filepath)
    
    return filenames

# extract useful informations from mat
def extractInfoo(mat_file):
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

def getTranslationRotations_ee(events, base, to, translations, rotations, trial_pointer = False, events_required=[781,33549], \
     base_str= "base", to_str="tool0_controller"):
    trials_translations = np.empty((0, 3))
    trials_rotations = np.empty((0,4))
    trial_pos = np.array([])
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

# print all the trials into one image
def print_2d(translations,pointer,ax):
    pointer = np.append(pointer, len(translations)-1) # we need also the final length of the pointer vector
    colors = np.random.rand(len(pointer)-1, 3)
    for i in range(len(pointer)-1):
        x_c = translations[int(pointer[i]):int(pointer[i+1]-1), 0]
        y_c = translations[int(pointer[i]):int(pointer[i+1]-1), 1]
        label = "Trial " + str(i)
        c_color = np.tile(np.array(colors[i]), len(x_c)).reshape(-1, len(colors[i]))

        ax.scatter(x_c, y_c, c=c_color, marker='o', label=label, s=1)

    return ax

def draw_base(ax):
    ax.scatter(0,0,c='black', marker='D', label="base", s=1)
    return ax

def getTranslationRotations_target(base, to, targets, translations, rotations, base_str="/kinect2_rgb_optical_frame"):
    translations_targets = np.empty((0,3))
    rotations_targets = np.empty((0,4))

    find_targets = [False, False, False, False, False]

    for i in range(len(base)):
        for j in range(len(find_targets)):
            if to[i].replace(" ", "") == targets[j] and (not find_targets[j]):
                translations_targets = np.vstack((translations_targets, translations[i]))
                rotations_targets = np.vstack((rotations_targets, rotations[i]))

    return [translations_targets, rotations_targets]




# load the mat file
directory = "/home/paolo/Scaricati/ur_data"
files = getFiles(directory)

for file in files:
    print(f"Processing file: {file}")
    # load file and extract informations
    mat_file = loadmat(file)
    events, base, to, translations, rotations = extractInfoo(mat_file)     

    # get the translation and the rotation of ee during cf and pick
    events_required = [781, 33549, 1000, 1001, 1002, 1003, 1004] # cf, end of cf, pick for all target
    req_translations, req_rotations, pointer = getTranslationRotations_ee(events, base, to, translations, rotations, trial_pointer=True, events_required=events_required) 

    cues = get_cue(events)
    print(cues)

    # get positions of targets
    targets = ["tag_0", "tag_1", "tag_2", "tag_3", "tag_4"]
    translations_kect_targets, rotations_kinect_targets = getTranslationRotations_target(base, to, targets, translations, rotations) # now we have kinect -> target
    translation_base_kinect = np.array([0.064, 0.759, 2.021])
    rotation_base_kinect = np.array([0.016, 0.977, -0.203, -0.058])

 
    # Create a 3D plot
    fig = plt.figure()
    ax = fig.add_subplot(111)

    # print the points
    ax = draw_base(ax)
    #ax = draw_cubes(ax, translations, rotations)
    ax = print_2d(req_translations, pointer, ax)

    # Set labels and title
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.set_title(f"file: {file}")

    # Show the plot
    plt.legend()
    plt.show()