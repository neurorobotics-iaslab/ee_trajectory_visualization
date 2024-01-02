# ee_trajectory_visualization

It take as input a .mat file and return an image with the path followed by the end effector. 

## structure of the mat file
The mat file must each value vector of the same length. Additionally the parameters needed:
- **event**        : which contains the last BCI event 
- **from**         : which contains the reference frame position
- **to**           : which contains the name of the frame
- **translation_x**: which contain the value to move frame 'from' to frame 'to' on x direction of frame 'from'
- **transaltion_y**: which contain the value to move frame 'from' to frame 'to' on y direction of frame 'from'