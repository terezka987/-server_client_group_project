
from Client.client import run_client
from Server.server import run_server

import sys

if __name__ == '__main__':
    if (len(sys.argv)) < 2:
        print(
            "Please specify whether to run client or server, or run python3 main.py -help")
        exit(1)
    argument = sys.argv[1]
    if argument == 'help':
        print("Application has the following options \n \
              -c, -client: will start the client \n \
              -s, -server: will start the server")
    elif argument in ('-s', '-server'):
        run_server()
    elif argument in ('-c', '-client'):
        run_client()
    else:
        print(f'{argument} is a invalid argument, run --help for valid arguments')
