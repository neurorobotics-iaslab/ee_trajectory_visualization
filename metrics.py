'''
This file contains all the functions used to compute the metrics.
'''

import numpy as np

############################################################################################ metrics computed and analysed
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
     

# compute the velocity, acceleration and jerk for each trial and show them
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