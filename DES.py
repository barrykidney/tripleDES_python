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

    def encrypt(self, message, kys, decrypt):
        """Function f operates on two blocks: a data block of 32 bits (rn_minus1) and a key (Kn) of 48 bits to produce
        a block of 32 bits.

        Args:
            message: The n minus one permutation of the right hand side of the message block.
            kys: The nth iteration of the key.
            decrypt: A boolean to set if the message is to be encrypted or decrypted.

        Returns:
            A block of 32 bits.
        """

        d = 15 if decrypt else 0

        bin_encryption = ""
        # split the message into 64bit blocks
        for x in range(0, len(message), 64):
            bit64 = message[x:x+64]

            # initial_permutation (ip) substitution
            initial_permutation = substitution(self.ip, bit64)

            # Divide the permuted block IP into a left and right half of 32 bits.
            ln, rn = 0, 0
            ln_minus_1 = int(initial_permutation[:32], 2)
            rn_minus_1 = int(initial_permutation[32:], 2)

            # 16 iterations of: Ln = Rn-1, Rn = Ln-1 + f(Rn-1,Kn)
            for y in range(0, 16):
                ln = rn_minus_1
                rn = ln_minus_1 ^ (f(rn_minus_1, kys[abs(d - y)], self.e_bit_table, self.__sbox, self.p_table))
                ln_minus_1 = ln
                rn_minus_1 = rn

            bit64 = bin(rn)[2:].zfill(32) + bin(ln)[2:].zfill(32)
            bin_encryption += substitution(self.ip_1, bit64)

        hex_translation = self.bin_to_hex(bin_encryption)
        return bin_encryption, hex_translation

    @staticmethod
    def hex_to_bin(hex_message):
        """Function to convert a hexadecimal message to a binary message.

        Args:
            hex_message: A String containing a message in hexadecimal format.

        Returns:
            A String containing the input message in binary format.
        """

        bin_message = ""

        for x in range(0, len(hex_message)):
            if ord(hex_message[x]) > 57:
                bin_message += str(bin(ord(hex_message[x]) - 55)[2:].zfill(4))
            else:
                bin_message += str(bin(ord(hex_message[x]) - 48)[2:].zfill(4))
        return bin_message

    @staticmethod
    def bin_to_hex(bin_message):
        """Function to convert a binary message to a hexadecimal message.

        Args:
            bin_message: A String containing a message in binary format.

        Returns:
            A String containing the input message in hexadecimal format.
        """

        hex_message = ""
        for x in range(0, len(bin_message), 4):
            t = int(bin_message[x:x + 4], 2)
            if t > 9:
                hex_message += chr(t + 55)
            else:
                hex_message += str(t)
        return hex_message

    def prepare_message(self, m):
        byte_array = self.create_ascii_array(m)
        padded_byte_array = self.pad_message(byte_array)
        bit64_binary_string = self.convert_64bit_byte_array_to_bin_str(padded_byte_array)
        return bit64_binary_string

    @staticmethod
    def remove_padding(encrypted_message):

        byte_arr = bytearray()
        for z in range(0, len(encrypted_message), 8):
            b = encrypted_message[z:z + 8]
            byte_arr.append(int(b, 2))

        remove = 0
        for b in range(len(byte_arr)-1, -1, -1):
            if byte_arr[b] == 0:
                remove += 1
            elif byte_arr[b] == 10:
                remove += 1
            elif byte_arr[b] == 13:
                remove += 1
                break
        byte_arr = byte_arr[:len(byte_arr)-remove]
        return byte_arr

    def encrypt_des(self, message, key):

        print("\nEncrypting with DES...")
        self.set_key(key)
        keys = generate_keys(key, self.pc_1, self.pc_2, self.shifts)
        prepared_message = self.prepare_message(message)
        binary_encryption, hex_translation = self.encrypt(prepared_message, keys, False)

        return binary_encryption, hex_translation

    def decrypt_des(self, m, key):

        print("\nDecrypting with DES...")
        self.set_key(key)
        keys = generate_keys(key, self.pc_1, self.pc_2, self.shifts)
        encrypted_message, hex_translation = self.encrypt(m, keys, True)

        byte_arr = self.remove_padding(encrypted_message)
        output = byte_arr.decode("ascii")
        return output

    def encrypt_triple_des(self, m, key1, key2, key3):

        print("\nEncrypting with triple DES...")
        self.set_key(key1)
        keys1 = generate_keys(key1, self.pc_1, self.pc_2, self.shifts)

        self.set_key(key2)
        keys2 = generate_keys(key2, self.pc_1, self.pc_2, self.shifts)

        self.set_key(key3)
        keys3 = generate_keys(key3, self.pc_1, self.pc_2, self.shifts)

        prepared_message = self.prepare_message(m)

        binary_encryption1, hex_translation1 = self.encrypt(prepared_message, keys1, False)
        binary_encryption2, hex_translation2 = self.encrypt(binary_encryption1, keys2, True)
        binary_encryption3, hex_translation3 = self.encrypt(binary_encryption2, keys3, False)

        return binary_encryption3, hex_translation3

    def decrypt_triple_des(self, m, key1, key2, key3):

        print("\nDecrypting with triple DES...")
        self.set_key(key1)
        keys1 = generate_keys(key1, self.pc_1, self.pc_2, self.shifts)

        self.set_key(key2)
        keys2 = generate_keys(key2, self.pc_1, self.pc_2, self.shifts)

        self.set_key(key3)
        keys3 = generate_keys(key3, self.pc_1, self.pc_2, self.shifts)

        binary_decryption1, hex_translation1 = self.encrypt(m, keys3, True)
        binary_decryption2, hex_translation2 = self.encrypt(binary_decryption1, keys2, False)
        binary_decryption3, hex_translation3 = self.encrypt(binary_decryption2, keys1, True)

        byte_arr = self.remove_padding(binary_decryption3)
        output = byte_arr.decode("ascii")
        return output


def main():

    print("\n\nDES")
    # file = open("test.txt", "r")
    # message = file.read()
    # file.close()
    message = "Your lips are smoother than vaseline"
    key = "0E329232EA6D0D73"

    print("\nOriginal message:\n", message, sep='')

    d = DataEncryptionSystem()
    encrypted_message_binary, encrypted_message_hex = d.encrypt_des(message, key)
    print("Encrypted:", encrypted_message_hex)
    print("Expected:  C0999FDDE378D7ED727DA00BCA5A84EE47F269A4D64381909DD52F78F5358499828AC9B453E0E653")

    unencrypted_message = d.decrypt_des(encrypted_message_binary, key)
    print("Unencrypted:", unencrypted_message)
    print("Expected:   ", message)


    print("\n\nTriple DES")
    message = "Your lips are smoother than vaseline"
    key1 = "0E329232EA6D0D73"
    key2 = "A025A2397EC48F99"
    key3 = "0123456789ABCDEF"

    print("\nOriginal message:\n", message, sep='')

    d = DataEncryptionSystem()
    encrypted_message_binary, encrypted_message_hex = d.encrypt_triple_des(message, key1, key2, key3)
    print("Encrypted:", encrypted_message_hex)

    unencrypted_message = d.decrypt_triple_des(encrypted_message_binary, key1, key2, key3)
    print("Unencrypted:", unencrypted_message)
    print("Expected:   ", message)



if __name__ == "__main__":
    main()
