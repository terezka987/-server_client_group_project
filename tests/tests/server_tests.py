# client test
import unittest
import io
import sys
import os
import time
import asyncio
import pickle

from unittest.mock import AsyncMock, MagicMock

from Server.server import Server


class Servertests_async (unittest.IsolatedAsyncioTestCase):

    # Test JSON data
    async def test_receive_message_json(self):
        # redirect stdout
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

        server = Server()
        reader.read = AsyncMock(return_value=data_json)
        await server._receive_message(reader, writer)

        # Asserts
        writer.get_extra_info.assert_called_once_with('peername')
        writer.close.assert_called_once_with()
        self.assertTrue("JSON" in stdout.getvalue())
        sys.stdout = sys.__stdout__  # Reset stdout redirect.

    # Test XML data
    async def test_receive_message_xml(self):
        # redirect stdout
        stdout = io.StringIO()
        sys.stdout = stdout
        # Mocking reader and writer
        reader = MagicMock()
        writer = MagicMock()

        # Create test data
        data_xml = b'<?xml version="1.0"?><root><key>value</key></root>'
        DICT_TO_SEND = {'boat': {'size': 'ship', 'country': 'Finland',
                                 'cargo': 'tomatoes', 'color': 'pink'}}

        server = Server()
        reader.read = AsyncMock(return_value=data_xml)
        await server._receive_message(reader, writer)

        # # Asserts
        writer.get_extra_info.assert_called_with('peername')
        writer.close.assert_called_with()
        self.assertTrue("XML" in stdout.getvalue())
        # self.assertTrue(b'XML' in writer.close.call_args[0])
        sys.stdout = sys.__stdout__  # Reset stdout redirect.

    # Test bytes data
    async def test_receive_message_bytes(self):
        # redirect stdout
        stdout = io.StringIO()
        sys.stdout = stdout
        # Mocking reader and writer
        reader = MagicMock()
        writer = MagicMock()

        # Create test data

        DICT_TO_SEND = {'boat': {'size': 'ship', 'country': 'Finland',
                                 'cargo': 'tomatoes', 'color': 'pink'}}
        data_bytes = pickle.dumps(DICT_TO_SEND)
        reader.read = AsyncMock(return_value=data_bytes)
        server = Server()
        await server._receive_message(reader, writer)

        # # Asserts
        writer.get_extra_info.assert_called_with('peername')
        writer.close.assert_called_with()
        self.assertTrue("bytes" in stdout.getvalue())
        sys.stdout = sys.__stdout__  # Reset stdout redirect.


if __name__ == '__main__':
    unittest.main()
