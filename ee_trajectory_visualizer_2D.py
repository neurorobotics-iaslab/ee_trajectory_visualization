from scipy.io import loadmat
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import os

COLORS = np.array([
    [255/255,   0,   0], # red
    [255/255, 165/255,   0], # orange
    [  0, 128/255,   0], # green
    [  0,   0, 255/255], # blue
    [128/255,   0, 128/255] # purple
    ])

TARGETS_ORDER = np.array([0,3,4,1,2])

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
def get_files(directory):
    filenames = []
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        filenames.append(filepath)
    
    return filenames

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

# print all the trials into one image
def draw_trajectory(translations, pointer, colors, ax):   
    pointer = np.append(pointer, len(translations)-1) # we need also the final length of the pointer vector
    for i in range(len(pointer)-1):
        x_c = translations[pointer[i]:pointer[i+1]-1, 0]
        y_c = translations[pointer[i]:pointer[i+1]-1, 1]
        c_color = np.tile(np.array(colors[i]), len(x_c)).reshape(-1, len(colors[i]))
        ax.scatter(x_c, y_c, c=c_color, marker='o', s=1, label=f"trial {i}")

    return ax

def draw_base(ax):
    ax.scatter(0,0,c='black', marker='D', label="base", s=15)
    return ax

def draw_target(ax, points, targets_order, colors_targets, width, height):
    # sort the target points according to x coords
    indices = np.argsort(points[:, 0])
    points = points[indices]

    # draw rect for each tags
    i = 0
    for point in points:
        #rect = patches.Rectangle((point[0]-width/2.0, point[1]-height/2), width, height, edgecolor='r', facecolor='none')
        rect = patches.Rectangle((point[0]-width/2.0, point[1]-height/2), width, height, edgecolor=colors_targets[i,:], facecolor='none')
        ax.text(point[0], point[1] + height, f"tag_{targets_order[i]}", ha='center', va='center')
        ax.add_patch(rect)
        i = i + 1
    return ax

def plot_everything(points_trajectories, points_targets, tragets_order, colors_trials, colors_targets, pointer, name_file):
    # Create a 2D plot
    fig = plt.figure(f"trajectories file: {name_file}")
    ax = fig.add_subplot(111)

    # print the points
    ax = draw_base(ax)
    ax = draw_trajectory(points_trajectories, pointer, colors_trials, ax)
    ax = draw_target(ax, points_targets, tragets_order, colors_targets, 0.02, 0.02)

    # Set labels and title
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.set_title(f"file: {name_file}")

    # Show the plot
    plt.legend()
    plt.axis([-0.5, 0.5, -0.05, 0.95])

    plt.savefig(f"plot_{name_file}.png")
    #plt.show()

def get_target_position(base, to, tragets_order, translations, rotations,  translation_base_kinect, rotation_base_kinect, base_str="/kinect2_rgb_optical_frame"):
    translations_targets = np.empty((0,3))
    rotations_targets = np.empty((0,4))

    find_targets = [False] * len(tragets_order)

    # take the translation and rotation of each target with respect to base_str frame
    for i in range(len(base)):
        for j in tragets_order:
            if (to[i].replace(" ", "") == f"tag_{j}" and base[i].replace(" ", "") == base_str) and (not find_targets[j]):
                translations_targets = np.vstack((translations_targets, translations[i]))
                rotations_targets = np.vstack((rotations_targets, rotations[i]))
                find_targets[j] = True

    # compute the transfromation matrix starting from rotation and translation matrix
    tf_base_kinect = quaternionTranslation_to_transformationMatrix(rotation_base_kinect, translation_base_kinect)
    points = np.empty((0,3))

    for i in range(len(translations_targets)):
        tmp_target = np.ones(4)
        tmp_target[0:3] = translations_targets[i,:]
        
        point = np.dot(tf_base_kinect, tmp_target)

        points = np.vstack((points, point[0:3]))
    
    return points

