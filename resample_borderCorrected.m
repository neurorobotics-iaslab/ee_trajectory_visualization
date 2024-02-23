% data un vettore colonna di dati (eg. x e y), n_finish quanti punti in totale
function resampled = resample_borderCorrected(data, n_finish)

    n_points = size(data,1);

    t_data = [repmat(data(1),n_points,1); data; repmat(data(end),n_points,1)];

    t_res = resample(t_data, n_finish*3, n_points*3);
    resampled = t_res(n_finish+1:2*n_finish);
end