% compute the Frechet distance of all ee position for each trial. we need
% the cf and pick events
function result = frechet_with_ideal_trj(ee, struct, event, ideal_trjs, cue, events_pick, event_cf, step)
    result.mean = zeros(length(struct.POS), 1);
    result.std = zeros(length(struct.POS), 1);
    j = 1;
    c_frecht = [];
    % iterate over all event
    for i= 1:length(event.TYP)
        if event.POS(i) > struct.POS(j) + struct.DUR(j)
            % upgrade frechet vector final
            result.mean(j) = mean(c_frecht);
            result.std(j) = std(c_frecht);
            j = j + 1;
            c_frecht = [];
        else
            % check the event is a cue
            if ismember(event.TYP(i), cue)
                idx_tag = event.TYP(i) - 5000 + 1;
                
                trj.x = [];
                trj.y = [];
            elseif ismember(event.TYP(i), event_cf)
                % in the trial cf
                trj.x = [trj.x; [ee.tr.x(event.POS(i):event.POS(i) + event.DUR(i)-1)]];
                trj.y = [trj.y; [ee.tr.y(event.POS(i):event.POS(i) + event.DUR(i)-1)]];
            elseif ismember(event.TYP(i), events_pick)
                % in the trial pick finish it, compute frechet
                trj.x = [trj.x; [ee.tr.x(event.POS(i):event.POS(i) + event.DUR(i)-1)]];
                trj.y = [trj.y; [ee.tr.y(event.POS(i):event.POS(i) + event.DUR(i)-1)]];

                % ideal trajectory
                i_trj.x = resample_borderCorrected(cell2mat(ideal_trjs.tr.x(idx_tag)), length(trj.x));
                i_trj.y = resample_borderCorrected(cell2mat(ideal_trjs.tr.y(idx_tag)), length(trj.y));
                % check the length!

                % frechet
                % use small trajectories in order to compute frechet faster
                l = length(trj.x);
                [cm, ~] = DiscreteFrechetDist([trj.x(1:step:l), trj.y(1:step:l)], [i_trj.x(1:step:l), i_trj.y(1:step:l)]);
                c_frecht = [c_frecht; cm];
            end
        end
    end
    result.mean(j) = mean(c_frecht);
    result.std(j) = std(c_frecht);

end

function tags_matrix = tags_as_matrix(tags)
    tags_matrix = nan(length(tags.tr.x), 3);

    tags_matrix(:,1) = tags.tr.x;
    tags_matrix(:,2) = tags.tr.y;
    tags_matrix(:,3) = tags.tr.z;

    tags_matrix = tags_matrix';
end
