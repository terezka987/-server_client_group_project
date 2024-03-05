import asyncio
import xmltodict
import json
import os
import socket
import pickle

HOST = '127.0.0.1'
PORT = 5000


DICT_TO_SEND = {'plane': {'year': '1977', 'make': 'Cessna',
                          'model': 'Skyhawk', 'color': 'Light blue and white'}}

# DICT_TO_SEND = {"one": 1, "two": [1, 2], "three": {
#     "threepointone": 3.1, "threepointtwo": 3.2}}


def create_dictionary_bytes() -> int:
    """Needs handle xml, json or bytes"""
    byte_msg = pickle.dumps(DICT_TO_SEND)
    return byte_msg


def create_dictionary_json() -> str:
    """Needs handle xml, json or bytes"""
    json_str = json.dumps(DICT_TO_SEND)
    return json_str.encode()


def create_dictionary_xml() -> int:
    """Needs handle xml, json or bytes"""
    xml_str = xmltodict.unparse(DICT_TO_SEND, pretty=True)
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

async def send(message: int):
    reader, writer = await asyncio.open_connection(
        '127.0.0.1', 8888)

    writer.write(message)
    await writer.drain()

    print('Close the connection')
    writer.close()
    await writer.wait_closed()


def handle_user_input(user_input: str) -> int:
    """
    Test that the input is integer
    If valid return entered number
    If not valid return -1
    """
    try:
        input_num = int(user_input)

    except ValueError:
        print("Entered value is not a integer")
        return -1

    if input_num not in (0, 1, 2, 3, 4, 5):
        print("Entered value should be between 0 and 5")
        return -1
    return input_num


if __name__ == '__main__':

    print("Options")
    print("3: Send dict as bytes")
    print("4: Send dict as json")
    print("5: Send dict as xml")
    selection = -1
    while selection == -1:
        selection = handle_user_input(
            input("Enter selection as a integer, or 0 to abort \n"))

    # print("Options")
    # print("1: No Encryption")
    # print("2: Encryption")
    # while encrypt_selection == -1:
    #     encrypt_selection = handle_user_input(
    #         input("Enter selection as a integer, or 0 to abort \n"))

    if selection == 0:
        print("Exiting")
    # if selection == 1:
    #     bytes_to_send = create_file(False)
    #     print("Sending unencrypted file")
    # if selection == 2:
    #     bytes_to_send = create_file(True)
    #     print("Sending encrypted file")
    if selection == 3:
        to_send = create_dictionary_bytes()
    if selection == 4:
        to_send = create_dictionary_json()
    if selection == 5:
        to_send = create_dictionary_xml()

    asyncio.run(send(to_send))
