% return a vector with ones and zeros accordin to hit or miss
function v = vector_hit(event, cues, offset_cue, offset_tag)
    v = [];
    i = 1;
    while i < length(event.TYP)
        if ismember(event.TYP(i), cues) && (event.TYP(i)-offset_cue == event.TYP(i+2) - offset_tag)
            v = [v; event.TYP(i:i+3)];
            i = i + 4;
        else
            v = [v; 0];
            i = i + 1;
        end
    end
    v = [v; 0]; % for the last 9999
end