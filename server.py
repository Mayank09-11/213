import socket
import threading
from pynput.keyboard import Controller
from screeninfo import get_monitors

SERVER = None
IP_ADDRESS = (int(input('YOUR_IP_ADDRESS')))  # Replace with your IP address
PORT = 12345  # You can choose any available port number
keyboard = Controller()

def setup():
    global SERVER, IP_ADDRESS, PORT
    
    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.bind((IP_ADDRESS, PORT))
    SERVER.listen(100)
    
    print(f"Server is listening on {IP_ADDRESS}:{PORT}")
    
    getDeviceSize()
    acceptConnections()

def getDeviceSize():
    for monitor in get_monitors():
        print(f"Width: {monitor.width}, Height: {monitor.height}")

def acceptConnections():
    global SERVER
    
    while True:
        client_socket, client_address = SERVER.accept()
        print(f"Accepted connection from {client_address}")
        threading.Thread(target=recvMessage, args=(client_socket,)).start()

def recvMessage(client_socket):
    global keyboard
    
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message:
                print(f"Received message: {message}")
                if message.startswith('PRESS'):
                    key = message.split(':')[1]
                    keyboard.press(key)
                elif message.startswith('RELEASE'):
                    key = message.split(':')[1]
                    keyboard.release(key)
        except:
            client_socket.close()
            break

if __name__ == "__main__":
    setup()
