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

solicitudes = [] # Aquí se guardan los ruts de quienes quieren acceder a un ejecutivo
ejecutivo_cliente = [] # Aquí se guardan los ejecutivos que no esten hablando con algun cliente

mutex = threading.Lock()

#Funciones comunes

def contact(sock_ejecutivo, sock_cliente, rut_cliente):

    nombre_cliente = cuentas_dict[rut_cliente]["Nombre"] 
    conectado = True

    while conectado:
        
        res_ejecutive = sock_ejecutivo.recv(1024).decode()
        
        if res_ejecutive == ":history:":
            sock_ejecutivo.send(f'El historial del cliente {nombre_cliente} es:'.encode())
            time.sleep(1)
           
            historial = cuentas_dict[rut_cliente]['Actividad']
            
            for j in historial:
                sock_ejecutivo.send(f'{j}\n'.encode())
                time.sleep(1)

        elif res_ejecutive == ":operations:":
            sock_cliente.send(f'Su historial es:'.encode())
            time.sleep(1)
            
            historial = cuentas_dict[rut_cliente]["Actividad"]
            
            for j in historial:
                sock_cliente.send(f'{j}\n'.encode())
                time.sleep(1)

        elif res_ejecutive == ":disconnect:":
            conectado = False
            for conexion in ejecutivo_cliente:
                if rut_cliente in conexion:
                    ejecutivo_cliente.remove(conexion)
        
        else:
            # res_client = sock_cliente.recv(1024).decode()
            # print(res_client)
            # sock_ejecutivo.send(res_client.encode())
            sock_cliente.send(f'[Ejecutivo]:{res_ejecutive}'.encode())
            time.sleep(1)
    pass


#Funciones Cliente
def change_pass_cli(sock,rut):
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
        change_pass_cli(sock,rut)
        pass

def trans_cli(sock,rut):
    #with mutex:
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
                sock.send(f'Por favor, vuelve a ingresar tu contraseña'.encode())
                cliente(sock,rut)
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
                    trans_cli(sock,rut)
        else:
            sock.send(f'Es la primera vez que le transfieres a esta persona. \nPor esta vez, el monto a transferir no puede superar los 5 pesos.\n'.encode())
            sock.send(f'Ingresa el monto a transferir:'.encode())
            monto = sock.recv(1024).decode()
            if int(monto) > int(saldo):
                sock.send(f'No posees el dinero suficiente para realizar la operación.'.encode())
                sock.send(f'Por favor, vuelve a ingresar tu contraseña'.encode())
                cliente(sock,rut)
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
                    trans_cli(sock,rut)
                    
        
        pass
    else: 
        sock.send(f'No existen registros de ese cliente en nuestra base de datos. \n ¿Qué quieres hacer? \n[0] Volver a intentar.\n[1] Ir al inicio.'.encode())
        try_again = sock.recv(1024).decode()
        if try_again == '0':
            trans_cli(sock,rut)
        elif try_again == '1':
            pass
        

def balance_cli(sock,rut):
    with mutex:
        saldo = cuentas_dict[rut]['Dinero']
    sock.send(f'Tu saldo es {saldo}'.encode())
    cuentas_dict[rut]['Actividad'].append('Has consultado tu saldo.')
    print(f'Cliente de RUT {rut} ha consultado su saldo.')
    time.sleep(1)
    pass


def history_cli(sock,rut):
    sock.send(f'Tu actividad reciente en el portal es:\n'.encode())
    print(f'Cliente de RUT {rut} ha consultado su actividad reciente.')
    
    #with mutex:
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
                        change_pass_cli(sock,rut)

                    elif data == "2":
                        trans_cli(sock,rut)
                    
                    elif data == "3":
                        balance_cli(sock,rut)

                    elif data == "4":
                        history_cli(sock,rut)

                    elif data == "5":
                        cuentas_dict[rut]['Actividad'].append('Has solicitado contacto con un ejecutivo.')
                        solicitudes.append(rut)
                        if len(sock_executives) == 0:
                            sock.send(f'En estos momentos no hay ejecutivos que puedan ayudarle'.encode())
                            time.sleep(1) 
                        else:
                            while rut in solicitudes:
                                t_espera = int((len(solicitudes) / len(sock_executives)) * 1)
                                sock.send(f'Será redirigid@ con nuestros ejecutivos, el tiempo de espera es de {t_espera} minutos'.encode())
                                time.sleep(5)
                            
                            
                            for conexion in ejecutivo_cliente:
                                if rut == conexion[1]:
                                    rut_ejecutivo = conexion[0]
                                    parejita = conexion
                                    for ejecutivo in sock_executives:
                                        if rut_ejecutivo == ejecutivo[0]:
                                            conn_ejecutivo = ejecutivo[1]
                                            while parejita in ejecutivo_cliente:
                                                res_client = sock.recv(1024).decode()
                                                conn_ejecutivo.send(f'[Cliente]:{res_client}'.encode())
                                            pass
                    elif data == "6":
                        sock.send("Gracias por conectarte al portal del banco de Putaendo".encode())
                        time.sleep(1)
                        
                        # Se modifican las variables globales usando un mutex.
                        with mutex:
                            for cliente in sock_clientes:
                                if cliente[0] == rut:
                                    sock_clientes.remove(cliente)
                        sock.close()
                        print(f'Cliente de RUT {rut} desconectado.')
                        return None

                    

                    else:
                        sock.send('Por favor indica un comando valido.'.encode())
            else: 
                sock.send('Contraseña Incorrecta'.encode())
                login(sock)

                
                return None

        elif rut == '::exit':
            with mutex:
                for cliente in sock_clientes:
                    if cliente[0] == rut:
                        sock_clientes.remove(cliente)
            sock.close()
            return None

        else: 
            sock.send('No te cacho :/\nVuelve a intentarlo o ::exit para salir.'.encode())


