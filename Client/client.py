
import socket
import pickle

HOST = '127.0.0.1'
PORT = 5000


def create_dictionary() -> dict:
    dict_to_send = {"one": 1, "two": [1, 2], "three": {
        "threepointone": 3.1, "threepointtwo": 3.2}}
    return dict_to_send


def send(dict_to_send: dict):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        byte_msg = pickle.dumps(dict_to_send)
        s.sendall(byte_msg)


if __name__ == '__main__':
    dict_to_send = create_dictionary()
    send(dict_to_send)
