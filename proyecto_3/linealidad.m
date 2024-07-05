%#ok<*TNMLP>
close all
clear
clc

amplitudes = 0.1:0.1:1;
output_amplitudes = zeros(size(amplitudes));
fs = 44100;
duration = 1;
L = length(amplitudes);
figure

for i = 1:L
    t = 0:1/fs:duration;
    test_signal = amplitudes(i) * sin(2*pi*1000*t);
    
    player = audioplayer(test_signal, fs);
    recorder = audiorecorder(fs, 16, 1);
    
    record(recorder);
    playblocking(player);
    stop(recorder);
    
    output_signal = getaudiodata(recorder);
    subplot(L,1,i)
    plot(output_signal)
    
    output_amplitudes(i) = sqrt(mean(output_signal.^2));
end

figure;
plot(amplitudes, output_amplitudes, '-o', 'LineWidth', 2);
xlabel('Input Amplitude');
ylabel('Output Amplitude');
title('Channel Linearity Test');
grid on;
