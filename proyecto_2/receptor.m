f_muestreo = 50000;
recObj = audiorecorder(f_muestreo,16,1);
seconds = 110;


disp('Start Recording.')
recordblocking(recObj, seconds);
disp('End of Recording.');


%play(recObj);

z = getaudiodata(recObj);
w=z;

t = 0:1/f_muestreo:seconds-1/f_muestreo;
plot(t,z)



