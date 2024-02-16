% ee contains all x, y of the event effector
% event: all event with POS, DUR and TYP (TYP is only for hit trial)
% struct: pos and dur for the division of the struct_hi
% events_req: all event we want to analyses
% ee_hit: only position of x, y of the end effector for hit and event
% required
% struct_hit: pointer to ee_hit according to the type and due of such time
function [ee_hit, struct_hit] = extract_ee_hit(event, struct, ee, events_req)
    struct_hit.POS = [1];
    struct_hit.DUR = [];
    struct_hit.n   = [0]; 
    ee_hit.tr.x = [];
    ee_hit.tr.y = [];
    ee_hit.tr.z = [];
    j = 1;
    c_dur = 0;
    for i=1:length(event.TYP)
        
        if event.POS(i) < struct.POS(j) + struct.DUR(j) 
            if ismember(event.TYP(i), events_req)
                c_dur = c_dur + event.DUR(i);
                ee_hit.tr.x = [ee_hit.tr.x; ee.tr.x(event.POS(i):event.POS(i)+event.DUR(i)-1)];
                ee_hit.tr.y = [ee_hit.tr.y; ee.tr.y(event.POS(i):event.POS(i)+event.DUR(i)-1)];
                if event.TYP(i) == 781
                    struct_hit.n(j) = struct_hit.n(j) + 1;
                end
            end
        else
            struct_hit.POS = [struct_hit.POS; length(ee_hit.tr.x)+1];
            struct_hit.DUR = [struct_hit.DUR; c_dur];
            struct_hit.n = [struct_hit.n; 0];
            c_dur = 0;
            j = j + 1;
        end
    end
    
    % add last DUR
    struct_hit.DUR = [struct_hit.DUR; c_dur];
end

%{ 
        % OLD
        if ismember(event.TYP(i), events_req)
            % event required so save position of ee starting from that
            % point, but according to the struct
            if event.POS(i) < struct.POS(j) + struct.DUR(j)
                c_dur = c_dur + event.DUR(i);
                if event.TYP(i) == 781
                    struct_hit.n(j) = struct_hit.n(j) + 1;
                end
            else
                struct_hit.POS = [struct_hit.POS; length(ee_hit.tr.x)+1];
                struct_hit.DUR = [struct_hit.DUR; c_dur];
                struct_hit.n = [struct_hit.n; 1];
                c_dur = event.DUR(i);
                j = j + 1;
            end
            ee_hit.tr.x = [ee_hit.tr.x; ee.tr.x(event.POS(i):event.POS(i)+event.DUR(i)-1)];
            ee_hit.tr.y = [ee_hit.tr.y; ee.tr.y(event.POS(i):event.POS(i)+event.DUR(i)-1)];
        end
        %}