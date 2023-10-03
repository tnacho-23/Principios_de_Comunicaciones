import socket
import threading
import time

sock_clientes = []
cuentas_dict = {'111-1': {'Nombre': 'Mario', 'Password': 'alagrandelepusecuca', 'Dinero': 100, 'Actividad': [], 'Contactos': []},
                '222-2': {'Nombre': 'Jorge', 'Password': 'elcurioso', 'Dinero': 200, 'Actividad': ['Transferencia de 500 a 1','Transferencia de 500 a 2','Transferencia de 500 a 3','Transferencia de 500 a 4','Transferencia de 500 a 5','Transferencia de 500 a 6'], 'Contactos': ['333-3']},
                '333-3': {'Nombre': 'Marcia', 'Password': 'ana', 'Dinero': 100, 'Actividad': [], 'Contactos': []},
                '444-4': {'Nombre': 'Jorge', 'Password': 'nitales', 'Dinero': 9999999999999, 'Actividad': [], 'Contactos': []}}

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
        cuentas_dict[rut]['Actividad'].append('Has cambiado tu contraseña.')
        sock.send(f'Contraseña actualizada.\n'.encode())
        print(f'Cliente de RUT {rut} ha cambiado de contraseña.')
        sock.send(f'Redirigiendo al inicio...\n'.encode())
        time.sleep(2)
        pass
    else:
        sock.send(f'Contraseña Incorrecta.\n'.encode())
        change_pass(sock,rut)
        pass

def trans(sock,rut):
    with mutex:
        saldo = cuentas_dict[rut]['Dinero']
    sock.send(f'Tienes {saldo} disponible para transferir\n'.encode())
    sock.send(f'Ingresa el rut de la persona a quien quieres transferir'.encode())
    destinatario = sock.recv(1024).decode()
    if destinatario in cuentas_dict.keys():
        if destinatario in cuentas_dict[rut]['Contactos']:
            sock.send(f'Ingresa el monto a transferir'.encode())
            monto = sock.recv(1024).decode()
            if int(monto) > int(saldo):
                sock.send(f'No posees el dinero suficiente para realizar la operación.'.encode())
                pass
            else:
                sock.send(f'Por favor, confirma la operación ingresando tu contraseña:'.encode())
                input_pass = sock.recv(1024).decode()
                with mutex:
                    real_password = cuentas_dict[rut]['Password']
                if input_pass == real_password:
                    my_new_saldo = int(saldo) - int(monto)
                    cuentas_dict[rut]['Dinero'] = my_new_saldo


                    with mutex:
                        their_saldo = cuentas_dict[destinatario]['Dinero']
                    their_new_saldo = int(their_saldo) + int(monto)
                    cuentas_dict[destinatario]['Dinero'] = their_new_saldo
                    with mutex:
                        their_name= cuentas_dict[destinatario]['Nombre']
                    sock.send(f'Has hecho una transferencia de {monto} a {their_name}'.encode())
                    cuentas_dict[rut]['Actividad'].append(f'Has hecho una transferencia de {monto} a {their_name}')
                    pass
                else:
                    sock.send(f'Contraseña Incorrecta'.encode())
                    trans(sock,rut)
        else:
            sock.send(f'Es la primera vez que le transfieres a esta persona. \nPor esta vez, el monto a transferir no puede superar los 5 pesos.\n'.encode())
            sock.send(f'Ingresa el monto a transferir:'.encode())
            monto = sock.recv(1024).decode()
            if int(monto) > int(saldo):
                sock.send(f'No posees el dinero suficiente para realizar la operación.'.encode())
                pass
            if int(monto) > 5:
                sock.send(f'No puedes realizar esta operación'.encode())
            else:
                sock.send(f'Por favor, confirma la operación ingresando tu contraseña:'.encode())
                input_pass = sock.recv(1024).decode()
                with mutex:
                    real_password = cuentas_dict[rut]['Password']
                if input_pass == real_password:
                    cuentas_dict[rut]['Contactos'].append(destinatario)
                    my_new_saldo = int(saldo) - int(monto)
                    cuentas_dict[rut]['Dinero'] = my_new_saldo
                    with mutex:
                        their_saldo = cuentas_dict[destinatario]['Dinero']
                    their_new_saldo = int(their_saldo) + int(monto)
                    cuentas_dict[destinatario]['Dinero'] = their_new_saldo
                    with mutex:
                        their_name= cuentas_dict[destinatario]['Nombre']
                    sock.send(f'Has hecho una transferencia de {monto} a {their_name}'.encode())
                    cuentas_dict[rut]['Actividad'].append(f'Has hecho una transferencia de {monto} a {their_name}')
                    time.sleep(1)
                    pass
                else:
                    sock.send(f'Contraseña Incorrecta'.encode())
                    trans(sock,rut)
                    
        
        pass
    else: 
        sock.send(f'No existen registros de ese cliente en nuestra base de datos. \n ¿Qué quieres hacer? \n[0] Volver a intentar.\n[1] Ir al inicio.'.encode())
        try_again = sock.recv(1024).decode()
        if try_again == '0':
            trans(sock,rut)
        elif try_again == '1':
            pass
        

