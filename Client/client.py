"""This contains the client code for sending messages to the server"""

import asyncio
import pickle
import json
import xmltodict
from Common.fileutils import save_to_file, read_from_file, DEFAULT_NORMAL_FILENAME
from Common.encryption import KeyHolder
from Common.handleuserinput import handle_client_options, handle_whether_to_encrypt, get_password_from_user


HOST = '127.0.0.1'
PORT = 8888


DICT_TO_SEND = {'boat': {'size': 'ship', 'country': 'Finland',
                         'cargo': 'tomatoes', 'color': 'pink'}}

TEXT_TO_SEND = "I like to float on the clouds of destiny"


class Client:
    def _create_dictionary_bytes(self) -> bytes:
        """Create dictionary and return in bytes"""
        byte_msg = pickle.dumps(DICT_TO_SEND)
        print(byte_msg)
        return byte_msg

    def _create_dictionary_json(self) -> bytes:
        """Create dictionary and return in encoded json_string"""
        json_str = json.dumps(DICT_TO_SEND, indent=2)
        print(json_str)
        return json_str.encode()

    def _create_dictionary_xml(self) -> bytes:
        """Create dictionary and return in encoded XML"""
        xml_str = xmltodict.unparse(DICT_TO_SEND, pretty=True)
        print(xml_str)
        return xml_str.encode()

    def _create_file(self) -> bytes:
        """Create a text file with some contents, which is returned as bytes"""
        save_to_file(TEXT_TO_SEND)
        contents = read_from_file(DEFAULT_NORMAL_FILENAME)
        return contents.encode()

    def _get_password(self) -> str:
        """Prompt the user for a password"""
        first_entry = str()
        second_entry = str()
        while (not first_entry and not second_entry) or (first_entry != second_entry):
            first_entry = input("Enter a password to encrypt files with \n")
            second_entry = input(
                "Re-Enter the password to encrypt files with \n")
            if first_entry != second_entry:
                print("Passwords dont match, please retry setting your password")
        return first_entry

    def _encrypt_and_save_contents(self, contents: bytes) -> bytes:
        """
        Govern the encryption process by 
        - Getting password 
        - Creating a Key
        - Encrypting contents
        - Writing contents to file
        - Returns salt and encrypted_contents for sending to server
        """
        password = get_password_from_user(True)
        keyholder = KeyHolder(password)
        encrypted_contents = keyholder.encrypt_contents(contents)
        save_to_file(encrypted_contents)
        return keyholder.create_encrypted_message()

    async def _send(self, message: bytes):
        """Send messages to server"""
        reader, writer = await asyncio.open_connection(
            '127.0.0.1', PORT)

        writer.write(message)
        await writer.drain()

        print('Close the connection')
        writer.close()
        await writer.wait_closed()

    def run_client(self):
        """Entry point to client"""
        print("Options")
        print("1: Send a text file")
        print("2: Send dict as bytes")
        print("3: Send dict as json")
        print("4: Send dict as xml")
        selection = -1
        while selection == -1:
            selection = handle_client_options(
                input("Enter selection as a integer, or 0 to abort \n"))

        to_send = None

        if selection == 0:
            print("Exiting")
            return
        if selection == 1:
            to_send = self._create_file()
            print("Sending file")

        encrypt = False
        if selection in (2, 3, 4):
            successful_input = False
            while not successful_input:
                response = handle_whether_to_encrypt(
                    input("Do you want to encrypt your dictionary? enter y or n. \n")
                )
                successful_input = response[0]
            encrypt = response[1]

        if selection == 2:
            to_send = self._create_dictionary_bytes()
        if selection == 3:
            to_send = self._create_dictionary_json()
        if selection == 4:
            to_send = self._create_dictionary_xml()

        if to_send is None:
            print("No data to send, exiting")
            return

        if encrypt:
            print("Sending encrypted message")
            encrypted_contents = self._encrypt_and_save_contents(to_send)
            asyncio.run(self._send(encrypted_contents))
        else:
            print("Sending non-encrypted message")
            asyncio.run(self._send(to_send))
