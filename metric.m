% tags mustbe already ordered from left to right. TAGS_ORDER is used to
% understand from cue where the robot must go

function [m_err_4_trial, m_abs_err_4_trial] = metric(ee_x, ee_y, ee_pos, ee_dur, tags_x, tags_y, TAGS_ORDER, cues, step)

    % Variable for all trials
    m_err_4_trial     = [];
    m_abs_err_4_trial = [];
    
    % Iterate over trials
    for i = 1:numel(ee_pos)

        % Take only few points of the trajectory
        c_ee_pos = ee_pos(i):step:ee_pos(i)+ee_dur(i)-1;

        % Take the correct tags position for this trial
        for t=1:numel(TAGS_ORDER)
            if TAGS_ORDER(t) == cues(i)
                c_tag_x = tags_x(t);
                c_tag_y = tags_y(t);
            end
        end

        % compute the metric
        err = [];
        for j = 1:numel(c_ee_pos)-1
            c_ee_x = ee_x(c_ee_pos(j));
            c_ee_y = ee_y(c_ee_pos(j));

            n_ee_x = ee_x(c_ee_pos(j+1));
            n_ee_y = ee_y(c_ee_pos(j+1));

            % calculate the correct angle to pick in the current point
            correct_angle = calculate_angle(c_ee_x, c_ee_y, c_tag_x, c_tag_y);

            % calculate the angle taken
            c_angle = calculate_angle(c_ee_x, c_ee_y, n_ee_x, n_ee_y);

            err = [err; correct_angle - c_angle];
        end

        % Save the mean error
        m_err_4_trial = [m_err_4_trial, mean(err)];
        m_abs_err_4_trial = [m_abs_err_4_trial, mean(abs(err))];
    end
    disp(['   mean 4 trial: ', num2str(round(m_err_4_trial, 4))])
    disp(['   mean abs 4 trial: ', num2str(round(m_abs_err_4_trial, 4))])
end

function angle_rad = calculate_angle(x1, y1, x2, y2)
    delta_x = x2 - x1;
    delta_y = y2 - y1;

    angle_rad = atan2(delta_y, delta_x);
end


