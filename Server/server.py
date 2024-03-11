import asyncio
import json
import pickle
import xmltodict

HOST = '127.0.0.1'
PORT = 5000

# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#     s.bind((HOST, PORT))
#     s.listen()
#     conn, addr = s.accept()
#     # need to handle broken connection and possibly loop
#     with conn:
#         data = conn.recv(1024)
#         output_dict = pickle.loads(data)
#         print(type(output_dict))
#         print(output_dict)


async def __receive_message(reader, writer):
    """Handle message sent to server"""
    data = await reader.read(-1)
    first_data = data[:6]
    print(first_data)
    try:
        # Json
        message = data.decode()
        if b'xml' in first_data:
            message = xmltodict.parse(message)
            print("Message is XML")
        else:
            message = json.loads(message)
            print("Message is JSON")
    except (UnicodeDecodeError, json.JSONDecodeError):
        # bytes
        try:
            message = pickle.loads(data)
            print("Message is bytes")
        except pickle.UnpicklingError:
            print("Cannot understand message, discarding")

    addr = writer.get_extra_info('peername')

    print(f"Received {message!r} from {addr!r}")

    print("Finished handling message")
    writer.close()


async def __main():
    """Begin the server"""
    server = await asyncio.start_server(
        __receive_message, '127.0.0.1', 8888)

    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')

    async with server:
        await server.serve_forever()


def run_server():
    """Entry point to file"""
    asyncio.run(__main())
