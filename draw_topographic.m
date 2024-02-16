function draw_topographic(ee, struct, couple, nbins_x, nbins_y, str)
    figure('Name', ['heatmap couple: ', couple]);

    edges_x = linspace(min(ee.tr.x), max(ee.tr.x), nbins_x);
    edges_y = linspace(min(ee.tr.y), max(ee.tr.y), nbins_y);

    for i = 1:length(struct.POS)
        subplot(2,ceil((length(struct.POS)+1)/2),i)
        
        c_ee.x = ee.tr.x(struct.POS(i):struct.POS(i) + struct.DUR(i) -1);
        c_ee.y = ee.tr.y(struct.POS(i):struct.POS(i) + struct.DUR(i) -1);
        h = histcounts2(c_ee.x, c_ee.y, edges_x, edges_y);
        h(h>100) = 100; % saturation
        imagesc(flipud(h'));
        title([str, ' ', num2str(i), ', hit: ', num2str(struct.n(i))])
    end

    subplot(2,ceil((length(struct.POS)+1)/2),length(struct.POS)+1);
    h = histcounts2(ee.tr.x, ee.tr.y, edges_x, edges_y);
    h(h>100) = 100;
    imagesc(flipud(h'));
    axis([0, 80, 0, 80]);
    title(['Merge of overall ', str])
end