# Funciones executive

def status(sock, rut):
    sock.send(f'Clientes conectados:'.encode())
    time.sleep(1)

    sock.send(f'Hay {len(sock_clientes)} conectados'.encode())
    time.sleep(1)

    for i in range(len(sock_clientes)):

        rut = (sock_clientes[i])[0]
        port = ((sock_clientes[i])[1]).getpeername()

        sock.send(f'Cliente: {rut} {cuentas_dict[rut]["Nombre"]} conectado'.encode())
        time.sleep(1)
        # sock.send(f'En el puerto: {((sock_clientes[i])[1]).getpeername()}'.encode())
        # time.sleep(1)

    if len(solicitudes) == 0:
        sock.send(f'No hay clientes esperando a un ejecutivo.'.encode())
        time.sleep(1)

    else: 
        for i in range(len(solicitudes)):
            rut = solicitudes[i]
            sock.send(f'Cliente {cuentas_dict[rut]["Nombre"]} esperando a un ejecutivo.'.encode())
            time.sleep(1)

    time.sleep(1)
    pass

def details(sock, rut): 
    sock.send(f'Aqui tienes los clientes conectados y su ultima acción:'.encode())
    time.sleep(1)
    
    for i in range(len(sock_clientes)):

        rut = (sock_clientes[i])[0]
        actividad = cuentas_dict[rut]["Actividad"]
        nombre = cuentas_dict[rut]["Nombre"]
        
        if len(actividad) == 0:
            sock.send(f'Cliente {rut} {nombre}, no a iniciado actividad'.encode())  
            time.sleep(1)

        else:  
            sock.send(f'Cliente {rut} {nombre}, su ultima acción fue: {actividad[-1]}'.encode())
        time.sleep(1)
        
def history(sock, rut):
    sock.send(f'El historial del cliente es:'.encode())
    time.sleep(1)

def executive(sock, rut):
    global sock_executives, executive_acces, sock_clientes, cuentas_dict
    while True:
        if rut in executive_acces.keys():
            
            inputed_password = sock.recv(1024).decode()
            with mutex:
                real_password = executive_acces[rut]['Password']
            if inputed_password == real_password:
                with mutex:
                    nombre = executive_acces[rut]['Nombre']
                sock.send(f'Login correcto\nBienvenid@ {nombre} '.encode())
                time.sleep(1)
                print(f'Admin {nombre} conectado.')
                
                while True:
                    try:
                        data = sock.recv(1024).decode()
                    except:
                        break

                    if data == ":exit:":
                        sock.send("Adios!".encode())
                        
                        # Se modifican las variables globales usando un mutex.
                        with mutex:
                            for ejecutivo in sock_executives:
                                if ejecutivo[0] == rut:
                                    sock_executives.remove(ejecutivo)
                        sock.close()
                        print(f'Admin {nombre} desconectado.')
                        return None

                    elif data == ":status:":
                            status(sock, rut)

                    elif data == ":details:":
                            details(sock, rut)
                    
                    elif data == ":connect:":
                        if len(solicitudes) !=0: 
                            rut_cliente = solicitudes[0]
                            solicitudes.pop(0)
                            ejecutivo_cliente.append((rut, rut_cliente))
                            for cliente in sock_clientes:
                                if cliente[0] == rut_cliente:
                                    cliente_conn = cliente[1]
                                    nombre_cliente = cuentas_dict[rut_cliente]["Nombre"] 
                                    cliente_conn.send(f'Usted se a conectado con el ejecutiv@ {executive_acces[rut]["Nombre"]}'.encode())
                                    contact(sock, cliente_conn, rut_cliente)
                                    
                        else:
                            sock.send('No hay clientes esperando.'.encode())
                            time.sleep(1)
                            

                    else:
                        sock.send('Por favor indique un comando valido.'.encode())
                        time.sleep(1)

            else: 
                sock.send('Contraseña Incorrecta'.encode())
                sock.send('Ingrese su rut:'.encode())
                executive(sock,rut)


                
                return None

        elif rut == '::exit':
            with mutex:
                for ejecutivo in sock_executives:
                    if ejecutivo[0] == rut:
                        sock_executives.remove(ejecutivo)
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
            sock_executives.append([rut, conn])                     # Sabemos quien y donde esta conectado
            sock.send(f'Ingresa tu contraseña:'.encode())
            return executive(sock, rut)
        elif rut in cuentas_dict.keys():
            sock_clientes.append([rut, conn])                        # Sabemos quien y donde esta conectado
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
            conn.send("Cuenta creada \n".encode())
            time.sleep(1)
            return login(sock)
    
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
        s.close()
        break

    