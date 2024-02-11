function angle_rad = calculate_angle(x1, y1, x2, y2)
    delta_x = x2 - x1;
    delta_y = y2 - y1;

    angle_rad = atan2(delta_y, delta_x);
end
