from utility_files import *
from utility_robot import *
from draws_functions import *
from metrics import *
import numpy as np
import os

TARGETS_ORDER = np.array([0,3,4,1,2])

# plot all the information of the trajectories
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

    #plt.savefig(f"plot_{name_file}.png")        #################################################################################
    plt.show()


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


