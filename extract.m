function ideal = extract(ee, event, cue, offset_cue, ideal)
    for i = 1:length(event.TYP)
        if event.TYP(i) == cue
            cf_POS = event.POS(i+1);
            pick_POS = event.POS(i+2);
            cf_DUR = event.DUR(i+1);
            pick_DUR = event.DUR(i+2);

            % fill all nan
            if any(isnan(ideal.DUR(cue-offset_cue+1,:)))
                idx_nan = find(isnan(ideal.DUR(cue-offset_cue+1,:)), 1);
                tmp_x = ee.tr.x(cf_POS:cf_POS+cf_DUR-1);
                tmp_x = [tmp_x; ee.tr.x(pick_POS:pick_POS+pick_DUR-1)];
                tmp_y = ee.tr.y(cf_POS:cf_POS+cf_DUR-1);
                tmp_y = [tmp_y; ee.tr.y(pick_POS:pick_POS+pick_DUR-1)];
                ideal.tr.x(cue-offset_cue+1,idx_nan) = {tmp_x};
                ideal.tr.y(cue-offset_cue+1,idx_nan) = {tmp_y};
                ideal.DUR(cue-offset_cue+1,idx_nan) = cf_DUR + pick_DUR;
                
            else
                % find the max value and compare it
                [max_dur, idx_max] = max(ideal.DUR(cue-offset_cue+1,:),[], 'all');
                if max_dur > (cf_DUR + pick_DUR)
                    tmp_x = ee.tr.x(cf_POS:cf_POS+cf_DUR-1);
                    tmp_x = [tmp_x; ee.tr.x(pick_POS:pick_POS+pick_DUR-1)];
                    tmp_y = ee.tr.y(cf_POS:cf_POS+cf_DUR-1);
                    tmp_y = [tmp_y; ee.tr.y(pick_POS:pick_POS+pick_DUR-1)];

                    ideal.tr.x(cue-offset_cue+1,idx_max) = {tmp_x};
                    ideal.tr.y(cue-offset_cue+1,idx_max) = {tmp_y};
                    ideal.DUR(cue-offset_cue+1,idx_max) = cf_DUR + pick_DUR;
                    
                end
            end
        end
    end
    ideal = order(ideal, cue-offset_cue+1);
end

function n_struct = order(struct, col)
    n_struct.tr.x = struct.tr.x;
    n_struct.tr.y = struct.tr.y;
    n_struct.DUR = struct.DUR;
    [~, idx] = sort(struct.DUR(col,:));
    for i = 1:length(struct.DUR(col,:))
        n_struct.tr.x(col,i) = struct.tr.x(col, idx(i));
        n_struct.tr.y(col,i) = struct.tr.y(col, idx(i));
        n_struct.DUR(col,i) = struct.DUR(col, idx(i));
    end
    
end