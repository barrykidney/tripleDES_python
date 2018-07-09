import math
import csv
import binascii


class DataEncryptionSystem:

    message = ""
    key = ""
    shifts = []
    pc_1 = []
    pc_2 = []
    ip = []
    e_bit_table = []
    __sbox = []
    p_table = []
    ip_1 = []

    def __init__(self):
        self.shifts = self.read_csv("files/shifts.csv")
        self.pc_1 = self.read_csv("files/pc_1.csv")
        self.pc_2 = self.read_csv("files/pc_2.csv")
        self.ip = self.read_csv("files/ip.csv")
        self.e_bit_table = self.read_csv("files/e_bit_table.csv")
        self.p_table = self.read_csv("files/p_table.csv")
        self.ip_1 = self.read_csv("files/ip_1.csv")

        temp_box = self.read_csv("files/__sbox.csv")
        for x in range(8):
            self.__sbox.append([])
            for y in range(64):
                self.__sbox[x].append(temp_box[(x*64)+y])

    def set_key(self, k):
        if len(k) < 16:
            return "Error: key too short"
        else:
            self.key = k[:16]

    def get_key(self):
        return self.key

    def set_message(self, m):
        self.message = m

    def get_message(self):
        return self.message

    @staticmethod
    def read_csv(filename):
        file = open(filename, "r")
        reader = csv.reader(file)
        x = []
        for r in reader:
            for s in r:
                x.append(s)
        file.close()
        return x

    @staticmethod
    def convert_to_hex(s):
        """ Convert each char to its ASCII base 10 number using ord() then range the results between 0 and 15. Convert
        that number to binary using bin() then drop the leading '0b'. example: b -> B -> 66 -> 11 -> 0b1011 -> 1011.
        If a char conversion has less than 4 bits pad with zeros. Finally concatenate each to the string 'k'."""

        if len(s) < 1:
            return "Error: key value is empty."

        k = ""
        for ch in s:
            a = ord(ch.upper())
            if 47 < a < 58:
                ch_binary = bin(a - 48)[2:]
            elif 64 < a < 71:
                ch_binary = bin(a - 55)[2:]
            else:
                return "Error: character " + str(ch) + " in key is out of range."
            while len(ch_binary) < 4:
                ch_binary = '0' + ch_binary
            k += ch_binary
        return k

    @staticmethod
    def remove_first_bit(numb):
        numb -= int(math.pow(2, len(bin(numb)[2:]) - 1))
        return numb

    def substitution_pc_1(self, m):
        s = ""
        for idx in self.pc_1:
            s += m[int(idx)]
        return s

    @staticmethod
    def split_key(k):
        c = {"c0": int(k[:28], 2)}
        d = {"d0": int(k[28:], 2)}
        # print("c0: ", bin(int(k[:28], 2))[2:].zfill(28))
        # print("d0: ", bin(int(k[28:], 2))[2:].zfill(28))
        return c, d

    def gen_key_blocks(self, c, d):
        for x in range(len(self.shifts)):
            sft = int(self.shifts[x])
            cf = c["c" + str(x)]
            df = d["d" + str(x)]

            while sft > 0:
                cf = cf << 1
                if len(bin(cf)[2:]) > 28:
                    cf += 1
                    cf = self.remove_first_bit(cf)

                df = df << 1
                if len(bin(df)[2:]) > 28:
                    df += 1
                    df = self.remove_first_bit(df)
                sft -= 1

            c["c{0}".format(x + 1)] = cf
            d["d{0}".format(x + 1)] = df

        return c, d

    def substitution_pc_2(self, c, d):
        keys = []

        for x in range(16):
            ky = ''
            cky = str(bin(c["c" + str(x + 1)])[2:])
            dky = str(bin(d["d" + str(x + 1)])[2:])

            if len(cky) < 28:
                for y in range(28 - len(cky)):
                    cky = '0' + cky

            if len(dky) < 28:
                for y in range(28 - len(dky)):
                    dky = '0' + dky
            cdky = cky + dky

            for pc in self.pc_2:
                ky += cdky[int(pc) - 1]  # -1 because the array index starts at 0 but the sub box numbers start at 1
            keys.append(int(ky, 2))

        return keys

    @staticmethod
    def print_keys(kys):
        for k in range(0, len(kys)):
            print("K" + str(k + 1) + " = " + str(bin(kys[k])[2:].zfill(48)))

    @staticmethod
    def create_ascii_array(m):
        """ Create an array of the ASCII base 10 representation of each character in the plain text message."""

        array = bytearray()
        for ch in m:
            array.append(ord(ch))
        return array

    @staticmethod
    def pad_message(array):
        """ Add '0D0A' to the end of the message indicates that the message has finished and everything after this is
        padding. Carriage return: '0D' (13 ASCII), line feed: '0A' (10 ASCII). If required pad the message array with
        zeros until it is a multiple of 8. """

        print("Original length of message array: ", len(array))
        array.append(13)
        array.append(10)
        for x in range(0, 8 - (len(array) % 8)):
            array.append(0)
        print("Length of message array after padding: ", len(array))
        return array


    def f(self, r, k):

        e_bit = ""
        # print("r", bin(r)[2:].zfill(32))
        for s in self.e_bit_table:
            e_bit += bin(r)[2:].zfill(32)[int(s) - 1]

        xored = int(e_bit, 2) ^ k

        op = ""
        for l in range(0, 8):
            bit6 = bin(xored)[2:].zfill(48)[(l*6):(l*6)+6]
            row = bit6[0] + bit6[5]
            col = bit6[1] + bit6[2] + bit6[3] + bit6[4]
            op += str(bin(int(self.__sbox[l][(int(row, 2) * 16) + int(col, 2)]))[2:].zfill(4))

        op2 = ""
        for p in range(0, len(self.p_table)):
            op2 += op[int(self.p_table[p])-1]

        return int(op2, 2)

    @staticmethod
    def convert_byte_to_bin_str(block):
        i = ""
        for b in block:
            i += str(bin(b)[2:].zfill(8))
        return i

    @staticmethod
    def substitution(array, bin_str):
        sub = ""
        for i in array:
            sub += bin_str[int(i)-1]
        return sub

    def encrypt(self, array, kys):

        encrypted_message = ""

        # split the message into 64bit blocks
        for x in range(0, len(array), 8):
            # print("\n", x)
            bit64_binary_string = ""
            bit64 = array[x:x+8]
            # print(bit64)

            # convert the 8 bytes to a binary string
            bit64_binary_string += self.convert_byte_to_bin_str(bit64)


            # initial_permutation (ip) substitution
            initial_permutation = self.substitution(self.ip, bit64_binary_string)


            # Divide the permuted block IP into a left and right half of 32 bits.
            ln = 0
            rn = 0
            ln_minus_1 = int(initial_permutation[:32], 2)
            rn_minus_1 = int(initial_permutation[32:], 2)

            print("ln", ln_minus_1, ":", initial_permutation[:32])
            print("rn", rn_minus_1, ":", initial_permutation[32:])


            # 16 iterations of: Ln = Rn-1, Rn = Ln-1 + f(Rn-1,Kn)
            for y in range(0, 16):
                ln = rn_minus_1
                rn = ln_minus_1 ^ self.f(rn_minus_1, kys[y])
                ln_minus_1 = ln
                rn_minus_1 = rn

            bit64 = bin(rn)[2:].zfill(32) + bin(ln)[2:].zfill(32)

            final_block = ""
            for p in range(0, 64):
                final_block += bit64[int(initial_permutation[p])-1]

            encrypted_message += final_block
        return encrypted_message

    def hex_encryption(self, encrypted_message):
        hex_encryption = ""
        for x in range(0, len(encrypted_message), 4):
            # print(encrypted_message[x:x+4])
            # print(int(encrypted_message[x:x + 4], 2))
            t = int(encrypted_message[x:x + 4], 2)
            if t > 9:
                hex_encryption += chr(t + 55)
            else:
                hex_encryption += str(t)
        return hex_encryption

    def generate_keys(self, k):
        self.set_key(k)
        ck, dk = self.split_key(self.substitution_pc_1(self.convert_to_hex(self.get_key())))
        cx, dx = self.gen_key_blocks(ck, dk)
        keys = self.substitution_pc_2(cx, dx)
        # self.print_keys(keys)
        return keys

    def encrypt_message(self, message, keys):
        self.set_message(message)

        # print("\nmessage before:", message)
        bytearray = self.create_ascii_array(self.message)
        # print("bytearray:", bytearray)

        # print('\nASCII array length:', len(bytearray), "type:", type(bytearray))
        # for x in bytearray:
            # print(chr(x), ":", x, ":", bin(x)[2:].zfill(8))
        # print("")

        padded_bytearray = self.pad_message(bytearray)
        # print('\nPadded bytearray length:', len(padded_bytearray), "type:", type(padded_bytearray))

        t3 = self.encrypt(padded_bytearray, keys)
        # print('\nEncrypt bytearray length:')

        t4 = self.hex_encryption(t3)
        return padded_bytearray, t3, t4


def main():

    d = DataEncryptionSystem()
    keys = d.generate_keys("133457799BBCDFF1")
    e2, e3, e4 = d.encrypt_message("0123456789ABCDEF", keys)
    print("e2:", e2)
    print("e3:", e3)
    print("e4:", e4)


if __name__ == "__main__":
    main()