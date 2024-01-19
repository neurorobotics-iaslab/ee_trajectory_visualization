# ee_trajectory_visualization

It take as input a .mat file with some variables, as can be seen in the following section. In addiction the main file is <i>ee_trajectory_visualizer_2D.py</i>.

## files explanation
- **draws_functions.py**: contains base functions to draw a ee trajectory
- **metrics.py**        : contains functions that compute the metrics which will be analysed
- **utility_files.py**  : contains functions to extract informations form files
- **utility:robot.py**  : contains function to trasformate points from one frame to another

## structure of the mat file
The mat file must each value vector of the same length. Additionally the parameters needed:
- **event**        : which contains the last BCI event 
- **from**         : which contains the reference frame position
- **to**           : which contains the name of the frame
- **translation_x**: which contain the value to move frame 'from' to frame 'to' on x direction of frame 'from'
- **transaltion_y**: which contain the value to move frame 'from' to frame 'to' on y direction of frame 'from'
- **transaltion_z**: which contain the value to move frame 'from' to frame 'to' on z direction of frame 'from'
- **rotation_x**   : which contain the value to rotate frame 'from' to frame 'to' on x direction of frame 'from'
- **rotation_y**   : which contain the value to rotate frame 'from' to frame 'to' on y direction of frame 'from'
- **rotation_z**   : which contain the value to rotate frame 'from' to frame 'to' on z direction of frame 'from'
- **rotation_w**   : which contain the value to rotate frame 'from' to frame 'to' on w direction of frame 'from'
