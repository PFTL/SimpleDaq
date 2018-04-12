# -*- coding: utf-8 -*-

import unittest
from PythonForTheLab.Model.daq import DummyDaq

dummy_model = DummyDaq(0)

class DummyDaqTest(unittest.TestCase):

    def test_analog_output(self):
        dummy_model.set_analog_value(0, 10)

    def test_analog_input(self):
        value = dummy_model.get_analog_value(0)
        self.assertGreaterEqual(value.m, 0, 'The output of the reading should be >0 ')