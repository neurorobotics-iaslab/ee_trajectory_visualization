function draw(ID_COLORS, width, height, tags_pos, TAGS_ORDER, cue, trj_x, trj_y, trj_POS, trj_DUR)
    % Draw base
    scatter(0, 0, 'k', 'filled', 'diamond', 'DisplayName', 'base');
    hold on;

    % Draw target
    draw_tags(width, height, tags_pos, TAGS_ORDER, ID_COLORS);
    
    % Draw trajectory
    draw_trj(cue, trj_x, trj_y, trj_POS, trj_DUR, ID_COLORS);
    
    hold off;
    drawnow;
end

% draw tags in the image
function draw_tags(width, height, tags_pos, TAGS_ORDER, ID_COLORS)
    for i = 1:length(tags_pos)
        tag = tags_pos(i,:);
        rectangle('Position',[tag(1)-width/2.0, tag(2)-height/2.0, width, height], ...
            'EdgeColor', ID_COLORS(TAGS_ORDER(i)), 'FaceColor', 'none');
        str = num2str(TAGS_ORDER(i));
        text(tag(1), tag(2) + height, ['tag_', str(end)], 'HorizontalAlignment', 'center', 'VerticalAlignment', 'bottom');
    end
end


% draw trajectories in the image
function draw_trj(cue, trj_x, trj_y, trj_pos, trj_dur, ID_COLORS)
    labels = {'base'};
    for idx_t = 1:numel(cue)
        c_cue = cue(idx_t);
        c_pos = trj_pos(idx_t);
        c_dur = trj_dur(idx_t);

        c_tr_x = trj_x(c_pos:c_pos+c_dur-1);
        c_tr_y = trj_y(c_pos:c_pos+c_dur-1);
        c_color = repmat(ID_COLORS(c_cue), c_dur, 1);
        scatter(c_tr_x, c_tr_y, 5, c_color, 'filled')
        labels = [labels, ['trial ', num2str(idx_t)]];
    end
    
    legend(labels, 'Location', 'northwest');
end