"""This contains the server code which will handle messages sent from the client"""

import asyncio
import json
import pickle

from Common.encryption import KeyHolder
from Common.handleuserinput import get_password_from_user, handle_whether_to_print_or_create_file
from Common.fileutils import save_to_file

HOST = '127.0.0.1'
PORT = 5000


class Server:
    def __init__(self):
        self.__message_received = 0

    def _handle_unencrypted_message(self, data: bytes) -> str:
        try:
            first_data = data[:6]
            message = data.decode()
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
        data_sections = data.split(KeyHolder.delimiter())
        salt_length = int.from_bytes(data_sections[1])
        salt = data_sections[2][:salt_length]
        data = data_sections[2][salt_length:]
        # print(f'Data is {data}')
        # print(f'Salt is {salt}')
        password = get_password_from_user(False)
        keyholder = KeyHolder(password, salt)
        decrypted_data = keyholder.decrypt(data)
        decoded_data = self._handle_unencrypted_message(decrypted_data)
        return decoded_data

    def output_message(self, message: str, sender: str):
        """Ask user whether to print to screen or save to file"""
        successful_input = False
        while not successful_input:
            response = handle_whether_to_print_or_create_file(
                input("Type 'file' to save, and 'screen' to print to screen\n")
            )
            successful_input = response[0]
        output_type = response[1]

        if output_type == 'screen':
            print(f"Message {self.__message_received}. Received {
                  message} from {sender!r}")
        elif output_type == 'file':
            filename = f"received_message{self.__message_received}.txt"
            print(f"Saving message to disk in {filename}")

            if isinstance(message, dict):
                message = json.dumps(message)
            save_to_file(message, filename)

    async def _receive_message(self, reader, writer):
        """Handle message sent to server"""
        data = await reader.read(-1)
        self.__message_received += 1

        if data.startswith(KeyHolder.encrypted_message_tag()):
            message = self._handle_encrypted_message(data)
        else:
            message = self._handle_unencrypted_message(data)
        addr = writer.get_extra_info('peername')
        self.output_message(message, addr)
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
