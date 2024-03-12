import asyncio
import pickle
import xmltodict

HOST = '127.0.0.1'
PORT = 5000


class Server:
    async def _receive_message(self, reader, writer):
        """Handle a incoming message"""
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

    async def _main(self):
        server = await asyncio.start_server(
            self._receive_message, '127.0.0.1', 8888)

        addr = server.sockets[0].getsockname()
        print(f'Serving on {addr}')

        async with server:
            await server.serve_forever()

    def run_server(self):
        asyncio.run(self._main())
