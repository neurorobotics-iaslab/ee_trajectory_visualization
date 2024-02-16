% struct contains all mean value for a run of a couple. n_run x n_couple
function plot_frechet(struct, str, couples)
    n_bars  = size(struct.mean, 1);
    n_goups = size(struct.mean, 2);
    x_tick = size(struct.mean, 2) + 1;
    x = 1:(size(struct.mean, 1) * (size(struct.mean,2) + 1));
    figure('Name', str);

    for i = 1:n_goups
        x_b = x(i:x_tick:x(end))';
        bar(x_b, struct.mean(:,i), 'BarWidth', 0.25);
        hold on;
        b = gca;
    end
    legend(couples);

    for i = 1:n_goups
        x_b = x(i:x_tick:x(end))';
        errorbar(x_b, struct.mean(:,i), struct.std(:,i), '.k', 'HandleVisibility','off');
    end
    b.XTick = 2:(size(struct.mean,2) + 1):(n_bars*(size(struct.mean,2) + 1));
    b.XTickLabel = 1:(size(struct.mean, 1) + 1);
    
    
    hold off;
end