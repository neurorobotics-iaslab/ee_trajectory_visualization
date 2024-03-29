function vel_acc_jerk_4_trial(x, y, pos, dur)
    mean_vel_x = [];
    mean_vel_y = [];
    mean_acc_x = [];
    mean_acc_y = [];
    mean_jrk_x = [];
    mean_jrk_y = [];
    for i = 1:numel(pos)
        % calculate everythings for x
        positions_x = x(pos(i):pos(i)+dur(i)-1);
        velocity_x = gradient(positions_x);
        acceleration_x = gradient(velocity_x);
        jerk_x = gradient(acceleration_x);

        % compute the mean and save it for x
        mean_vel_x = [mean_vel_x; mean(velocity_x)];
        mean_acc_x = [mean_acc_x; mean(acceleration_x)];
        mean_jrk_x = [mean_jrk_x; mean(jerk_x)];

        % calculate everythings for y
        positions_y = y(pos(i):pos(i)+dur(i)-1);
        velocity_y = gradient(positions_y);
        acceleration_y = gradient(velocity_y);
        jerk_y = gradient(acceleration_y);

        % compute the mean and save it for y
        mean_vel_y = [mean_vel_y; mean(velocity_y)];
        mean_acc_y = [mean_acc_y; mean(acceleration_y)];
        mean_jrk_y = [mean_jrk_y; mean(jerk_y)];

    end

    fprintf('   mean vel_x = %.5f \n', mean(mean_vel_x))
    fprintf('   mean acc_x = %.5f \n', mean(mean_acc_x))
    fprintf('   mean jrk_x = %.5f \n', mean(mean_jrk_x))
    fprintf('   mean vel_y = %.5f \n', mean(mean_vel_y))
    fprintf('   mean acc_y = %.5f \n', mean(mean_acc_y))
    fprintf('   mean jrk_y = %.5f \n', mean(mean_jrk_y))
end
