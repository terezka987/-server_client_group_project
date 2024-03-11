"""This contains the client code for sending messages to the server"""

import asyncio
import pickle
import json
import xmltodict
from Common.fileutils import save_to_file
from Common.encryption import KeyHolder
from Common.handleuserinput import handle_client_options, handle_whether_to_encrypt, get_password_from_user


HOST = '127.0.0.1'
PORT = 8888


DICT_TO_SEND = {'boat': {'size': 'ship', 'country': 'Finland',
                         'cargo': 'tomatoes', 'color': 'pink'}}


def create_dictionary_bytes() -> int:
    """Create dictionary and return in bytes"""
    byte_msg = pickle.dumps(DICT_TO_SEND)
    print(byte_msg)
    return byte_msg


def create_dictionary_json() -> int:
    """Create dictionary and return in encoded json_string"""
    json_str = json.dumps(DICT_TO_SEND, indent=2)
    print(json_str)
    return json_str.encode()


def create_dictionary_xml() -> int:
    """Create dictionary and return in encoded XML"""
    xml_str = xmltodict.unparse(DICT_TO_SEND, pretty=True)
    print(xml_str)
    return xml_str.encode()

# def create_file(encrypt: bool) -> int:
#     """Needs handle encryption option"""
#     testdir = "testdir"
#     if not os.path.exists(testdir):
#         os.mkdir(testdir)
#     text_to_file = "Test Text"
#     path_to_file = testdir + "/test.txt"
#     with open(path_to_file, "w", encoding="utf8") as file:
#         file.write(text_to_file)
#     with open(path_to_file, "r", encoding="utf8") as file:
#         content = file.read()
#         byte_msg = pickle.dumps(content)
#         return byte_msg


# def send(dict_to_send: dict):
#     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#         s.connect((HOST, PORT))
#         byte_msg = pickle.dumps(dict_to_send)
#         s.sendall(byte_msg)

# def send(bytes_to_send: int):
#     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#         s.connect((HOST, PORT))
#         s.sendall(bytes_to_send)


def encrypt_and_save_contents(contents: bytes) -> bytes:
    """
    Govern the encryption process by 
    - Getting password 
    - Creating a Key
    - Encrypting contents
    - Writing contents to file
    - Returns salt and encrypted_contents for sending to server
    """
    password = get_password_from_user()
    keyholder = KeyHolder(password)
    encrypted_contents = keyholder.encrypt_contents(contents)
    save_to_file(encrypted_contents)
    return keyholder.create_encrypted_message()


async def send(message: bytes):
    """Send messages to server"""
    reader, writer = await asyncio.open_connection(
        '127.0.0.1', PORT)

    writer.write(message)
    await writer.drain()

    print('Close the connection')
    writer.close()
    await writer.wait_closed()


def run_client():
    """Entry point to client"""
    print("Options")
    print("3: Send dict as bytes")
    print("4: Send dict as json")
    print("5: Send dict as xml")
    selection = -1
    while selection == -1:
        selection = handle_client_options(
            input("Enter selection as a integer, or 0 to abort \n"))

    if selection == 0:
        print("Exiting")
        return
    # if selection == 1:
    #     bytes_to_send = create_file(False)
    #     print("Sending unencrypted file")
    # if selection == 2:
    #     bytes_to_send = create_file(True)
    #     print("Sending encrypted file")

    encrypt = False
    if selection in (3, 4, 5):
        successful_input = False
        while not successful_input:
            response = handle_whether_to_encrypt(
                input("Do you want to encrypt your dictionary? \n")
            )
            successful_input = response[0]
        encrypt = response[1]

    if selection == 3:
        to_send = create_dictionary_bytes()
    if selection == 4:
        to_send = create_dictionary_json()
    if selection == 5:
        to_send = create_dictionary_xml()

    if encrypt:
        print("Sending encrypted message")
        encrypted_contents = encrypt_and_save_contents(to_send)
        asyncio.run(send(encrypted_contents))
    else:
        print("Sending non-encrypted message")
        asyncio.run(send(to_send))
