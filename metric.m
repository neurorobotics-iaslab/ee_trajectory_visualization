function mean_err_4_trial = metric(ee_positions, pointer, targets_positions, targets_order, cues, step)
    % Sort the position of targets in order to have correct labeling using targets_order
    [~, indices] = sort(targets_positions(:, 1));
    target_positions_sorted = targets_positions(indices, :);
    
    % Add the final pointer
    pointer = [pointer, numel(ee_positions)];

    % Variable with all error for all trials
    mean_err_4_trial = [];
    
    % Iterate over trials
    for i = 1:numel(pointer)-1
        % Save initial position ee
        ee_start_position = ee_positions(pointer(i), :);

        % Take only few points of the trajectory
        pointer_points_used = pointer(i)+1:step:pointer(i+1)-1; % +1 since first position is used as initial pos for ee
        
        % Take the correct target position
        for t = 1:numel(targets_order)
            if targets_order(t) == cues(i)
                i_target = t;
            end
        end
        correct_target_position = target_positions_sorted(i_target, :);
        % Compute the correct angle which connect first position of ee and target
        correct_angle = calculate_angle(ee_start_position(1), ee_start_position(2), correct_target_position(1), correct_target_position(2));
        
        % Variable initialization
        err = [];
        % Iterate over points to use except the last point which is the target one
        for j = 1:numel(pointer_points_used)-1
            c_ee_x = ee_positions(pointer_points_used(j), 1);
            c_ee_y = ee_positions(pointer_points_used(j), 2);

            n_ee_x = ee_positions(pointer_points_used(j+1), 1);
            n_ee_y = ee_positions(pointer_points_used(j+1), 2);

            c_angle = calculate_angle(c_ee_x, c_ee_y, n_ee_x, n_ee_y);

            err = [err, abs(c_angle - correct_angle)];
        end
        mean_err_4_trial = [mean_err_4_trial, mean(err)];
    end
end


