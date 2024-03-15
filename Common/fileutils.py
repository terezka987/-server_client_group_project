"""Contains methods for interacting with filesystem"""

import typing

DEFAULT_SECURE_FILENAME = "secure_client_file.txt"
DEFAULT_NORMAL_FILENAME = "client_file.txt"


def save_to_file(contents: typing.Union[bytes, str], filename=None):
    """
    save a contents in a file in a fixed location
    - Accepts bytes for encrypted content
    - or str for unencrypted
    """
    if isinstance(contents, bytes):
        if not filename:
            filename = DEFAULT_SECURE_FILENAME
        openmode = "wb"
    elif isinstance(contents, str):
        if not filename:
            filename = DEFAULT_NORMAL_FILENAME
        openmode = "w"
    else:
        print(f"Error unrecognised data type: {type(contents)}")
        return

    with open(filename, openmode) as file:
        file.write(contents)


def read_from_file(filename: str) -> str:
    """
    Reads an entire file from the current directory
    """
    with open(filename, 'r', encoding='utf8') as file:
        contents = file.read()
        return contents
