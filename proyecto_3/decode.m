%clear
received_signal = w;

% Parámetros de la señal
window_duration = 0.01;  % Duración de cada ventana de tiempo en segundos
pulse_width = 0.5 * window_duration;  % Ancho del pulso en segundos
fs = 50000;
T = 1/fs;

% Frecuencias de sincronización
f1 = 6000;
f2 = 7000;
f3 = 8000;



% Duración de la señal de sincronización
time_header = 1;  % Duración en segundos
t_s = 0:T:time_header-T;

% Crear señales de sincronización esperadas
s_sincr1 = cos(2*pi*f1*t_s);
s_sincr2 = cos(2*pi*f2*t_s);
s_sincr3 = cos(2*pi*f3*t_s);
s_sincr = [s_sincr1, s_sincr2, s_sincr3];


% Detectar la señal de sincronización en los primeros 5 segundos de la
% grabación
header_test = time_header*5;

sinc_signal = received_signal(1:header_test*fs);


% Correlacionar para encontrar la sincronización
corr = xcorr(sinc_signal, s_sincr);
[~, idx] = max(corr);
desfase = (idx - (length(s_sincr)-length(t_s)));

% Extraer la señal PPM
ppm_signal = received_signal(desfase:end);


% Función para decodificar la señal PPM
samples_per_window = round(fs * window_duration);
num_bits = floor(length(ppm_signal) / samples_per_window);  % Asegurarse de que num_bits sea un entero
decoded_bits = zeros(1, num_bits);

for i = 1:num_bits
    start_index = + (i - 1) * samples_per_window + 1;
    % disp(start_index);
    pulse_sample = ppm_signal(start_index:start_index + samples_per_window - 1);
    [~, pulse_position] = max(pulse_sample);
    decoded_bits(i) = 1 * (pulse_position > samples_per_window / 2);
end

decoded_bits = decoded_bits(1:68);
% Mostrar la secuencia de bits decodificada
disp('Secuencia de bits decodificada:');
disp(decoded_bits);

% Graficar la señal recibida
figure;
subplot(3, 1, 1);
plot(received_signal);
title('Señal de audio recibida');
ylabel('Amplitud');

% Graficar la señal PPM
subplot(3, 1, 3);
plot(ppm_signal);
title('Señal PPM');
ylabel('Amplitud');

original_bit_sequence = [1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1,  1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1,  1, 0, 0];

% Calcular el número de errores
num_errors = sum(original_bit_sequence ~= decoded_bits);

% Calcular el porcentaje de error
total_bits = length(original_bit_sequence);
percentage_error = (num_errors / total_bits) * 100;

% Mostrar el resultado
fprintf('El porcentaje de error es: %.2f%%\n', percentage_error);
