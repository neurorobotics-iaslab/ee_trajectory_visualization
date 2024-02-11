% extract infoo
function [event_TYP, event_POS, event_DUR, tr_x, tr_y, tr_z, rt_x, rt_y, rt_z, rt_w, base, to] = exctract_info(file)
    fprintf('file processing: %s\n', file);
    mat_file = load(file);

    event_TYP = mat_file.event.TYP;
    event_POS = mat_file.event.POS;
    event_DUR = mat_file.event.DUR;

    tr_x = mat_file.translation_x;
    tr_y = mat_file.translation_y;
    tr_z = mat_file.translation_z;

    rt_x = mat_file.rotation_x;
    rt_y = mat_file.rotation_y;
    rt_z = mat_file.rotation_z;
    rt_w = mat_file.rotation_w;

    base = mat_file.from;
    to = mat_file.to;
end