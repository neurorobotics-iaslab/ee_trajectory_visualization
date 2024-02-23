function draw_topographic(ee, struct, couple, nbins_x, nbins_y, str, saturation)
    figure('Name', ['heatmap couple: ', couple]);

    edges_x = linspace(min(ee.tr.x), max(ee.tr.x), nbins_x);
    edges_y = linspace(min(ee.tr.y), max(ee.tr.y), nbins_y);

    for i = 1:length(struct.POS)
        subplot(1,length(struct.POS),i)
        
        c_ee.x = ee.tr.x(struct.POS(i):struct.POS(i) + struct.DUR(i) -1);
        c_ee.y = ee.tr.y(struct.POS(i):struct.POS(i) + struct.DUR(i) -1);
        h = histcounts2(c_ee.x, c_ee.y, edges_x, edges_y);
        h(h>saturation) = saturation; % saturation
        imagesc(flipud(h'));
        title([str, ' ', num2str(i)])
        axis([0, nbins_x, 0, nbins_y]);
    end
    sgtitle(['couple: ', couple]);
end