import socket

HOST = '127.0.0.1'
PORT = 8888

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        while True:
            data = conn.recv(1024)
            print(data.decode())
            if data.decode() == "stop":
                break
            conn.sendall(data)
