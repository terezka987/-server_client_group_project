"""This contains the server code which will handle messages sent from the client"""

from Common.encryption import KeyHolder
from Common.handleuserinput import get_password_from_user

import asyncio
import json
import pickle
import xmltodict
import io

HOST = '127.0.0.1'
PORT = 5000


class Server:
    def _handle_unencrypted_message(self, data: bytes) -> str:
        try:
            first_data = data[:6]
            message = data.decode()
            print(message)
            if b'xml' in first_data:
                print("Message is XML")
                return message
            else:
                print("Message is JSON")
                return message
        except (UnicodeDecodeError, json.JSONDecodeError):
            try:
                message = pickle.loads(data)
                print("Message is bytes")
                return message
            except pickle.UnpicklingError:
                print("Cannot understand message, discarding")
                return str()

    def _handle_encrypted_message(self, data: bytes) -> str:
        keyholder = KeyHolder("")
        data_sections = data.split(keyholder.delimiter())
        salt_length = int.from_bytes(data_sections[1])
        salt = data_sections[2][:salt_length]
        data = data_sections[2][salt_length:]
        # print(f'Data is {data}')
        # print(f'Salt is {salt}')
        password = get_password_from_user(False)
        otherkeyholder = KeyHolder(password, salt)
        decrypted_data = otherkeyholder.decrypt(data)
        decoded_data = self._handle_unencrypted_message(decrypted_data)
        print(decoded_data)
        return decoded_data

    async def _receive_message(self, reader, writer):
        """Handle message sent to server"""
        data = await reader.read(-1)

        # Need to make it so we dont need a keyholder here
        keyholder = KeyHolder("")

        if data.startswith(keyholder.encrypted_message_tag()):
            message = self._handle_encrypted_message(data)
        else:
            message = self._handle_unencrypted_message(data)
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
        """Entry point to Server"""
        asyncio.run(self._main())
