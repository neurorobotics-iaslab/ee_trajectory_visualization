clear all; close all;
couples = {'c7.g1', 'c9.c8', 'g2.d7'};

directory = '/home/paolo/Scaricati/upsampled';
files = get_files(directory);

% variables for general plot frechet
n_tags = 5;
storage = 3;
ideal_trj.tr.x = cell(n_tags,storage);
ideal_trj.tr.y = cell(n_tags,storage);
ideal_trj.DUR = nan(n_tags,storage);

for i= 1:length(couples) 
    % Take only files with such couple
    fprintf('Couple: %s\n', strjoin(couples(i)));
    couple_files = file_with_substr(files, strjoin(couples(i)));

    % Load all file of such couple and concatenate them. Tags are ordered
    % by name, so first is tag0, then tag1, and so on and already on base
    % frame
    n_tags = 5;
    [event, ee, tags, run, session] = load_and_concatenate(couple_files, n_tags);

    % extract translation ee only of the hit trials
    cues = [5000, 5001, 5002, 5003, 5004];
    fprintf('   extracting hit');
    event.TYP = vector_hit(event, cues, 5000, 1000); % hit is a vector same length of event.TYP
    fprintf('... done')

    % extract for each run only hit trials
    ideal_trj = extract(ee, event, 5000, 5000, ideal_trj);
    ideal_trj = extract(ee, event, 5001, 5000, ideal_trj);
    ideal_trj = extract(ee, event, 5002, 5000, ideal_trj);
    ideal_trj = extract(ee, event, 5003, 5000, ideal_trj);
    ideal_trj = extract(ee, event, 5004, 5000, ideal_trj);
end

%% Plotting to understand which trajectory is the best for each trial
%{%
for i =1:size(ideal_trj.tr.x,1)
    figure;
    hold on;
    for j = 1:size(ideal_trj.tr.y, 2)
        plot(cell2mat(ideal_trj.tr.x(i,j)), cell2mat(ideal_trj.tr.y(i,j)));
    end
    hold off;
end
%}

%% save
% pick only the first trajectories
data.tr.x = ideal_trj.tr.x(:,1);
data.tr.y = ideal_trj.tr.y(:,1);
data.DUR = ideal_trj.DUR(:,1);

save("paolo/ee_trajectory_visualization/ideal_trjectories.mat", 'data');



