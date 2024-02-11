% given cf and pick, obtain the full trajectory
function [x,y,pos, dur] = get_trj(tr_x, tr_y, cf_POS, cf_DUR, pick_POS, pick_DUR)
    x = [];
    y = [];
    pos = [];
    dur = [];
    for i = 1:length(cf_POS)
        pos = [pos; length(x)+1];
        x = [x; tr_x(cf_POS(i):cf_POS(i)+cf_DUR(i)-1); tr_x(pick_POS(i):pick_POS(i)+pick_DUR(i)-1)];
        y = [y; tr_y(cf_POS(i):cf_POS(i)+cf_DUR(i)-1); tr_y(pick_POS(i):pick_POS(i)+pick_DUR(i)-1)];
        dur = [dur; length(x)-pos(i)+1];
    end
end
