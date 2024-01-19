'''
This file contains all the functions to obtain position of targets with respect to base frame.
'''

import numpy as np

############################################################################################ extract robot infoo
# transform quaternion to rotation matrix
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

# obtain the position of the targets with respect to base frame
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