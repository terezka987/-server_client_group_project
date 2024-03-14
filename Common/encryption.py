"""
This file contains the KeyHolder class
This can be initialised with 
- password only, for encryption, and will create salt and key.
- password and salt, for decryption, and will create key.

Encryption
- encrypt_contents, precursor for sending to server, for saving to file.
- create_encrypted_message, for sending to server.

Decryption
- Use @classmember functions to facilitate processing contents
- decrypt, takes contents and uses key to decrypt
"""
import secrets
import base64

import cryptography
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt


class KeyHolder:
    """Is initialised with password and generates a key which is held as a member"""
    # static members
    __delimiter = b'\n'
    __encrypted_tag = b'encrypted'

    def __init__(self, password: str, salt=None):
        self.__salt = salt
        self.__key = b'0'
        self.__contents = b'0'
        self.__generate_key(password)

    def __generate_salt(self, size=16):
        """Set salt member"""
        self.__salt = secrets.token_bytes(size)

    def __derive_key(self, salt: bytes, password: str) -> bytes:
        """Derive the key from the `password` using the passed `salt`"""
        key = Scrypt(salt=salt, length=32, n=2**14, r=8, p=1)
        return key.derive(password.encode())

    def __generate_key(self, password: str):
        """
        sets self.__key 
        password will be used in generation of key
        salt should be None encryption and will be generated

        key is stored internally and is not available to callers
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
        Returns: encrypted bytes
        Stores: encrypted bytes
        """
        fernet = Fernet(self.__key)
        self.__contents = fernet.encrypt(contents_to_encrypt)
        return self.__contents

    def decrypt(self, contents_to_decrypt: bytes) -> bytes:
        """
        Takes contents_to_decrypt (bytes), and decrypts using key initailised in 
        __init__

        Returns: decrypted bytes
        """
        fernet = Fernet(self.__key)

        try:
            decrypted_data = fernet.decrypt(contents_to_decrypt)
        except cryptography.fernet.InvalidToken:
            print("Invalid token, most likely the password is incorrect")
            return bytes()
        return decrypted_data

    def create_encrypted_message(self) -> bytes:
        """
        Should be called after encrypt_contents

        Combine salt and contents into single byte object containing
        - tag, identifies contents as encrypted, can be accessed via @classmethods
        - size of salt
        - salt
        - contents
        - A delimiter is used, can be accessed via @classmethods

        Returns: bytes containing above info
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

    @classmethod
    def encrypted_message_tag(cls) -> bytes:
        """provide the encrypted tag"""
        return KeyHolder.__encrypted_tag

    @classmethod
    def delimiter(cls) -> bytes:
        """provide the encrypted message delimiter"""
        return KeyHolder.__delimiter
