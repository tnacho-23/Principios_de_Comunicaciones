import socket
import threading

sock_clientes = []
cuentas_dict = {'1234-5': {'Nombre': 'Camilo', 'Dinero': 1, 'Usuarios_asociados': ['Giovanni']},
                '6789-0': {'Nombre': 'Giovanni', 'Dinero': 2, 'Usuarios_asociados': ['Camilo']}}
mutex = threading.Lock()

def cliente(sock):
    global sock_clientes, cuentas_dict
    while True:
        rut = sock.recv(1024).decode()
        if rut in cuentas_dict.keys():
            sock.send('Wena malditooo!'.encode())
            print(f'Cliente de RUT {rut} conectado.')

            while True:
                try:
                    data = sock.recv(1024).decode()
                except:
                    break

                if data == "::exit":
                    sock.send("Adios!".encode())
                    
                    # Se modifican las variables globales usando un mutex.
                    with mutex:
                        sock_clientes.remove(sock)
                    sock.close()
                    print(f'Cliente de RUT {rut} desconectado.')
                    break

                elif data == "::dinero":
                    # Se lee el dinero en la cuenta de una persona con mutex
                    with mutex:
                        dinero = cuentas_dict[rut]['Dinero']
                    sock.send(f"[SERVER] Tu saldo es de {dinero} pesos.".encode())

                else:
                    sock.send('Por favor indique un comando valido.'.encode())
            return None

        elif rut == '::exit':
            with mutex:
                sock_clientes.remove(sock)
            sock.close()
            return None

        else: 
            sock.send('No te cacho :/\nVuelve a intentarlo o ::exit para salir.'.encode())

    

# Se configura el servidor para que corra localmente y en el puerto 8889.
HOST = '127.0.0.1'
PORT = 8889

# Se crea el socket y se instancia en las variables anteriores.
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen()

# Se buscan clientes que quieran conectarse.
while True:

    # Se acepta la conexion de un cliente
    conn, addr = s.accept()
    sock_clientes.append(conn)

    # Se manda el mensaje de bienvenida
    conn.send("Bienvenid@ al Banco Zembe!\nIngrese su RUT a continuacion: ".encode())

    # Se inicia el thread del cliente
    client_thread = threading.Thread(target=cliente, args=(conn,))
    client_thread.start()