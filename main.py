
from Client.client import Client
from Server.server import Server

import sys

HELP = '-help'

if __name__ == '__main__':
    if (len(sys.argv)) < 2:
        print(
            f"Please specify whether to run client or server, or run python3 main.py {HELP}")
        exit(1)
    elif (len(sys.argv)) > 2:
        print(f"To many arguments received, try {HELP} to get options")
        exit(1)
    argument = sys.argv[1]
    if argument == HELP:
        print("Application has the following options \n \
              -c, -client: will start the client \n \
              -sos, -server: will start the server and prints to screen \n \
              -sof, -server: will start the server and prints to file")
    elif argument in ('-sos', '-server'):
        server = Server(True)
        server.run_server()
    elif argument in ('-sof', '-server'):
        server = Server(False)
        server.run_server()
    elif argument in ('-c', '-client'):
        client = Client()
        client.run_client()
    else:
        print(f'{argument} is a invalid argument, run {
              HELP} for valid arguments')
