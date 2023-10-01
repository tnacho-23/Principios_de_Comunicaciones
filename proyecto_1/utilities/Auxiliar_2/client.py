
import socket
import sys

# Se asume que el servidor esta corriendo localmente en el puerto 8889.
HOST = '127.0.0.1'
PORT = 8889

# Se crea el socket y se conecta al servidor.
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
print("Conectado al servidor")

# Se revisa la entrada estandar y se envia lo que ingrese le usuarie.
for line in sys.stdin:
    s.send(line.encode())
    
    # Se reciben datos del servidor y se imprimen.
    res = s.recv(1024).decode()
    print(f"[SERVER]: {res}")

    if line == "::exit\n":
        break
    
# Se cierra el socket.
s.close()
print('Te has desconectado.')