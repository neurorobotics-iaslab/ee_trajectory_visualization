% get a vector with only the cue values
function cue = get_cue(event_TYP, cue_events)
    cue = zeros(0, 1);
    for i = 1:length(event_TYP)
        if any(event_TYP(i) == cue_events)
            cue = [cue; event_TYP(i)];
        end
    end
end
