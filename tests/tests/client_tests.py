#client test
import unittest
import io
import sys
import os
import time
import asyncio
import pickle

from unittest.mock import AsyncMock, MagicMock

from Client.client import Client


class Clienttests (unittest.TestCase):


#Testing dictionary functions

    def test_dictionary_bytes(self):
        expected_bytes = b'\x80\x04\x95S\x00\x00\x00\x00\x00\x00\x00}\x94\x8c\x04boat\x94}\x94(\x8c\x04size\x94\x8c\x04ship\x94\x8c\x07country\x94\x8c\x07Finland\x94\x8c\x05cargo\x94\x8c\x08tomatoes\x94\x8c\x05color\x94\x8c\x04pink\x94us.'
        client = Client()
        bytes = client._create_dictionary_bytes()
        self.assertEqual(bytes, expected_bytes)
        
    def test_dictionary_json(self):
        expected_json = b'{\n  "boat": {\n    "size": "ship",\n    "country": "Finland",\n    "cargo": "tomatoes",\n    "color": "pink"\n  }\n}'
        client = Client()
        json = client._create_dictionary_json()
        self.assertEqual(json, expected_json)
   

    def test_dictionary_xml(self):
        expected_xml = b'<?xml version="1.0" encoding="utf-8"?>\n<boat>\n\t<size>ship</size>\n\t<country>Finland</country>\n\t<cargo>tomatoes</cargo>\n\t<color>pink</color>\n</boat>'
        client = Client()
        xml = client._create_dictionary_xml()
        self.assertEqual(xml, expected_xml)


if __name__ == '__main__':
    unittest.main()