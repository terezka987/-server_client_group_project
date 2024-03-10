import cryptography
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt

import secrets
import base64
import getpass


class KeyHolder:
    """Is initialised with password and generates a key which is held as a member"""

    def __init__(self, password: str):
        self.__salt = b'0'
        self.__key = b'0'
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
        sets self.__key from a `password` and the salt.
        """
        salt_size = 16

        # generate new salt and save it
        self.__generate_salt(salt_size)
        # generate the key from the salt and the password
        dervied_key = self.__derive_key(self.__salt, password)

        # encode it using Base 64 and save it
        self.__key = base64.urlsafe_b64encode(dervied_key)
        print(self.__key)
        print(self.__salt)

    def get_salt(self) -> bytes:
        """Return salt"""
        # print
        return self.__salt

    def get_key(self) -> bytes:
        """Return key"""
        return self.__key

    def encrypt_contents(self, contents_to_encrypt: str) -> bytes:
        """
        Takes some contents, encrypts using key and creates a in current directory
        contents_to_encrypt: the string to be encrypted
        key: key to use for for encryption/decryption
        """
        fernet = Fernet(self.__key)
        return fernet.encrypt(contents_to_encrypt)
# encrypt_file
#     with open(filename, "wb") as file:
#         file.write(encrypted_data)

    # def decrypt(filename, key):
    #     """
    #     Given a filename (str) and key (bytes), it decrypts the file and write it
    #     """
    #     f = Fernet(key)
    #     with open(filename, "rb") as file:
    #         # read the encrypted data
    #         encrypted_data = file.read()
    #     # decrypt data
    #     try:
    #         decrypted_data = f.decrypt(encrypted_data)
    #     except cryptography.fernet.InvalidToken:
    #         print("Invalid token, most likely the password is incorrect")
    #         return
    #     # write the original file
    #     with open(filename, "wb") as file:
    #         file.write(decrypted_data)
    #     print("File decrypted successfully")