def getColors(cues, targes_order):
    # compute a dict with cue : color
    cue_color_dict = {}
    for i in range(len(targes_order)):
        cue_color_dict[targes_order[i]] = COLORS[i]

    # compute the vector with th ecolor for all trial
    colors_trials = np.empty((0,3))
    for cue in cues:
        colors_trials = np.vstack((colors_trials, cue_color_dict[cue]))

    return [colors_trials, COLORS]


def quaternionTranslation_to_transformationMatrix(q, translation):
    x, y, z, w = q
    tx, ty, tz = translation
    
    rotation_matrix = np.array([
        [1 - 2*y*y - 2*z*z, 2*x*y - 2*w*z, 2*x*z + 2*w*y],
        [2*x*y + 2*w*z, 1 - 2*x*x - 2*z*z, 2*y*z - 2*w*x],
        [2*x*z - 2*w*y, 2*y*z + 2*w*x, 1 - 2*x*x - 2*y*y]
    ])

    transformation_matrix = np.eye(4)
    transformation_matrix[0:3, 0:3] = rotation_matrix
    transformation_matrix[0:3, 3] = [tx, ty, tz]
    
    return transformation_matrix



def vel_acc_jerk_4_trial(x, y, pointer):
    pointer = np.append(pointer, len(x))
    print(pointer)
    for i in range(0, len(pointer)-1):
        positions_x = x[pointer[i]:pointer[i+1]-1]
        velocity_x = np.gradient(positions_x, 1)
        acceleration_x = np.gradient(velocity_x, 1)
        jerk_x = np.gradient(acceleration_x, 1)

        positions_y = y[pointer[i]:pointer[i+1]-1]
        velocity_y = np.gradient(positions_y, 1)
        acceleration_y = np.gradient(velocity_y, 1)
        jerk_y = np.gradient(acceleration_y, 1)

        fig = plt.figure(f"analisis trial {i}")
        plt.subplot(2,3,1)
        plt.plot(range(len(velocity_x)), velocity_x, label='velocity_x')
        plt.legend()

        plt.subplot(2,3,2)
        plt.plot(range(len(acceleration_x)), acceleration_x, label='acceleration_x')
        plt.legend()

        plt.subplot(2,3,3)
        plt.plot(range(len(jerk_x)), jerk_x, label='jerk_x')
        plt.legend()

        plt.subplot(2,3,4)
        plt.plot(range(len(velocity_y)), velocity_y, label='velocity_y')
        plt.legend()

        plt.subplot(2,3,5)
        plt.plot(range(len(acceleration_y)), acceleration_y, label='acceleration_y')
        plt.legend()

        plt.subplot(2,3,6)
        plt.plot(range(len(jerk_y)), jerk_y, label='jerk_y')
        plt.legend()
    
    plt.show()
    
def calculate_angle(x1,y1,x2,y2):
    delta_x = x2-x1
    delta_y = y2-y1

    angle_rad = np.arctan2(delta_y, delta_x)

    return angle_rad

