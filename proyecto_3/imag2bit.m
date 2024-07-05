% Leer la imagen
img = imread('C:\Users\palfe\Downloads\test_tic.jpg'); % Asegúrate de que 'imagen.png' es la imagen que quieres usar

% Convertir la imagen a escala de grises si no lo es
if size(img, 3) == 3
    img = rgb2gray(img);
end

% Convertir la imagen a blanco y negro
bw_img = imbinarize(img);

% Visualizar la imagen original y la imagen en blanco y negro
figure;
subplot(1, 2, 1);
imshow(img);
title('Imagen original en escala de grises');

subplot(1, 2, 2);
imshow(bw_img);
title('Imagen convertida a blanco y negro');

% Convertir la imagen a un arreglo de bits
bits = bw_img(:); % Convertir la imagen a un vector de bits

% Mostrar la secuencia de bits en la consola
disp('Secuencia de bits:');
disp(bits');

% Guardar el arreglo de bits en un archivo
save('bits_image.mat', 'bits', 'bw_img'); % Guardar los bits y las dimensiones originales de la imagen