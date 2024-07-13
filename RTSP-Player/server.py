import socket
import time
import random

def start_server():
    # Create a socket object
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

    # Get local machine name
    #host = socket.gethostname() 
    host = '10.26.10.103' 

    # Set a port number
    port = 9999

    # Bind to the port
    serversocket.bind((host, port))

    print("Waiting for connection.")
    # Set up as a server, specify the maximum number of queued connections
    serversocket.listen(5)

    while True:
        # Establish a connection with the client
        clientsocket, addr = serversocket.accept()   
        print("Connection address: %s" % str(addr))
        
        while True:
            #time.sleep(1)
            msg = input()
            #msg = str(random.randint(1,5))
            clientsocket.send(msg.encode('utf-8'))
            
            data = clientsocket.recv(1024)
            print('Received data: ' + data.decode('utf-8'))
        
        # Close the connection
    clientsocket.close()

if __name__ == '__main__':
    start_server()