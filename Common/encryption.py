import cryptography
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt

import secrets
import base64
import getpass


class KeyHolder:
    """Is initialised with password and generates a key which is held as a member"""

    def __init__(self, password: str, salt=None):
        self.__salt = salt
        self.__key = b'0'
        self.__contents = b'0'
        self.__generate_key(password)
        # Can be static
        self.__delimiter = b'\n'
        self.__encrypted_tag = b'encrypted'

    def __generate_salt(self, size=16):
        """Set salt member"""
        self.__salt = secrets.token_bytes(size)

    def __derive_key(self, salt: bytes, password: str) -> bytes:
        """Derive the key from the `password` using the passed `salt`"""
        key = Scrypt(salt=salt, length=32, n=2**14, r=8, p=1)
        return key.derive(password.encode())

    def __generate_key(self, password: str):
        """
        sets self.__key from a `password` and the salt.
        """
        salt_size = 16

        # generate new salt if required and save it
        if self.__salt is None:
            self.__generate_salt(salt_size)
        # generate the key from the salt and the password
        dervied_key = self.__derive_key(self.__salt, password)

        # encode it using Base 64 and save it
        self.__key = base64.urlsafe_b64encode(dervied_key)

    def get_salt(self) -> bytes:
        """Return salt"""
        # print
        return self.__salt

    def encrypt_contents(self, contents_to_encrypt: str) -> bytes:
        """
        Takes some contents as str, encrypts using key initialised in __init__
        contents_to_encrypt: the string to be encrypted
        key: key to use for for encryption/decryption
        """
        fernet = Fernet(self.__key)
        self.__contents = fernet.encrypt(contents_to_encrypt)
        return self.__contents

    def decrypt(self, contents_to_decrypt: bytes) -> bytes:
        """
        Takes contents_to_decrypt (bytes), and decrypts using key initailised in 
        __init__
        """
        fernet = Fernet(self.__key)

        try:
            decrypted_data = fernet.decrypt(contents_to_decrypt)
        except cryptography.fernet.InvalidToken:
            print("Invalid token, most likely the password is incorrect")
        return decrypted_data

    def create_encrypted_message(self) -> bytes:
        """
        Combine salt and contents into single byte object containing
        - header allowing server to detect its encrypted
        - size of salt
        - delimiter so values can be extracted
        """
        # print(f'Contents is {self.__contents}')
        # print(f'Salt is {self.__salt}')
        encrypted_header = bytearray()
        encrypted_header.extend(self.__encrypted_tag)
        encrypted_header.extend(self.__delimiter)
        encrypted_header.append(len(self.__salt))
        encrypted_header.extend(self.__delimiter)
        encrypted_header.extend(self.__salt)
        encrypted_header.extend(self.__contents)
        return bytes(encrypted_header)

    # Can be static
    def encrypted_message_tag(self) -> bytes:
        """provide the encrypted tag"""
        return self.__encrypted_tag

    def delimiter(self) -> bytes:
        """provide the encrypted message delimiter"""
        return self.__delimiter
