# socket server demo

import socket
import os
import threading

# for testing: cd c:\Users\alyssa\Documents\CIS_D022A\Student

def cd(new_path):
    try:
        os.chdir(new_path)
        return 'success'
    except Exception as e:
        return f"fail: {str(e)}"

def ls(curr_dir):
    try:
        listing = "\n".join(os.listdir(curr_dir))
        return listing
    except Exception as e:
        return f"fail: {str(e)}"

def lsr(curr_dir):
    try:
        results = []
        for (path, dirList, fileList) in os.walk(curr_dir):
            for d in dirList:
                results.append(os.path.join(path, d))
            for f in fileList:
                results.append(os.path.join(path, f))
        long_listing = "\n".join(results)
        return long_listing
    except Exception as e:
        return f"fail: {str(e)}"
            

def client_handler(conn, num_connections, time):
    while True:
        try:
            current_directory = os.getcwd()
            conn.settimeout(time) # to fix: doesnt timeout the first time
            fromClient = conn.recv(1024).decode('utf-8')
            

            try:
                fromClient, path  = fromClient.split(' ')
            except ValueError:
                pass

            
            if fromClient == 'q':
                mesg = 'q'
                print(f'Client #{num_connections} has quit')
                num_connections -=1
                break
    
            elif fromClient == 'cd':
                print(f'New path: {path}')
                current_directory = path
                mesg = cd(path)
            elif fromClient == 'ls':
                print(f'Listing of {os.getcwd()}')
                mesg = ls(current_directory)
            elif fromClient == 'lsr':
                print(f'Long listing of {os.getcwd()}')
                mesg = lsr(current_directory)
            else:
                mesg = 'incorrect input, please try again'

            print("Received:", fromClient)          
            conn.send(mesg.encode('utf-8'))

        except socket.timeout:
            mesg = f'Connection {num_connections} timed out, closing'
            print(f'Connection {num_connections} timed out, closing')
            conn.send(mesg.encode('utf-8'))
            num_connections -= 1
            conn.close()
            break
        

        
def main():
    HOST = "localhost"      
    PORT = 5484
    while True:
        try:
            max_clients =  int(input("Enter the maximum number of clients: "))
            if max_clients > 0 and max_clients <= 5:
                break
            else:
                print('The number of clients needs to be more than 0 and less than 5. Try again')
        except ValueError:
            print('Value needs to be an integer. Please try again')

    while True:
        try:
            timer_time =  int(input("Enter the time you wish the server to be operational: "))
            if timer_time > 3 and timer_time <= 120:
                break
            else:
                print('The time needs to be between 3 and 120. Please try again')
        except ValueError:
            print('Value needs to be an integer. Please try again')



    with socket.socket() as s :
        s.bind((HOST, PORT))
        s.listen(max_clients)
        print("Server hostname:", HOST, "port:", PORT)
        
        threads = []
        num_connections = 0

        try:
            while True:

                #print(f'numconections: {num_connections}')
                #print(f'max {max_clients}')
                num_connections +=1
                (conn, addr) = s.accept()  
                if num_connections > max_clients:
                    print('Max clients reached')
                    conn.close()
                    break
                print(f'Accepted connection from {addr}')
               
                client_thread = threading.Thread(target=client_handler, args=(conn, num_connections, timer_time))
                client_thread.start()
                threads.append(client_thread)
                                
        except socket.timeout:
            print("Server timed out, shutting down.")

        except Exception as e:
            print(f"[!] error: {e}")
                   
        for t in threads:
            t.join()
        


if __name__ == '__main__':
    main()


