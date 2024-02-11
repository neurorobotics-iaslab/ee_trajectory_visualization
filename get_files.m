% extract names
function filenames = get_files(directory)
    files = dir(directory);
    filenames = {};
    for i = 1:length(files)
        filename = files(i).name;
        [~, ~, ext] = fileparts(filename);
        if strcmp(ext, '.mat')
            filepath = fullfile(directory, filename);
            filenames = [filenames, filepath];
        end
    end
end



