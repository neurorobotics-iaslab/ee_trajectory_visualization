'''
This file contains all the functions to draw the trajectories of the robot.
'''

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

COLORS = np.array([
    [255/255,   0,   0], # red
    [255/255, 165/255,   0], # orange
    [  0, 128/255,   0], # green
    [  0,   0, 255/255], # blue
    [128/255,   0, 128/255] # purple
    ])

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