def balance(sock,rut):
    with mutex:
        saldo = cuentas_dict[rut]['Dinero']
    sock.send(f'Tu saldo es {saldo}'.encode())
    cuentas_dict[rut]['Actividad'].append('Has consultado tu saldo.')
    print(f'Cliente de RUT {rut} ha consultado su saldo.')
    time.sleep(1)
    pass


def history(sock,rut):
    sock.send(f'Tu actividad reciente en el portal es:\n'.encode())
    print(f'Cliente de RUT {rut} ha consultado su actividad reciente.')
    with mutex:
        historial = cuentas_dict[rut]['Actividad']
    if len(historial)<5:
        for j in historial:
            sock.send(f'{j}\n'.encode())
    else:
        for i in range(-1, -6, -1):
            this_historial = historial[i]
            sock.send(f'{this_historial}\n'.encode())

    

    time.sleep(1)
    pass

def contact(sock,rut):
    cuentas_dict[rut]['Actividad'].append('Has solicitado contacto con un ejecutivo.')

    time.sleep(1)
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
                        trans(sock,rut)
                    
                    elif data == "3":
                        balance(sock,rut)

                    elif data == "4":
                        history(sock,rut)

                    elif data == "5":
                        contact(sock,rut)

                    elif data == "6":
                        sock.send("Gracias por conectarte al portal del banco de Putaendo".encode())
                        time.sleep(1)
                        
                        # Se modifican las variables globales usando un mutex.
                        with mutex:
                            sock_clientes.remove(sock)
                        sock.close()
                        print(f'Cliente de RUT {rut} desconectado.')
                        return None

                    

                    else:
                        sock.send('Por favor indica un comando valido.'.encode())
            else: 
                sock.send('Contraseña Incorrecta'.encode())
                sock.send('Ingresa tu contraseña:'.encode())
                cliente(sock,rut)

                
                return None

        elif rut == '::exit':
            with mutex:
                sock_clientes.remove(sock)
            sock.close()
            return None

        else: 
            sock.send('No te cacho :/\nVuelve a intentarlo o ::exit para salir.'.encode())


# Funciones executive

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
                time.sleep(1)
                print(f'Admin {nombre} conectado.')
                sock.send(f'Clientes conectados:'.encode())
                time.sleep(1)
                for i in sock_clientes:
                    sock.send(f'{sock_clientes[i]}'.encode())
                    time.sleep(1)

                while True:
                    try:
                        data = sock.recv(1024).decode()
                    except:
                        break

                    if data == ":exit:":
                        sock.send("Adios!".encode())
                        
                        # Se modifican las variables globales usando un mutex.
                        with mutex:
                            sock_executives.remove(sock)
                        sock.close()
                        print(f'Admin {nombre} desconectado.')
                        return None
                    
                    elif data == ":status:":
                        pass

                    elif data == ":details:":
                        pass

                    elif data == ":history:":
                        pass

                    elif data == ":operations:":
                        pass

                    elif data == ":connect:":
                        pass 

                    elif data == ":disconnect:":
                        pass

                    else:
                        sock.send('Por favor indique un comando valido.'.encode())
                        time.sleep(1)

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
    conn.send("Escoje una opción \n".encode())
    conn.send("[0] Sign in \n[1] Sign up \n".encode())
    log = sock.recv(1024).decode()
    if log == '0':
        conn.send("Ingresa tu RUT:".encode())
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
            cuentas_dict[str(rut)] = {'Nombre': str(nombre), 'Password': str(contraseña), 'Dinero': 0, 'Actividad': [], 'Contactos': []}
    
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

    