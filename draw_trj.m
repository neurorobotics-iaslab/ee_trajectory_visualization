function draw_trj(ee, struct, couple, str)
    figure('Name', ['trajectories couple: ', couple]);
    
    for i = 1:length(struct.POS)
        subplot(2,ceil((length(struct.POS)+1)/2),i)
        
        c_ee.x = ee.tr.x(struct.POS(i):struct.POS(i) + struct.DUR(i) -1);
        c_ee.y = ee.tr.y(struct.POS(i):struct.POS(i) + struct.DUR(i) -1);
        scatter(c_ee.x, c_ee.y);
        title([str, ': ', num2str(i), ', hit: ', num2str(struct.n(i))]);
        axis([-0.5, 0.5, 0.2, 0.9]);
    end

    subplot(2,ceil((length(struct.POS)+1)/2),length(struct.POS)+1)
    scatter(ee.tr.x, ee.tr.y);
    title(['Merge all ', str, 's'])
    axis([-0.5, 0.5, 0.2, 0.9]);

    sgtitle(['Only hit for couple: ', couple])
end