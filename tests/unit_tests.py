#client test
import unittest
import pprint
import os
import time

from Client import client
from Server import server
class Unittests (unittest.TestCase):

#Test that dictionary has 3 entries
    def test_dictionary(self):
        dict_to_send = client.create_dictionary()
        self.assertTrue(len(dict_to_send) == 3)

#Test that we can connect the client to the server
    def test_connection(self):
        os.system("python3 Server/server.py &")
        time.sleep(1)
        dict_to_send = client.create_dictionary()
        client.send(dict_to_send)

if __name__ == '__main__':
    unittest.main()