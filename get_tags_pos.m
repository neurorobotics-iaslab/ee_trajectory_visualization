% function to have the targs position ordered from the left one to the
% right
function final_position = get_tags_pos(tr_x, tr_y, tr_z)
    translation_base_kinect = [0.064; 0.759; 2.021];
    rotation_base_kinect = [0.016; 0.977; -0.203; -0.058];
    tf_base_kinect = quaternionTranslation_to_transformationMatrix(rotation_base_kinect, translation_base_kinect);
    
    final_position = zeros(0, 3);
    for i = 1:length(tr_x)
        point = [tr_x(i, 1); tr_y(i, 1); tr_z(i, 1); 1];
        point = tf_base_kinect * point;

        final_position = [final_position; point(1:3)'];
    end
    
    final_position = order_following_x(final_position);
end

function ordered_positions = order_following_x(positions)
    [~, order] = sort(positions(:, 1));
    ordered_positions = zeros(0, 3);
    for i = 1:length(order)
        ordered_positions = [ordered_positions; positions(order(i), :)];
    end
end
