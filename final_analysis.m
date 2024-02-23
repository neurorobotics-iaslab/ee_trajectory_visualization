clear all; close all;
couples = {'c7.g1', 'c9.c8', 'g2.d7'};

directory = '/home/paolo/Scaricati/upsampled';
files = get_files(directory);

% variables for general plot frechet
n_run_f = 16;
n_session_f = 5;
run_f.mean = nan(n_run_f, length(couples));
run_f.std = nan(n_run_f, length(couples));
session_f.mean = nan(n_session_f, length(couples));
session_f.std = nan(n_session_f, length(couples));

session_f_old.mean = nan(n_session_f, length(couples));
session_f_old.std = nan(n_session_f, length(couples));

% load ideal trajectories
ideal = load("paolo/ee_trajectory_visualization/ideal_trjectories.mat");
ideal = ideal.data;

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
    old_TYP = event.TYP;
    fprintf('   extracting hit\n');
    event.TYP = vector_hit(event, cues, 5000, 1000); % hit is a vector same length of event.TYP

    % extract for each run only hit trials
    event_req = [781, 1000, 1001, 1002, 1003, 1004]';
    fprintf('      for each run\n');
    [ee_run, run_hit] = extract_ee_hit(event, run, ee, event_req); % only hit ee.tr with pointer for each start/end run to the ee.tr vector

    % extract for each session only hit trials
    fprintf('      for each session\n');
    [ee_session, session_hit] = extract_ee_hit(event, session, ee, event_req);

    % draw trajectories
    %fprintf('   drawing trajectories')
    %draw_trj(ee_run, run_hit, strjoin(couples(i)), 'run');
    %draw_trj(ee_session, session_hit, strjoin(couples(i)), 'session');

    % definition for the heatmap plot
    nbins_x = 80;
    nbins_y = 80;
    saturation = 300;
    fprintf('   drawing heatmap for runs\n')
    %draw_topographic(ee_run, run_hit, strjoin(couples(i)), nbins_x, nbins_y, 'run', saturation);
    fprintf('   drawing heatmap for sessions\n')
    draw_topographic(ee_session, session_hit, strjoin(couples(i)), nbins_x, nbins_y, 'session', saturation);

    % frechet distance
    event.TYP = old_TYP;
    events_pick = [1000, 1001, 1002, 1003, 1004];
    event_cf = [781];
    step = 16;
    fprintf('   computing frechet for each run\n') 
    %result_run = frechet(ee, run, event, tags, cues, events_pick, event_cf, step);
    %result_run = frechet_with_ideal_trj(ee, run, event, ideal, cues, events_pick, event_cf, step);
    fprintf('   computing frechet for each session\n')
    %result_session_old = frechet(ee, session, event, tags, cues, events_pick, event_cf, step);
    result_session = frechet_with_ideal_trj(ee, session, event, ideal, cues, events_pick, event_cf, step);
    
    % save frechet for such couple
    %run_f.mean(1:length(result_run.mean(:)),i) = result_run.mean(:);
    %run_f.std(1:length(result_run.std(:)),i)  = result_run.std(:);
    session_f.mean(:,i) = result_session.mean(1:n_session_f);
    session_f.std(:,i)  = result_session.std(1:n_session_f);

    %session_f_old.mean(:,i) = result_session.mean(1:n_session_f);
    %session_f_old.std(:,i)  = result_session.std(1:n_session_f);
end

%% plot frechet
fprintf('   plotting frechet\n')
%plot_frechet(run_f, 'Frechet distance for each run', couples, 'Runs');
plot_frechet(session_f, 'Frechet distance for each session', couples, 'Sessions');
%plot_frechet(session_f_old, 'Frechet distance for each session OLD', couples, 'Sessions');


