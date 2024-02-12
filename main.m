%% analisis of alessio's experiments
addpath('/home/paolo/ee_trajectory_visualization');

COLORS = {
    [255/255,       0,       0];     % red
    [255/255, 165/255,       0]; % orange
    [      0, 128/255,       0];     % green
    [      0,       0, 255/255];     % blue
    [128/255,       0, 128/255]  % purple
};

TAGS_ORDER = [0, 3, 4, 1, 2];

TAGS_ORDER = TAGS_ORDER + 5000;

ID_COLORS = containers.Map(TAGS_ORDER, COLORS);

directory = '/home/paolo/Scaricati/ur_data';
files = get_files(directory);

for i = 1:length(files)
    %% load and process all file
    file = files{i};
    [event_TYP, event_POS, event_DUR, tr_x, tr_y, tr_z, rt_x, rt_y, rt_z, rt_w, base, to] = exctract_info(file);
    tags_pos = get_tags_pos(tr_x(1:5), tr_y(1:5), tr_z(1:5)); % 5 x 3 (n_tags x coordinates) -> correct order for colors
    
    % get all cue
    cue = get_cue(event_TYP, [5000, 5001, 5002, 5003, 5004]);
    
    % get all cf and pick informations -> all the trajectory
    [cf_POS, cf_DUR] = get_event_info(event_TYP, event_POS, event_DUR, [781]);
    [pick_POS, pick_DUR] = get_event_info(event_TYP, event_POS, event_DUR, [1000, 1001, 1002, 1003, 1004]);

    % extract only position needed
    [trj_x, trj_y, trj_POS, trj_DUR] = get_trj(tr_x, tr_y, cf_POS, cf_DUR, pick_POS, pick_DUR);

    %% Plotting
    %fig = figure('Name', ['trajectory for file: ', file]);
    %draw(ID_COLORS, 0.02, 0.02, tags_pos, TAGS_ORDER, cue, trj_x, trj_y, trj_POS, trj_DUR);

    %% show jerk
    %vel_acc_jerk_4_trial(trj_x, trj_y, trj_POS, trj_DUR);

    %% compute metric
    metric(trj_x, trj_y, trj_POS, trj_DUR, tags_pos(:,1), tags_pos(:,2), TAGS_ORDER, cue, 2);
end