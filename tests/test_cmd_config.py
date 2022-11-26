import os
from datetime import datetime

import unittest
import pytest
from unittest.mock import patch

from cmd_config import (print_help, prompt)

SETTINGS = {"host": "localhost", "probes": [
    {"pin": 4, "sensor": 22, "outdoor": "False"},
    {"pin": 21, "sensor": 11, "outdoor": "True"}],
    "dataStore": 0, "delay": 300, "hiveId": 1, "filename": "hivedata.csv"}


class TestCmdConfig(unittest.TestCase):
    @patch('builtins.input', side_effect=[1])
    def test_prompt_input(self, mock_inputs):
        self.assertEqual(
            prompt(
                message='test', error_message='test_error',
                isvalid=lambda v: int(v), default_value=None
            ),
            1
        )
    @patch('builtins.input', side_effect=[''])
    def test_prompt_no_input(self, mock_inputs):
        self.assertEqual(
            prompt(
                message='test', error_message='test_error',
                isvalid=lambda v: v in ('', None, 'N'), default_value=None
            ),
            ''
        )

    @patch('builtins.input', side_effect=['Y'])
    def test_print_help_yes(self, mock_inputs):
        self.assertEqual(print_help(), True)

    @patch('builtins.input', side_effect=[''])
    def test_print_help_false(self, mock_inputs):
        self.assertEqual(print_help(), False)
