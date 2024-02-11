% function which transform from a quaternion to a transformation matrix
function transformation_matrix = quaternionTranslation_to_transformationMatrix(rotation, translation)
    x = rotation(1);
    y = rotation(2);
    z = rotation(3);
    w = rotation(4);
    
    tx = translation(1);
    ty = translation(2);
    tz = translation(3);
    
    rotation_matrix = [
        1 - 2*y*y - 2*z*z, 2*x*y - 2*w*z, 2*x*z + 2*w*y;
        2*x*y + 2*w*z, 1 - 2*x*x - 2*z*z, 2*y*z - 2*w*x;
        2*x*z - 2*w*y, 2*y*z + 2*w*x, 1 - 2*x*x - 2*y*y
    ];

    transformation_matrix = eye(4);
    transformation_matrix(1:3, 1:3) = rotation_matrix;
    transformation_matrix(1:3, 4) = [tx; ty; tz];
end