def metric(ee_positions, pointer, targets_positions, targets_order, cues, step=5):
    # sort the position of targets in order to have correct labeling using targets_order
    indices = np.argsort(targets_positions[:,0])
    target_positions_sorted = targets_positions[indices]
    
    # add the final pointer
    pointer = np.append(pointer, len(ee_positions))

    # variable with all error for all trials
    mean_err_4_trial = np.array([])

    # iterate over trials
    for i in range(len(pointer)-1):
        # save initial position ee
        ee_start_position = ee_positions[pointer[i],:]

        # take only few points of the trajectory
        pointer_points_used = np.arange(pointer[i]+1, pointer[i+1]-1, step) # +1 since first position is used as initial pos for ee
        
        # take the correct target position
        for t in range(len(targets_order)):
            if targets_order[t] == cues[i]:
                i_target = t
        correct_target_position = target_positions_sorted[i_target,:]
        # print(f"current target pos: {correct_target_position}, cue: {cues[i]}")

        # compute the correct angle which connect first position of ee and target
        correct_angle = calculate_angle(ee_start_position[0], ee_start_position[1], correct_target_position[0], correct_target_position[1])
        
        # variable initialization
        err = np.array([])
        # iterate over points to use except the last point which is the target one
        for j in range(len(pointer_points_used)-1):
            c_ee_x = ee_positions[pointer_points_used[j], 0]
            c_ee_y = ee_positions[pointer_points_used[j], 1]

            n_ee_x = ee_positions[pointer_points_used[j+1], 0]
            n_ee_y = ee_positions[pointer_points_used[j+1], 1]

            c_angle = calculate_angle(c_ee_x, c_ee_y, n_ee_x, n_ee_y)

            err = np.append(err, abs(c_angle - correct_angle))
        
        mean_err_4_trial = np.append(mean_err_4_trial, np.mean(err))
        #print(f"Trial: {i}, step: {step}, error computed for: {len(err)} segments, error mean: {np.mean(err)} rad")
    
    return mean_err_4_trial
     






# load the mat file
directory = "/home/paolo/Scaricati/ur_data_correct"
files = get_files(directory)
print(f"files to process: {len(files)}")
for file in files:
    ############################## LOAD FILE AND EXTRACT ALL INFORMATIONS
    #file = directory + "/ur_data20231215.173304_new.mat"
    print(f"Processing file: {file}")
    mat_file = loadmat(file)
    name_file = file.split('/')[len(file.split('/'))-1]
    name_file = name_file[0:len(name_file)-4]
    events, base, to, translations, rotations = extract_infoo(mat_file)     

    ############################## REASONING FOR PLOTTING
    # get the translation and the rotation of ee during cf and pick. All is with respect to base frame
    events_required = [781, 33549, 1000, 1001, 1002, 1003, 1004] # cf, end of cf, pick for all target
    ee_positions, ee_rotations, pointer = get_translation_rotations_ee(events, base, to, translations, rotations, trial_pointer=True, events_required=events_required) 

    # get the cues and set the colors according them
    cues = get_cue(events)
    colors_trials, colors_targets = getColors(cues, TARGETS_ORDER + 5000)

    # get positions of targets with respect to base frame
    translation_base_kinect = np.array([0.064, 0.759, 2.021])
    rotation_base_kinect = np.array([0.016, 0.977, -0.203, -0.058])
    targets_positions = get_target_position(base, to, TARGETS_ORDER, translations, rotations, translation_base_kinect, rotation_base_kinect) # now we have kinect -> target

    # plot all
    plot_everything(ee_positions, targets_positions, TARGETS_ORDER, colors_trials, colors_targets, pointer, name_file)

    ############################## REASONING FOR METRIC
    # shows velocity, acceleration and jerk starting from position (x,y) of the end-effector
    #vel_acc_jerk_4_trial(ee_positions[1:,0], ee_positions[1:,1], pointer) # --> close to zero

    # check if metrics need to be computed also for the picking or not
    metric_with_pick = False
    if not metric_with_pick:
        events_required = [781, 33549] # cf, end of cf
        ee_positions, ee_rotations, pointer = get_translation_rotations_ee(events, base, to, translations, rotations, trial_pointer=True, events_required=events_required) 
    
    steps_to_check = 5
    all_mena4trial = np.empty((0,10))
    fig = plt.figure(f"best steps for: {name_file}")
    ax = fig.add_subplot(111)
    for i in range(1,steps_to_check):
        mean_4_trial = metric(ee_positions, pointer, targets_positions, TARGETS_ORDER + 5000, cues, i)
        print(f"mean for trial: {mean_4_trial}")
        ax.scatter(mean_4_trial, range(len(mean_4_trial)), s=10, label=f"steps: {i}")
        ax.legend()
        ax.set_ylabel("trial")
        ax.set_xlabel("error")

plt.show()


