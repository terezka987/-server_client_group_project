import os
import typing


def save_to_file(contents: typing.Union[bytes, str]):
    """save a contents in a file in a fixed location"""
    filename = "secure_file.txt"
    with open(filename, "wb") as file:
        file.write(contents)
