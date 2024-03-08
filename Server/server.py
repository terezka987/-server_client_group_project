import asyncio
import pickle
import xmltodict

HOST = '127.0.0.1'
PORT = 5000
#method for listening
def serve():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            data = conn.recv(1024)
            output_dict = pickle.loads(data)
            print(type(output_dict))
            print(output_dict)

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


async def receive_message(reader, writer):
    data = await reader.read(-1)
    first_data = data[:6]
    print(first_data)
    try:
        # Json
        message = data.decode()
        if b'xml' in first_data:
            print("Message is XML")
            message = xmltodict.parse(message)
        else:
            print("Message is JSON")
    except UnicodeDecodeError:
        # bytes
        message = pickle.loads(data)
        print("Message is bytes")

    addr = writer.get_extra_info('peername')

    print(f"Received {message!r} from {addr!r}")

    print("Finished handling message")
    writer.close()


async def main():
    server = await asyncio.start_server(
        receive_message, '127.0.0.1', 8888)

    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')

    async with server:
        await server.serve_forever()

asyncio.run(main())
