from scipy.io import loadmat
from PIL import Image, ImageDraw
import numpy as np


class NotEqualLenException(Exception):
    pass

# check if the length of the passed parameters are equals
def compare_lens(event, base, to, translation_x, translation_y):
    if len(event) != len(base) or len(base) != len(to) or len(to) != len(translation_x) or len(translation_x) != len(translation_y):
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
#   event_required: int of the event, 
#   base_str: string of the base frame, 
#   to_str: string of the to frame
def getXY(event, base, to, translation_x, translation_y, event_required=781, base_str= "base", to_str="tool0_controller"):
    x = np.array([])
    y = np.array([])
    for i in range(len(to)):
        if event[i] == event_required and base[i].replace(" ", "") == base_str.replace(" ", "") and to[i].replace(" ", "") == to_str.replace(" ", "") and flag:
            x = np.append(x, translation_x[i])
            y = np.append(y, translation_y[i])

    return [x, y]

def draw_points(x, y, center, draw):
    point_color = (0, 0, 0) 
    for i in range(len(x)):
        print(f"point: ({center[0] + x[i]}, {center[1] - y[i]}), x: {x[i]}, y: {y[i]}")
        point_position = (center[0] + x[i], center[1] - y[i])
        draw.point(point_position, fill=point_color)

# load the mat file
filename = "/home/paolo/Scaricati/ur_data/ur_data20231221.120230.mat"
mat_file = loadmat(filename)

# take useful informations and check them
event = mat_file['event'][0]
base = mat_file['from']
to = mat_file['to']
translation_x = mat_file['translation_x'][0]
translation_y = mat_file['translation_y'][0]
try:
    compare_lens(event, base, to, translation_x, translation_y)
except NotEqualLenException as e:
    print("Caught NotEqualLenException: ", e)

# get the x and y useful values in cm
x, y = getXY(event, base, to, translation_x, translation_y)
x = x * 1000
y = y * 1000

# Create an empty image
width, height = 1000, 1000  # Dimensions of the image
background_color = (255, 255, 255)  # White background
img = Image.new("RGB", (width, height), background_color)

# define image settings
center = (width/2.0, height-1)

# Draw a point on the image
draw = ImageDraw.Draw(img)
draw_points(x,y,center,draw)

# Save the image
img.save("trajectory_plot.png")  # Save the image as PNG format
