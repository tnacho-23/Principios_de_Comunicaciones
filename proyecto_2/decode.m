
red_Channel = [];
green_Channel = [];
blue_Channel = [];
str_Channel = [];

m_pixel = 8000;
fs = 50000;
T = 1/fs;
step = 12;

s = z;

f1 = 6000;
f2 = 7000;
f3 = 8000;
header_time = 1; % segundos
ts = 0:T:header_time-T;

% Se define la senal de sincronizacion

s_sincr1 = cos(2*pi*f1*ts);
s_sincr2 = cos(2*pi*f2*ts);
s_sincr3 = cos(2*pi*f3*ts);
s_sincr = [s_sincr1, s_sincr2, s_sincr3];

% Se realiza una autocorrelacion en los primeros 30 segundos para encontrar la senal de sincronizacion
% en el audio recibido

header_test=header_time*30;

signal = s(1: header_test*fs);
[acorr, lag] = xcorr(signal, s_sincr);
[~,I] = max(abs(acorr));
lagDiff = I-(length(signal)-length(ts)*3);


% Proceso de demodulación

for i=1:400
y = s(m_pixel*(i-1)+lagDiff:m_pixel*i+lagDiff); 
[i_red, i_blue, i_green]=frec_colores(y, fs, step);

red_Channel=[red_Channel,i_red];
green_Channel=[green_Channel,i_green];
blue_Channel=[blue_Channel,i_blue];
end 

% Se reconstruye la imagen
m_red = uint8(reshape(red_Channel,20,20));
m_green = uint8(reshape(green_Channel,20,20));
m_blue = uint8(reshape(blue_Channel,20,20));


imagenRGB = cat(3, m_red, m_green, m_blue);

subplot(1,4,1);
imshow(cat(3, m_red, zeros(20,20,'uint8'), zeros(20,20,'uint8')));
title('Red');
subplot(1,4,2);
imshow(cat(3, zeros(20,20,'uint8'), m_green, zeros(20,20,'uint8')));
title('Green');
subplot(1,4,3);
imshow(cat(3, zeros(20,20,'uint8'), zeros(20,20,'uint8'), m_blue));
title('Blue');
subplot(1,4,4);

imagen_decodificada = cat(3, m_red, m_green, m_blue);
imshow(imagen_decodificada);
title('Imagen decodificada');

%---------------------Transmisión de texto-------------------------------
for i=401:450
    s_prima= s(m_pixel*(i-1)+lagDiff:m_pixel*i+lagDiff);
    y=s_prima;
    str_Channel=[str_Channel,frec_str(y, fs, step)];
end
disp(str_Channel)

%-----------------funciones auxiliares----------------------------------

function [str] = frec_str(y, fs, step)
espectro_str = 2000;

simbolos='abcdefghijklmnñopqrstuvwxyz ABCDEFGIJKLMNÑOPQRSTUVWXYZ0123456789';
n = length(simbolos);
posicion_simbolos = 1:n ;

%se crean filtros para cada banda de frecuencias
n=5; %orden de los filtros
norma = fs/2;
Wd_r=(espectro_str-25)/norma;
Wu_r=(espectro_str+65*step+25)/norma;
[b,a]=butter(n,[Wd_r,Wu_r],'bandpass');
str_filt = filter(b,a,y);

y_frecuencias_str1 = abs(fft(str_filt,fs));
y_frecuencias1 = y_frecuencias_str1(1:(length(y_frecuencias_str1))/2);
y_frecuencias_str=y_frecuencias1(espectro_str-25:(espectro_str+65*step)+25);
[maxValue_str, maxIndex_str] = max(y_frecuencias_str);


if maxIndex_str<25
    f_str=1;
    
elseif maxIndex_str <= length(y_frecuencias_str)-25
    f_str = round((maxIndex_str-25)/step)+1;
    
else
    f_str=63+1;
end
%disp(simbolos(f_str));
str=simbolos(f_str);

end


function [i_red, i_blue, i_green] = frec_colores(y, fs, step)
    
    symbols=255;
    init_red=2000;
    order_filter=10;
    sred_filt = filter_butterworth(y, fs, order_filter, init_red, init_red+symbols*step);

    y_frecuencias_r1=abs(fft(sred_filt,fs));
    y_frecuencias_r=y_frecuencias_r1(1:length(y_frecuencias_r1)/2);
    y_frecuencias_red=y_frecuencias_r(init_red-25:init_red+symbols*step+25);

    init_green = init_red+symbols*step+50;
    sgreen_filt = filter_butterworth(y, fs, order_filter, init_green, init_green+symbols*step);

    y_frecuencias_g1 = abs(fft(sgreen_filt,fs));
    y_frecuencias_g = y_frecuencias_g1(1:length(y_frecuencias_g1)/2);
    y_frecuencias_green=y_frecuencias_g(init_green-25:init_green+symbols*step+25);
   
    init_blue = init_green+symbols*step+50;
    sblue_filt = filter_butterworth(y, fs, order_filter, init_blue, init_blue+symbols*step);

    y_frecuencias_b1 = abs(fft(sblue_filt,fs));
    y_frecuencias_b = y_frecuencias_b1(1:length(y_frecuencias_b1)/2);
    y_frecuencias_blue=y_frecuencias_b(init_blue-25:init_blue+symbols*step+25);
    
    [~, maxIndex_red] = max(y_frecuencias_red);
    [~, maxIndex_green] = max(y_frecuencias_green);
    [~, maxIndex_blue] = max(y_frecuencias_blue);

    %disp(init_blue+symbols*step+25)

    if maxIndex_red<25
        i_red=0;
        
    elseif maxIndex_red <= length(y_frecuencias_red)-25
        i_red = round((maxIndex_red-25)/step);
        
    else
        i_red=255;
    end
    
    
    if maxIndex_green<25
        i_green=0;
        
    elseif maxIndex_green <= length(y_frecuencias_green)-25
        i_green = round((maxIndex_green-25)/step);
        
    else
        i_green=255;
    end
    
    
    if maxIndex_blue<25
        i_blue=0;
        
    elseif maxIndex_blue <= length(y_frecuencias_blue)-25
        i_blue = round((maxIndex_blue-25)/step);
        
    else
        i_blue=255;
        
    end    
end

function [filtered_signal] = filter_butterworth(signal, fs, order, f_low, f_high)
    [b, a] = butter(order, [f_low, f_high] * 2 / fs, 'bandpass');
    filtered_signal = filter(b,a,signal);
end