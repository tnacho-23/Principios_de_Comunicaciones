% Lectura y procesamiento de imagenes

image = imread('img1.png');

% Separar en matrices RGB
[redChannel, greenChannel, blueChannel] = imsplit(image);


%Se crean vectores unidimensionales de las matrices RGB de cada color
v_redChannel=reshape(redChannel,400,1);
v_greenChannel=reshape(greenChannel,400,1);
v_blueChannel=reshape(blueChannel,400,1);

%Se reconstruyen los canales de color independientes
emptyChannel = zeros(20, 20, 'uint8');
just_redColor = cat(3, redChannel, emptyChannel, emptyChannel);
just_greenColor = cat(3, emptyChannel, greenChannel, emptyChannel);
just_blueColor = cat(3, emptyChannel, emptyChannel, blueChannel);
all_imageColor = cat(3, redChannel, greenChannel, blueChannel);
subplot(1,4,4);
imshow(all_imageColor);
subplot(1,4,3);
imshow(just_blueColor);
subplot(1,4,2);
imshow(just_greenColor);
subplot(1,4,1);
imshow(just_redColor);
%close all;

% Generacion de senales para cada canal de color
step = 12;
f_muestreo = 50000;
m_pixel = 8000;
time_header = 1;
symbols = 255;
f1 = 6000;
f2 = 7000;
f3 = 8000;

s_red = [];
s_green = [];
s_blue = [];


tiempo_envio = m_pixel/f_muestreo; 
t1 = 0:1/f_muestreo:tiempo_envio-1/f_muestreo;
frec = 0:step:255*step;

init_red = 2000; 
for i=1:400
    y_red = cos(2*pi*(frec(v_redChannel(i)+1)+init_red)*t1);
    s_red = [s_red, y_red]; 
end

init_green = init_red+symbols*step+50; %comienzo del espectro de color verde
for i=1:400
    y_green = cos(2*pi*(frec(v_greenChannel(i)+1)+init_green)*t1);
    s_green = [s_green, y_green]; 
end

init_blue = init_green+symbols*step+50; %comienzo del espectro de color azul
for i=1:400
    y_blue = cos(2*pi*(frec(v_blueChannel(i)+1)+init_blue)*t1);
    s_blue = [s_blue, y_blue];  
end

s1 = s_red + s_green + s_blue; 


simbolos=65;
step_str = step;
frec_str = 0:1/simbolos:1-1/simbolos;
frec_str = frec_str*step_str;


% Codificacion y transmision de texto
simbolos = 'abcdefghijklmnñopqrstuvwxyz ABCDEFGIJKLMNÑOPQRSTUVWXYZ0123456789';
n = length(simbolos);
posicion_simbolos = 0:n-1;
vector_simbolos = zeros(1, n);

mensaje = 'Principios de Comunicaciones primavera 2023 EL4112';
vector_mensaje = zeros(1, length(mensaje));

for i = 1:n
    vector_simbolos(i) = simbolos(i);
end

for i = 1:length(mensaje)
    vector_mensaje(i) = mensaje(i);
end

largo_mensaje = length(mensaje);
t_str = 0:1/f_muestreo:m_pixel/f_muestreo-1/f_muestreo;
s_str = [];
vector_ASCII = [];
espectro_str = 2000;

for i = 1:largo_mensaje
    posicion = find(vector_simbolos == vector_mensaje(i));
    vector_ASCII = [vector_ASCII, posicion];
    y = cos(2*pi*(step*(posicion-1)+espectro_str)*t_str);
    s_str = [s_str, y];
end
s1 = [s1, s_str];


% Generacion de senales de sincronizacion y transmision
T = 1/f_muestreo;
t_s = 0:T:time_header-T;
s_sincr = [];
s_sincr1 = cos(2*pi*f1*t_s);
s_sincr2 = cos(2*pi*f2*t_s);
s_sincr3 = cos(2*pi*f3*t_s);
s_sincr = [s_sincr, s_sincr1, s_sincr2, s_sincr3];
s1 = [s_sincr, s1];

soundsc(s1,f_muestreo);

