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
from Server.server import Server
from Common import handleuserinput

class Commontests (unittest.TestCase):


# Testing validating user input as integer within range 0 to 5
        
    def test_handle_user_input(self):
        self.assertEqual(handleuserinput.handle_client_options(1),1)
        self.assertEqual(handleuserinput.handle_client_options(0),0)
        self.assertEqual(handleuserinput.handle_client_options(2),2)
        self.assertEqual(handleuserinput.handle_client_options(3),3)
        self.assertEqual(handleuserinput.handle_client_options(4),4)
        self.assertEqual(handleuserinput.handle_client_options(5),5)
        self.assertEqual(handleuserinput.handle_client_options(6),-1)
        self.assertEqual(handleuserinput.handle_client_options("Tereza"),-1)

if __name__ == '__main__':
    unittest.main()