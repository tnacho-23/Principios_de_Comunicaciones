import socket

# Se configura el servidor para que corra localmente y en el puerto 8889.
HOST = '127.0.0.1'
PORT = 8889

# Se crea el socket y se instancia en las variables anteriores, aceptando hasta 3 clientes.
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(3)

# Se buscan clientes que quieran conectarse.
while True:

    # Se acepta la conexion de un cliente
    conn, addr = s.accept()
    print(f"Cliente conectado en address {addr}")
    
    # Se ejecuta lo siguiente en un loop hasta que el cliente se desconecte.
    while True:
    
        # Se reciben los datos que ha enviado el cliente.
        data = conn.recv(1024)
        
        # Si el cliente se desconecta a la mala, al leer los datos se recibira un string vacio.
        if not data:
            
            # Salir de este loop y permitir la conexion de otro cliente.
            break

        # El cliente tambien puede desconectarse bien
        elif data == b'::exit\n':
            conn.send("Chau".encode())
            break
        
        # Responder con los mismos datos que fueron recibidos.
        conn.send(data)
    
    # Terminar la conexion con el cliente.
    conn.close()
    print(f'Cliente en {addr} desconectado.')