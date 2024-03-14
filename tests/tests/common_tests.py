import unittest
from Common import handleuserinput

from Common.encryption import KeyHolder


class Commontests (unittest.TestCase):
    # Testing validating user input as integer within range 0 to 5
    def test_handle_user_input(self):
        self.assertEqual(handleuserinput.handle_client_options(1), 1)
        self.assertEqual(handleuserinput.handle_client_options(0), 0)
        self.assertEqual(handleuserinput.handle_client_options(2), 2)
        self.assertEqual(handleuserinput.handle_client_options(3), 3)
        self.assertEqual(handleuserinput.handle_client_options(4), 4)
        self.assertEqual(handleuserinput.handle_client_options(5), 5)
        self.assertEqual(handleuserinput.handle_client_options(6), -1)
        self.assertEqual(handleuserinput.handle_client_options("Tereza"), -1)

# Testing that the salt method returns something:
    def test_get_salt(self):
        keyholder = KeyHolder("password")
        salt = keyholder.get_salt()
        self.assertIsInstance(salt, bytes)
        print(salt)

# Testing encryption and decryption:
    def test_encrypt_contents(self):
        keyholder = KeyHolder("password")
        message = b"Tereza"
        cipher_text = keyholder.encrypt_contents(message)
        decrypted_message = keyholder.decrypt(cipher_text)
        self.assertEqual(decrypted_message, message)


# Testing handle_whether_to_encrypt

    def test_handle_whether_to_encrypt(self):
        res = handleuserinput.handle_whether_to_encrypt("y")
        self.assertEqual(res, (True, True))
        res = handleuserinput.handle_whether_to_encrypt("n")
        self.assertEqual(res, (True, False))
        res = handleuserinput.handle_whether_to_encrypt("5")
        self.assertEqual(res, (False, False))


if __name__ == '__main__':
    unittest.main()
