% transform the tags position form kinect frame to mount. This function
% depends on the calibration, therefore works only for our system
function final_pos = tags_pos_transformation(tags)
    tr_x = tags.tr.x;
    tr_y = tags.tr.y;
    tr_z = tags.tr.z;
    translation_base_kinect = [0.064; 0.759; 2.021];
    rotation_base_kinect = [0.016; 0.977; -0.203; -0.058];
    tf_base_kinect = quaternionTranslation_to_transformationMatrix(rotation_base_kinect, translation_base_kinect);
    
    final_position = zeros(0, 3);
    for i = 1:length(tr_x)
        point = [tr_x(i, 1); tr_y(i, 1); tr_z(i, 1); 1];
        point = tf_base_kinect * point;

        final_position = [final_position; point(1:3)'];
    end
    final_pos.tr.x = final_position(:,1);
    final_pos.tr.y = final_position(:,2);
    final_pos.tr.z = final_position(:,3);
end