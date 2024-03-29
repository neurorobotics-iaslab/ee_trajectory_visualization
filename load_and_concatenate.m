% load all file from a list and concatene them. Is important the the files
% are .mat with a specific structure (reported in the README.md)
function [c_event, ee, tags, run, session] = load_and_concatenate(files, n_tags)
    % build up a new structure with all the data
    c_event.TYP = [];
    c_event.POS = [];
    c_event.DUR = [];

    % edn effector values
    ee.tr.x = [];
    ee.tr.y = [];
    ee.tr.z = [];
    ee.rt.x = [];
    ee.rt.y = [];
    ee.rt.z = [];
    ee.rt.w = [];

    % tags values
    c_tags.tr.x = zeros(n_tags,1);
    c_tags.tr.y = zeros(n_tags,1);
    c_tags.tr.z = zeros(n_tags,1);
    c_tags.rt.x = zeros(n_tags,1);
    c_tags.rt.y = zeros(n_tags,1);
    c_tags.rt.z = zeros(n_tags,1);
    c_tags.rt.w = zeros(n_tags,1);

    % value for each run
    run.POS = [];
    run.DUR = [];

    % value for each session
    session.POS = [];
    session.DUR = [];
    session.day = [];
    pattern = '\d{8}';
    c_session_dur = 0;

    for idx_f = 1:length(files)
        % load file
        c_file = strjoin(files(idx_f));
        fprintf('   loading: %s\n', c_file);
        load(c_file);

        % save the session
        c_session = regexp(c_file, pattern, 'match');
        c_session  = str2num(c_session{1});
        if ~(any(ismember(session.day, c_session)))
            session.day = [session.day; c_session];
            if isempty(session.POS)
                session.POS = [session.POS; c_session_dur + 1];
            else 
                session.POS = [session.POS; session.POS(end) + c_session_dur];
            end
            
            if c_session_dur ~=0
                session.DUR = [session.DUR; c_session_dur];
            end
            c_session_dur = 0;
        end

        % save the event
        if isempty(c_event.POS)
            tags_name = to(1:n_tags,:);
            tags_number = str2double(tags_name(:,5:end));
            [~,idx] = sort(tags_number);
            c_tags.tr.x(1:n_tags) = translation_x(idx);
            c_tags.tr.y(1:n_tags) = translation_y(idx);
            c_tags.tr.z(1:n_tags) = translation_z(idx);
            c_tags.rt.x(1:n_tags) = rotation_x(idx);
            c_tags.rt.y(1:n_tags) = rotation_y(idx);
            c_tags.rt.z(1:n_tags) = rotation_z(idx);
            c_tags.rt.w(1:n_tags) = rotation_w(idx);

        end
        c_event.TYP = [c_event.TYP; event.TYP];
        c_event.DUR = [c_event.DUR; event.DUR];
        c_event.POS = [c_event.POS; event.POS + (length(ee.tr.x))];

        run.POS = [run.POS; length(ee.tr.x)+1];

        ee.tr.x = [ee.tr.x; translation_x];
        ee.tr.y = [ee.tr.y; translation_y];
        ee.tr.z = [ee.tr.z; translation_z];
        ee.rt.x = [ee.rt.x; rotation_x];
        ee.rt.y = [ee.rt.y; rotation_y];
        ee.rt.z = [ee.rt.z; rotation_z];
        ee.rt.w = [ee.rt.w; rotation_w];
        run.DUR = [run.DUR; length(translation_x)];
        c_session_dur = c_session_dur + run.DUR(end);
    end

    % add the last session DUR
    session.DUR = [session.DUR; c_session_dur];

    tags = tags_pos_transformation(c_tags);


end