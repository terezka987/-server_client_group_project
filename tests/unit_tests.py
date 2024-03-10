#client test
import unittest
import io
import sys
import os
import time
import asyncio
import pickle

from unittest.mock import AsyncMock, MagicMock

from Client import client
from Server import server
class Unittests (unittest.TestCase):



#Testing dictionary functions

    def test_dictionary_bytes(self):
        expected_bytes = b'\x80\x04\x95S\x00\x00\x00\x00\x00\x00\x00}\x94\x8c\x04boat\x94}\x94(\x8c\x04size\x94\x8c\x04ship\x94\x8c\x07country\x94\x8c\x07Finland\x94\x8c\x05cargo\x94\x8c\x08tomatoes\x94\x8c\x05color\x94\x8c\x04pink\x94us.'
        bytes = client.create_dictionary_bytes()
        self.assertEqual(bytes, expected_bytes)
        
    def test_dictionary_json(self):
        expected_json = b'{\n  "boat": {\n    "size": "ship",\n    "country": "Finland",\n    "cargo": "tomatoes",\n    "color": "pink"\n  }\n}'
        json = client.create_dictionary_json()
        self.assertEqual(json, expected_json)
   

    def test_dictionary_xml(self):
        expected_xml = b'<?xml version="1.0" encoding="utf-8"?>\n<boat>\n\t<size>ship</size>\n\t<country>Finland</country>\n\t<cargo>tomatoes</cargo>\n\t<color>pink</color>\n</boat>'
        xml = client.create_dictionary_xml()
        self.assertEqual(xml, expected_xml)


#Testing validating user input as integer within range 0 to 5
        
    def test_handle_user_input(self):
        self.assertEqual(client.handle_user_input(1),1)
        self.assertEqual(client.handle_user_input(0),0)
        self.assertEqual(client.handle_user_input(2),2)
        self.assertEqual(client.handle_user_input(3),3)
        self.assertEqual(client.handle_user_input(4),4)
        self.assertEqual(client.handle_user_input(5),5)
        self.assertEqual(client.handle_user_input(6),-1)
        self.assertEqual(client.handle_user_input("Tereza"),-1)

class Unittests_async (unittest.IsolatedAsyncioTestCase):
#Testing receive message method from server
    async def test_receive_message(self):
        #redirect stdout
        stdout = io.StringIO()
        sys.stdout = stdout
        # Mocking reader and writer
        reader = MagicMock()
        writer = MagicMock()

        # Create test data
        data_json = b'{"key": "value"}'
        data_xml = b'<?xml version="1.0"?><root><key>value</key></root>'
        DICT_TO_SEND = {'boat': {'size': 'ship', 'country': 'Finland',
                         'cargo': 'tomatoes', 'color': 'pink'}}
        data_bytes = pickle.dumps(DICT_TO_SEND)

        # Test JSON data
        reader.read = AsyncMock(return_value=data_json)
        await server.receive_message(reader, writer)

        # Asserts
        writer.get_extra_info.assert_called_once_with('peername')
        writer.close.assert_called_once_with()
        self.assertTrue("JSON" in stdout.getvalue())
       
        # Test XML data
        reader.read = AsyncMock(return_value=data_xml)
        await server.receive_message(reader, writer)

        # # Asserts
        writer.get_extra_info.assert_called_with('peername')
        writer.close.assert_called_with()
        self.assertTrue("XML" in stdout.getvalue())
        # self.assertTrue(b'XML' in writer.close.call_args[0])

        # # Test bytes data
        reader.read = AsyncMock(return_value=data_bytes)
        await server.receive_message(reader, writer)

        # # Asserts
        writer.get_extra_info.assert_called_with('peername')
        writer.close.assert_called_with()
        self.assertTrue("bytes" in stdout.getvalue())
        sys.stdout = sys.__stdout__  # Reset stdout redirect.

if __name__ == '__main__':
    unittest.main()