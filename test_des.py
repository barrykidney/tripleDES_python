import unittest
from DES import DataEncryptionSystem
from DES import *
# from DES import *
from csv_read import read_csv
from f import *
from Generate_keys import *
import binascii

class DESTest(unittest.TestCase):

    def setUp(self):
        self.d = DataEncryptionSystem()

        file_path = "files/"
        self.__sbox = []
        self.pc_1 = read_csv(file_path, "pc_1.csv")
        self.ip = read_csv(file_path, "ip.csv")
        self.e_bit_table = read_csv(file_path, "e_bit_table.csv")
        self.p_table = read_csv(file_path, "p_table.csv")
        self.temp_box = read_csv(file_path, "__sbox.csv")
        for x in range(8):
            self.__sbox.append([])
            for y in range(64):
                self.__sbox[x].append(self.temp_box[(x * 64) + y])

    def tearDown(self):
        self.d.set_key("")

    param_list = [("1", "0001", "1 == 0001"), ("13", "00010011", "13 == 10010011"),
                  ("1a", "00011010", "1a == 00011010"),
                  ("", "Error: key value is empty.", "that a blank entry returns an error"),
                  ("3s76", "Error: character s in key is out of range.",
                   "that an invalid character entry returns an error")]

    def convert_64bit_byte_array_to_bin_str(self):
        for param in self.param_list:
            self.byte_to_bin_str(param[0], param[1], param[2])

    def byte_to_bin_str(self, param1, param2, param3):
        self.d.set_key(param1)
        self.assertEqual(param2, self.d.convert_64bit_byte_array_to_bin_str(), 'Testing ' + param3)

    def test_function_f(self):
        K1 = 0b000110110000001011101111111111000111000001110010
        R0 = 0b11110000101010101111000010101010
        expect = "00100011010010101010100110111011"
        # bin(f(R0, K1, self.e_bit_table, self.__sbox, self.p_table))[2:].zfill(32)
        self.assertEqual(expect, str(bin(f(R0, K1, self.e_bit_table, self.__sbox, self.p_table))[2:].zfill(32)), 'Testing f')

    # def test_function_un_f(self):
    #     K1 = 0b000110110000001011101111111111000111000001110010
    #     Rn = "00100011010010101010100110111011"
    #     expect = "11110000101010101111000010101010"
    #     print("expect: ", expect)
    #     # bin(f(Rn, K1, self.e_bit_table, self.__sbox, self.p_table))[2:].zfill(32)
    #     self.assertEqual(expect, str(bin(un_f(Rn, K1, self.e_bit_table, self.__sbox, self.p_table))[2:].zfill(32)), 'Testing f')

    @unittest.skip("WIP")
    def test_missing_entry_raises_keyError(self):
        with self.assertRaises(KeyError):
            self.d.set_message("missing")

    def test_pc1_substitution(self):
        input =  "0001001100110100010101110111100110011011101111001101111111110001"
        expect = "11110000110011001010101011110101010101100110011110001111"
        self.assertEqual(expect, substitution(self.pc_1, input))

    def test_ip_substitution(self):
        input =  "0000000100100011010001010110011110001001101010111100110111101111"
        expect = "1100110000000000110011001111111111110000101010101111000010101010"
        self.assertEqual(expect, substitution(self.ip, input))

    def test_hex_to_bin(self):
        input =  "1"
        expect = "0001"
        self.assertEqual(expect, DataEncryptionSystem.hex_to_bin(input))


if __name__ == '__main__':
    unittest.main()
