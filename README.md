# ee_trajectory_visualization

The project is composed by two main files: initlia_analysis.m and final_analysis.m. 
The first one was used to understand the initial trajectories forllowed by the ee and compute a new type of metric which we discard later.
The second one provides all the results about the ee trajectory reported in our paper.

Both files uses as input a .mat file with some variables and structures.

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
