import socket

HOST = '127.0.0.1'
PORT = 5000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        user_input = input("Enter your message \n")
        s.sendall(str(user_input).encode('utf-8'))
        if user_input == "stop":
            break
        
        data = s.recv(1024)
        s
        print('Echoing: ', repr(data.decode()))