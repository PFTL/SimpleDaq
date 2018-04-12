# -*- coding: utf-8 -*-

import unittest
from PythonForTheLab.Model.daq import DummyDaq


class DummyDaqTest(unittest.TestCase):
    def setUp(self):
        self.dummy_model = DummyDaq(0)
    def test_analog_output(self):
        self.dummy_model.set_analog_value(0, 10)

    def test_analog_input(self):
        value = self.dummy_model.get_analog_value(0)
        self.assertGreaterEqual(value.m, 0, 'The output of the reading should be >0 ')

    def test_idn(self):
        idn = self.dummy_model.idn()
        if not isinstance(idn, str):
            self.fail('Failed to get the IDN')