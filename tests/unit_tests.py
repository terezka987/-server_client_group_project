#client test
import unittest
import pprint
import io
import os
import time
import asyncio

from Client import client
from Server import server
class Unittests (unittest.TestCase):



#Testing dictionary functions
    DICT_TO_SEND = {'boat': {'size': 'ship', 'country': 'Finland',
                         'cargo': 'tomatoes', 'color': 'pink'}}

    # def test_dictionary_bytes(self):
    #     expected_bytes = b'\x80\x04\x95S\x00\x00\x00\x00\x00\x00\x00}\x94\x8c\x04boat\x94}\x94(\x8c\x04size\x94\x8c\x04ship\x94\x8c\x07country\x94\x8c\x07Finland\x94\x8c\x05cargo\x94\x8c\x08tomatoes\x94\x8c\x05color\x94\x8c\x04pink\x94us.'
    #     bytes = client.create_dictionary_bytes()
    #     self.assertEqual(bytes, expected_bytes)
        
    # def test_dictionary_json(self):
    #     expected_json = b'{\n  "boat": {\n    "size": "ship",\n    "country": "Finland",\n    "cargo": "tomatoes",\n    "color": "pink"\n  }\n}'
    #     json = client.create_dictionary_json()
    #     self.assertEqual(json, expected_json)
   

    # def test_dictionary_xml(self):
    #     expected_xml = b'<?xml version="1.0" encoding="utf-8"?>\n<boat>\n\t<size>ship</size>\n\t<country>Finland</country>\n\t<cargo>tomatoes</cargo>\n\t<color>pink</color>\n</boat>'
    #     xml = client.create_dictionary_xml()
    #     self.assertEqual(xml, expected_xml)


#Testing validating user input as integer within range 0 to 5
        
    # def test_handle_user_input(self):
    #     self.assertEqual(client.handle_user_input(1),1)
    #     self.assertEqual(client.handle_user_input(0),0)
    #     self.assertEqual(client.handle_user_input(2),2)
    #     self.assertEqual(client.handle_user_input(3),3)
    #     self.assertEqual(client.handle_user_input(4),4)
    #     self.assertEqual(client.handle_user_input(5),5)
    #     self.assertEqual(client.handle_user_input(6),-1)
    #     self.assertEqual(client.handle_user_input("Tereza"),-1)

class Unittests_async (unittest.IsolatedAsyncioTestCase):
#Testing receive message method from server
    

    async def test_receive_message(self):
        writer = io.StringIO("xml")
        reader = io.StringIO()
        r = await server.receive_message(reader, writer)
        print(reader.read())
        self.assertTrue(r)





#Test that dictionary has 3 entries
    # def test_dictionary(self):
    #     dict_to_send = client.create_dictionary()
    #     self.assertTrue(len(dict_to_send) == 3)

#Test that we can connect the client to the server
    # def test_connection(self):
    #     os.system("python3 Server/server.py &")
    #     time.sleep(1)
    #     dict_to_send = client.create_dictionary()
    #     client.send(dict_to_send)


if __name__ == '__main__':
