# socket client demo

import socket

HOST = '127.0.0.1'
PORT = 5484

with socket.socket() as s :
    try:
        s.connect((HOST, PORT))
        print("Client connect to:", HOST, "port:", PORT)

        print("Available commands:")
        print("ls - list current directory")
        print("lsr - list subdirectories recursively")
        print("cd - change directory, usage: cd <dir_name>")
        print("q  - quit")
        
        mesg = input("Enter message to send or q to quit: ")
        s.send(mesg.encode('utf-8'))
        while mesg != 'q':
            try:
                fromServer = s.recv(1024).decode('utf-8')
                print(f'Received from server:\n{fromServer}')
                mesg = input("Enter message to send or q to quit: ")
                s.send(mesg.encode('utf-8'))
            except ConnectionAbortedError as e:
                print('The maximum amount of clients was reached, try again later')
                break
        print('Connection closed.')

    except ConnectionRefusedError as e:
        print('Max number of clients reached. Please try again later')
        #print(e)



