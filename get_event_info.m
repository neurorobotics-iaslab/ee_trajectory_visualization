% funtion to extract pos and dur from a defined event
function [c_event_POS, c_event_DUR] = get_event_info(event_TYP, event_POS, event_DUR, events)
    c_event_POS = zeros(0, 1);
    c_event_DUR = zeros(0, 1);
    for i = 1:length(event_TYP)
        if any(event_TYP(i) == events)
            c_event_POS = [c_event_POS; event_POS(i)];
            c_event_DUR = [c_event_DUR; event_DUR(i)];
        end
    end
end
