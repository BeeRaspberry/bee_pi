import unittest
from unittest.mock import patch

from cmd_config import (print_help, prompt, check_for_probes)


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

    def test_check_for_probes(self):
        settings = {
            "host": "localhost", "probes": [
            {"pin": 4, "sensor": 22, "outdoor": "False"},
            {"pin": 21, "sensor": 11, "outdoor": "True"}],
            "dataStore": 0, "delay": 300, "hiveId": 1,
            "filename": "hivedata.csv"}
        self.assertEqual(check_for_probes(settings), True)

    def test_check_for_probes_no_probe(self):
        settings = {
            "host": "localhost", "filename": "hivedata.csv",
            "dataStore": 0, "delay": 300, "hiveId": 1,
        }
        self.assertEqual(check_for_probes(settings), False)

    def test_check_for_probes_zero_length(self):
        settings = {
            "host": "localhost", "probes": [],
            "dataStore": 0, "delay": 300, "hiveId": 1,
            "filename": "hivedata.csv"
        }
        self.assertEqual(check_for_probes(settings), False)