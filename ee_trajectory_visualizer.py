from scipy.io import loadmat

# load the mat file
filename = "/home/paolo/Scaricati/ur_data/ur_data20231215.115243.mat"
mat_file = loadmat(filename)

# take useful informations
event = mat_file['event']
base = mat_file['from']
to = mat_file['to']
translation_x = mat_file['translation_x']
translation_y = mat_file['translation_y']

