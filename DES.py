from f import f
from Generate_keys import generate_keys
from Generate_keys import substitution
from csv_read import read_csv


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
    file_path = ""
    filename = ""

    def __init__(self):
        self.file_path = "files/"
        self.test_keys = read_csv(self.file_path, "test_keys.csv")
        self.shifts = read_csv(self.file_path, "shifts.csv")
        self.pc_1 = read_csv(self.file_path, "pc_1.csv")
        self.pc_2 = read_csv(self.file_path, "pc_2.csv")
        self.ip = read_csv(self.file_path, "ip.csv")
        self.e_bit_table = read_csv(self.file_path, "e_bit_table.csv")
        self.p_table = read_csv(self.file_path, "p_table.csv")
        self.ip_1 = read_csv(self.file_path, "ip_1.csv")

        temp_box = read_csv(self.file_path, "__sbox.csv")
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
    def print_keys(kys, test_kys):
        for k in range(0, len(kys)):
            print("K" + str(k + 1) + " = " + str(bin(kys[k])[2:].zfill(48)))
            print("K" + str(k + 1) + " = " + test_kys[k])

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

        array.append(13)
        array.append(10)
        for x in range(0, 8 - (len(array) % 8)):
            array.append(0)
        return array

    @staticmethod
    def convert_64bit_byte_array_to_bin_str(block):
        i = ""
        for b in block:
            i += str(bin(b)[2:].zfill(8))
        return i

    # def encrypt(self, array, kys):
    def encrypt(self, message, kys):

        # self.set_message(message)
        byte_array = self.create_ascii_array(message)
        padded_byte_array = self.pad_message(byte_array)

        encrypted_message = ""

        # split the message into 64bit blocks
        for x in range(0, len(padded_byte_array), 8):
            bit64_binary_string = ""
            bit64 = padded_byte_array[x:x+8]

            # convert the 8 bytes to a binary string
            bit64_binary_string += self.convert_64bit_byte_array_to_bin_str(bit64)

            # initial_permutation (ip) substitution
            initial_permutation = substitution(self.ip, bit64_binary_string)

            # Divide the permuted block IP into a left and right half of 32 bits.
            ln = 0
            rn = 0
            ln_minus_1 = int(initial_permutation[:32], 2)
            rn_minus_1 = int(initial_permutation[32:], 2)

            # 16 iterations of: Ln = Rn-1, Rn = Ln-1 + f(Rn-1,Kn)
            for y in range(0, 16):
                ln = rn_minus_1
                rn = ln_minus_1 ^ (f(rn_minus_1, kys[y], self.e_bit_table, self.__sbox, self.p_table))
                ln_minus_1 = ln
                rn_minus_1 = rn

            bit64 = bin(rn)[2:].zfill(32) + bin(ln)[2:].zfill(32)
            encrypted_message += substitution(self.ip_1, bit64)

        hex_translation = self.hex_encryption(encrypted_message)
        return encrypted_message, hex_translation

    @staticmethod
    def hex_encryption(encrypted_message):
        hex_encryption = ""
        for x in range(0, len(encrypted_message), 4):
            t = int(encrypted_message[x:x + 4], 2)
            if t > 9:
                hex_encryption += chr(t + 55)
            else:
                hex_encryption += str(t)
        return hex_encryption

    @staticmethod
    def message_hex_encryption(encrypted_message):
        hex_encryption = ""
        for x in encrypted_message:
            hex_encryption += hex(ord(x))[2:]
        return hex_encryption


def main():

    message = "Your lips are smoother than vaseline"
    key = "0E329232EA6D0D73"

    d = DataEncryptionSystem()
    d.set_key(key)
    keys = generate_keys(key, d.pc_1, d.pc_2, d.shifts)
    encrypted_message, hex_translation = d.encrypt(message, keys)

    print("\nMessage:", message)
    print("\nBin output:", encrypted_message)
    print("Hex output:", hex_translation)
    print("Expected:   C0999FDDE378D7ED727DA00BCA5A84EE47F269A4D64381909DD52F78F5358499828AC9B453E0E653")


if __name__ == "__main__":
    main()
