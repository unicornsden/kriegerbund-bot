# /usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from unittest.mock import patch
import pixie.messages as messages


class MessageExtractionTestCase(unittest.TestCase):

    @patch('pixie.messages.MessageWrapper')
    def setUp(self, mock_message):
        self.message = mock_message

    def tearDown(self):
        # Revert setup stuff
        self.message = None

    def test_simple_extraction(self):
        self.message.content = '!command'
        self.assertEqual(messages.get_command(self.message, '!'), 'command')

    def test_extraction_with_multiple_prefixes(self):
        prefixes = ['!', '$', 'ü!']
        self.message.content = '$command'
        self.assertEqual(messages.get_command(self.message, prefixes), 'command')
        self.message.content = 'ü!command'
        self.assertEqual(messages.get_command(self.message, prefixes), 'command')

    def test_extraction_with_args(self):
        prefixes = ['!', '$', 'ü!']
        self.message.content = '!command arg1 arg2 arg3'
        self.assertEqual(messages.get_command(self.message, prefixes), 'command')


class ArgsExtractionTestCase(unittest.TestCase):

    @patch('pixie.messages.MessageWrapper')
    def setUp(self, mock_message):
        self.message = mock_message

    def tearDown(self):
        # Revert setup stuff
        self.message = None

    def test_args_extraction(self):
        self.message.content = '!command arg1 arg2 arg3'
        self.assertEqual(messages.get_args(self.message), ['arg1', 'arg2',
                                                           'arg3'])


class BuildStringTestCase(unittest.TestCase):

    def test_get_string(self):
        with patch.dict('pixie.data.STRINGS', {'en': {'test1': 'Test 1'}}):
            self.assertEqual(messages.get_string('test1'), 'Test 1')
            self.assertEqual(messages.get_string('test2'), None)

    def test_different_langs(self):
        with patch.dict('pixie.data.STRINGS', {'en': {'test1': 'Test 1',
                                                      'test2': 'Test 2'}, 'de': {'test1': '1. Test'}}):
            self.assertEqual(messages.get_string('test1', 'de'), '1. Test')
            self.assertEqual(messages.get_string('test2', 'en'), 'Test 2')
            self.assertEqual(messages.get_string('test2', 'de'), 'Test 2')
            self.assertIsNone(messages.get_string('test3'))

    @patch('pixie.data.CMDCHAR', '!')
    @patch('pixie.messages.MessageWrapper')
    def test_unknown_usage(self, message):
        with patch.dict('pixie.data.STRINGS', {'en':
                                                   {'unknown-args': 'Test {command}'}}):
            message.command = 'test'
            self.assertEqual(messages.get_string('unknown-args'),
                             'Test {command}')


suite = unittest.TestLoader().loadTestsFromTestCase(MessageExtractionTestCase)
suite = unittest.TestLoader().loadTestsFromTestCase(ArgsExtractionTestCase)
suite = unittest.TestLoader().loadTestsFromTestCase(BuildStringTestCase)

if __name__ == '__main__':
    unittest.main()
