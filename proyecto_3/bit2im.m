% Cargar el arreglo de bits y las dimensiones originales de la imagen
load('bits_image.mat', 'bits', 'bw_img');

% Reconstruir la imagen a partir del arreglo de bits
reconstructed_img = reshape(bits, size(bw_img));

% Visualizar la imagen reconstruida
figure;
imshow(reconstructed_img);
title('Imagen reconstruida');

% Mostrar la secuencia de bits reconstruida en la consola
disp('Secuencia de bits reconstruida:');
disp(bits');
