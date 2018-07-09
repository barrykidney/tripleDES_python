import unittest
from DES import DataEncryptionSystem


class DESTest(unittest.TestCase):

    def setUp(self):
        self.d = DataEncryptionSystem()

    def tearDown(self):
        self.d.set_key("")

    param_list = [("1", "0001", "1 == 0001"), ("13", "00010011", "13 == 10010011"),
                  ("1a", "00011010", "1a == 00011010"),
                  ("", "Error: key value is empty.", "that a blank entry returns an error"),
                  ("3s76", "Error: character s in key is out of range.",
                   "that an invalid character entry returns an error")]

    def test_convert_string_to_hex(self):
        for param in self.param_list:
            self.convert_string_to_hex(param[0], param[1], param[2])

    def convert_string_to_hex(self, param1, param2, param3):
        self.d.set_key(param1)
        self.assertEqual(param2, self.d.convert_to_hex(), 'Testing ' + param3)

    @unittest.skip("WIP")
    def test_missing_entry_raises_keyError(self):
        with self.assertRaises(KeyError):
            self.d.set_message("missing")

