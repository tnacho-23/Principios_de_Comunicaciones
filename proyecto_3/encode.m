% Parámetros
clear
fs = 50000;  % Frecuencia de muestreo para audio
window_duration = 0.01;  % Duración de cada ventana de tiempo en segundos
pulse_width = 0.5 * window_duration;  % Ancho del pulso en segundos

% Secuencia de bits (ejemplo)
bit_sequence = [1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1,  1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1,  1, 0, 0];
%disp(length(bit_sequence));
disp('Secuencia de bits transmitida:');
disp(bit_sequence);

% Generar la señal PPM
total_time = window_duration * length(bit_sequence);
time = linspace(0, total_time, fs * total_time);
ppm_signal = zeros(size(time));
for i = 1:length(bit_sequence)
    % Calcula el tiempo de inicio del pulso basado en el valor del bit actual
    pulse_start_time = (i - 1) * window_duration;
    if bit_sequence(i) == 1
        pulse_start_time = pulse_start_time + 0.5 * window_duration;
    end
    % Enciende el pulso en el tiempo calculado
    pulse_indices = (time >= pulse_start_time) & (time <= pulse_start_time + pulse_width);
    ppm_signal(pulse_indices) = 1;
end

% Visualización
figure;
subplot(2,1,1);
plot(time, ppm_signal, 'LineWidth', 1.5);  % Ajuste del grosor de línea para mejor visualización
title('Señal PPM');
xlabel('Tiempo (s)');
ylabel('Amplitud');
grid on;

% Frecuencia de la portadora
f_carrier = 1000;  % Frecuencia de la portadora en Hz

% Generar la señal portadora
carrier_signal = sin(2 * pi * f_carrier * time);

% Modulación de amplitud de la señal PPM con la portadora
information_signal = ppm_signal .* carrier_signal;

% Generacion de senales de sincronizacion
f1 = 6000;
f2 = 7000;
f3 = 8000;
time_header = 1;

T = 1/fs;
t_s = 0:T:time_header-T;
s_sincr = [];
s_sincr1 = cos(2*pi*f1*t_s);
s_sincr2 = cos(2*pi*f2*t_s);
s_sincr3 = cos(2*pi*f3*t_s);
sinc_signal = [s_sincr, s_sincr1, s_sincr2, s_sincr3];


audio_signal = [sinc_signal, information_signal];

% Genera la señal de audio
audio_duration = length(audio_signal)/fs; % Duración de la señal de audio en segundos

% Visualizar la señal de audio generada
time_audio = (0:length(audio_signal)-1) / fs; % Tiempo en segundos
subplot(2,1,2);
plot(time_audio, audio_signal);
title('Audio Signal with Synchronization');
xlabel('Time (seconds)');
ylabel('Amplitude');

% Play the audio signal
sound(audio_signal, fs);
filename = 'ppm_signal.wav';  % Nombre del archivo de audio
audiowrite(filename, audio_signal, fs);

disp('Señal de audio modulada y reproducida.');
