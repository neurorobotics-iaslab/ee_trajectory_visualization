function vel_acc_jerk_4_trial(x, y, pos, dur)
    for i = 1:numel(pos)
        positions_x = x(pos(i):pos(i)+dur(i)-1);
        velocity_x = gradient(positions_x);
        acceleration_x = gradient(velocity_x);
        jerk_x = gradient(acceleration_x);

        positions_y = y(pos(i):pos(i)+dur(i)-1);
        velocity_y = gradient(positions_y);
        acceleration_y = gradient(velocity_y);
        jerk_y = gradient(acceleration_y);

        fig = figure('Name', sprintf('analysis vel,acc,jerk for trial %d', i));
        subplot(2, 3, 1);
        plot(velocity_x);
        title('Vel_x');
        legend('Vel_x');
        
        subplot(2, 3, 2);
        plot(acceleration_x);
        title('Acc_x');
        legend('Acc_x');
        
        subplot(2, 3, 3);
        plot(jerk_x);
        title('Jerk_x');
        legend('Jerk_x');
        
        subplot(2, 3, 4);
        plot(velocity_y);
        title('Vel_y');
        legend('Vel_y');
        
        subplot(2, 3, 5);
        plot(acceleration_y);
        title('Acc_y');
        legend('Acc_y');
        
        subplot(2, 3, 6);
        plot(jerk_y);
        title('Jerk_y');
        legend('Jerk_y');
    end
end
