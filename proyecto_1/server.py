import socket
import threading
import time

sock_clientes = []
cuentas_dict = {'111-1': {'Nombre': 'Mario', 'Password': 'alagrandelepusecuca', 'Dinero': 100, 'Actividad': []},
                '222-2': {'Nombre': 'Jorge', 'Password': 'elcurioso', 'Dinero': 200, 'Actividad': []},
                '333-3': {'Nombre': 'Marcia', 'Password': 'ana', 'Dinero': 100, 'Actividad': []},
                '444-4': {'Nombre': 'Jorge', 'Password': 'nitales', 'Dinero': 9999999999999, 'Actividad': []}}

sock_executives = []
executive_acces = {'555-5': {'Nombre': 'InHackeable', 'Password': '1234'}}

mutex = threading.Lock()

#Funciones Cliente

def change_pass(sock,rut):
    sock.send(f'Ingresa tu contraseña actual:'.encode())
    inputed_password = sock.recv(1024).decode()
    with mutex:
        real_password = cuentas_dict[rut]['Password']
    if inputed_password == real_password:
        sock.send(f'Ingresa tu nueva contraseña:'.encode())
        new_password = sock.recv(1024).decode()
        cuentas_dict[rut]['Password'] = new_password
        sock.send(f'Contraseña actualizada.\n'.encode())
        print(f'Cliente de RUT {rut} ha cambiado de contraseña.')
        sock.send(f'Redirigiendo al inicio...\n'.encode())
        time.sleep(2)
        pass
    else:
        sock.send(f'Contraseña Incorrecta.\n'.encode())
        change_pass(sock,rut)

def trans(sock,rut):
    pass

def balance(sock,rut):
    pass

def history(sock,rut):
    pass

def contact(sock,rut):
    pass

def cliente(sock, rut):
    global sock_clientes, cuentas_dict
    
    while True:
        if rut in cuentas_dict.keys():
            
            inputed_password = sock.recv(1024).decode()
            with mutex:
                real_password = cuentas_dict[rut]['Password']
            if inputed_password == real_password:
                with mutex:
                    nombre = cuentas_dict[rut]['Nombre']
                sock.send(f'Login correcto\nBienvenid@ {nombre}\n'.encode())
                print(f'Cliente de RUT {rut} conectado.')

                while True:
                    sock.send(f'¿Cómo te podemos ayudar?\n'.encode())
                    sock.send(f'[1] Cambio de contraseña. \n[2] Realizar transferencia. \n[3] Consulta de saldo. \n[4] Historial de operaciones \n[5] Contacto con un ejecutivo. \n[6] Salir.'.encode())
                    try:
                        data = sock.recv(1024).decode()
                    except:
                        break
    
                    if data == "1":
                        change_pass(sock,rut)

                    elif data == "2":
                        trans(rut,sock)
                    
                    elif data == "3":
                        balance(rut,sock)

                    elif data == "4":
                        history(rut,sock)

                    elif data == "5":
                        contact(rut,sock)

                    elif data == "6":
                        sock.send("Gracias por conectarse al portal del banco de Putaendo".encode())
                        
                        # Se modifican las variables globales usando un mutex.
                        with mutex:
                            sock_clientes.remove(sock)
                        sock.close()
                        print(f'Cliente de RUT {rut} desconectado.')
                        return None

                    

                    else:
                        sock.send('Por favor indique un comando valido.'.encode())
            else: 
                sock.send('Contraseña Incorrecta'.encode())
                sock.send('Ingrese su contraseña:'.encode())
                cliente(sock,rut)


                
                return None

        elif rut == '::exit':
            with mutex:
                sock_clientes.remove(sock)
            sock.close()
            return None

        else: 
            sock.send('No te cacho :/\nVuelve a intentarlo o ::exit para salir.'.encode())

def executive(sock, rut):
    global sock_executives, executive_acces, sock_clientes, cuentas_dict
    while True:
        if rut in executive_acces.keys():
            sock.send(f'Ingresa tu contraseña:'.encode())
            inputed_password = sock.recv(1024).decode()
            with mutex:
                real_password = executive_acces[rut]['Password']
            if inputed_password == real_password:
                with mutex:
                    nombre = executive_acces[rut]['Nombre']
                sock.send(f'Login correcto\nBienvenid@ {nombre} '.encode())
                print(f'Admin {nombre} conectado.')

                while True:
                    try:
                        data = sock.recv(1024).decode()
                    except:
                        break

                    if data == "::exit":
                        sock.send("Adios!".encode())
                        
                        # Se modifican las variables globales usando un mutex.
                        with mutex:
                            sock_executives.remove(sock)
                        sock.close()
                        print(f'Admin {nombre} desconectado.')
                        return None

                    else:
                        sock.send('Por favor indique un comando valido.'.encode())
            else: 
                sock.send('Contraseña Incorrecta'.encode())
                sock.send('Ingrese su rut:'.encode())
                cliente(sock)


                
                return None

        elif rut == '::exit':
            with mutex:
                sock_clientes.remove(sock)
            sock.close()
            return None

        else: 
            sock.send('No te cacho :/\nVuelve a intentarlo o ::exit para salir.'.encode())
    
def login(sock):
    global sock_executives, executive_acces, sock_clientes, cuentas_dict
    conn.send("Escoja una opción \n".encode())
    conn.send("[0] Sign in \n[1] Sign up \n".encode())
    log = sock.recv(1024).decode()
    if log == '0':
        conn.send("Ingrese su RUT".encode())
        rut = sock.recv(1024).decode()
        if rut in executive_acces.keys():
            sock_executives.append(conn)
            sock.send(f'Ingresa tu contraseña:'.encode())
            return executive(sock, rut)
        elif rut in cuentas_dict.keys():
            sock_clientes.append(conn)
            sock.send(f'Ingresa tu contraseña:'.encode())
            return cliente(sock, rut)
        else:
            conn.send("No se encuentra registrado \n".encode())
            return login(sock)
    elif log == '1': #BONUS
        conn.send("Ingrese su RUT \n".encode())
        rut = sock.recv(1024).decode()
        if rut in cuentas_dict.keys():
            conn.send("Este RUT ya tiene una cuenta asociada \n".encode())
            return login(sock)
        else:
            #'444-4': {'Nombre': 'Jorge', 'Password': 'nitales', 'Dinero': 100, 'Actividad': []}}
            conn.send("Ingrese su nombre \n".encode())
            nombre = sock.recv(1024).decode()
            conn.send("Ingrese una contraseña \n".encode())
            contraseña = sock.recv(1024).decode()
            cuentas_dict[str(rut)] = {'Nombre': str(nombre), 'Password': str(contraseña), 'Dinero': 0, 'Actividad': []}
    
    else: 
        conn.send("Por favor ingresar una opción valida \n".encode())
        return login(sock)
        

# Se configura el servidor para que corra localmente y en el puerto 8889.
HOST = '127.0.0.1'
PORT = 8889

# Se crea el socket y se instancia en las variables anteriores.
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen()

# Se buscan clientes que quieran conectarse.
while True:
    try: 
        # Se acepta la conexion de un cliente
        conn, addr = s.accept()

        # Se manda el mensaje de bienvenida
        conn.send("Bienvenid@ al Banco de Putaendo: \n".encode())

        # Se inicia el thread del cliente
        client_thread = threading.Thread(target=login, args=(conn,))
        client_thread.start()
    
    except KeyboardInterrupt:
        break

    