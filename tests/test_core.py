#/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import discord
import asyncio
from unittest.mock import patch
import pixie.core as core 

async def async_magic():
    pass

unittest.mock.MagicMock.__await__ = lambda x: async_magic().__await__()

class CoreTestCase(unittest.TestCase):

    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None)

    # def tearDown(self):
    #     1 == 1

    @patch('discord.Message')
    @patch('discord.User')
    def test_on_message(self, mock_message, mock_author):
        with patch.dict('pixie.data.STRINGS', {'en':
        {'unknown-args': 'Test {command}'}}):
            mock_author.id = 1
            mock_message.author = mock_author 
            self.loop.run_until_complete(core.on_message(mock_message))


suite = unittest.TestLoader().loadTestsFromTestCase(CoreTestCase)

if __name__ == '__main__':
    unittest.main()
