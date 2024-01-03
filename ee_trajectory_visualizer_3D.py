import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.io import loadmat

# initial exception class
class NotEqualLenException(Exception):
    pass

# check if the length of the passed parameters are equals
def compare_lens(event, base, to, translation_x, translation_y, translation_z):
    if len(event) != len(base) or len(base) != len(to) or len(to) != len(translation_x) or len(translation_x) != len(translation_y) or \
       len(translation_y) != len(translation_z):
        err_string = f"One of the vectors has a different length.\n  event size: {len(event)},\n  base size: {len(base)},\n  to size: {len(to)}, \
        \n  translation_x size: {len(translation_x)}, \n  translation_y size: {len(translation_y)}."
        raise NotEqualLenException(err_string)

# return x and y of the required from-to frame transformation on a specific event. 
# Parameters: 
#   event: vector with all the events, 
#   base: vector with all base vector
#   to: vector with all to frame
#   translation_x: vector with all translation of x of the end effector
#   translation_y: vector with all translation of y of the end effector
#   translation_z: vector with all translation of z of the end effector
#   event_required: int of the event, 
#   base_str: string of the base frame, 
#   to_str: string of the to frame
def getXYZ(event, base, to, translation_x, translation_y, translation_z, trial_pointer = False, events_required=[781,33549],\
     base_str= "base", to_str="tool0_controller"):
    x = np.array([])
    y = np.array([])
    z = np.array([])
    trial_pos = np.array([])
    first = True
    for i in range(len(to)):

        # check if correct event according to the one searched
        flag = False
        for c_event in events_required:
            if event[i] == c_event:
                flag = True

        # check for frames
        if flag and base[i].replace(" ", "") == base_str.replace(" ", "") and to[i].replace(" ", "") == to_str.replace(" ", ""):
            x = np.append(x, translation_x[i])
            y = np.append(y, translation_y[i])
            z = np.append(z, translation_z[i])
            if first:
                first = False
                trial_pos = np.append(trial_pos, len(x)-1)
        
        # update the flag used to save first element of the trial
        if not flag: 
            first = True

    if trial_pointer:
        return [x, y, z, trial_pos]
    else:
        return [x, y, z]

# print all the trials into one image
def print_3d(x,y,z,pointer,ax):
    pointer = np.append(pointer, len(x)-1) # we need also the final length of the pointer vector
    colors = np.random.rand(len(pointer)-1, 3)
    for i in range(len(pointer)-1):
        x_c = x[int(pointer[i]):int(pointer[i+1]-1)]
        y_c = y[int(pointer[i]):int(pointer[i+1]-1)]
        z_c = z[int(pointer[i]):int(pointer[i+1]-1)]
        label = "Trial " + str(i)
        c_color = np.tile(np.array(colors[i]), len(x_c)).reshape(-1, len(colors[i]))

        ax.scatter(x_c, y_c, z_c, c=c_color, marker='o', label=label, s=1)
    
    # Set labels and title
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.set_zlabel('Z-axis')
    ax.set_title('3D Scatter Plot')

    return ax

# load the mat file
filename = "/home/paolo/Scaricati/ur_data/ur_data20231221.120230.mat"
mat_file = loadmat(filename)

# take useful informations and check them
event = mat_file['event'][0]
base = mat_file['from']
to = mat_file['to']
translation_x = mat_file['translation_x'][0]
translation_y = mat_file['translation_y'][0]
translation_z = mat_file['translation_z'][0]
try:
    compare_lens(event, base, to, translation_x, translation_y, translation_z)
except NotEqualLenException as e:
    print("Caught NotEqualLenException: ", e)

# get the x and y useful values in cm
x, y, z, pointer = getXYZ(event, base, to, translation_x, translation_y, translation_z, trial_pointer=True)

# Create a 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

print_3d(x,y,z,pointer,ax)

# Show the plot
plt.legend()
plt.show()