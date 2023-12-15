% Leer la imagen
%imagen = imread('img1.png'); % Reemplaza con el nombre de tu imagen
imagen = imagenRGB;
% Obtener los canales de color
canalRojo = imagen(:,:,1);
canalVerde = imagen(:,:,2);
canalAzul = imagen(:,:,3);

% Calcular los histogramas de cada canal
histogramaRojo = imhist(canalRojo);
histogramaVerde = imhist(canalVerde);
histogramaAzul = imhist(canalAzul);

% Mostrar los histogramas
figure;

subplot(3, 1, 1);
bar(histogramaRojo, 'r');
title('Histograma del Canal Rojo');

subplot(3, 1, 2);
bar(histogramaVerde, 'g');
title('Histograma del Canal Verde');

subplot(3, 1, 3);
bar(histogramaAzul, 'b');
title('Histograma del Canal Azul');
