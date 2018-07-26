import math


def remove_first_bit(numb):
    numb -= int(math.pow(2, len(bin(numb)[2:]) - 1))
    return numb


def split_key(k):
    c = {"c0": int(k[:28], 2)}
    d = {"d0": int(k[28:], 2)}
    # print("c0: ", bin(int(k[:28], 2))[2:].zfill(28))
    # print("d0: ", bin(int(k[28:], 2))[2:].zfill(28))
    return c, d


def substitution(sub_array, msg):
    sub = ""
    for idx in sub_array:
        sub += msg[int(idx)-1]
    return sub


def substitution_pc_2(c, d, pc_2):
    keys = []

    for x in range(16):
        ky = ''
        cky = str(bin(c["c" + str(x + 1)])[2:].zfill(28))
        dky = str(bin(d["d" + str(x + 1)])[2:].zfill(28))
        cdky = cky + dky

        for pc in pc_2:
            ky += cdky[int(pc) - 1]  # -1 because the array index starts at 0 but the sub box numbers start at 1
        keys.append(int(ky, 2))

    return keys


def convert_string_to_hex(str_arg):
    """ Convert each char to its ASCII base 10 number using ord() then range the results between 0 and 15. Convert
    that number to binary using bin() then drop the leading '0b'. example: b -> B -> 66 -> 11 -> 0b1011 -> 1011.
    If a char conversion has less than 4 bits pad with zeros. Finally concatenate each to the string 'k'."""

    if len(str_arg) < 1:
        return "Error: string is empty."

    k = ""
    for ch in str_arg:
        a = ord(ch.upper())
        if 47 < a < 58:
            ch_binary = bin(a - 48)[2:]
        elif 64 < a < 71:
            ch_binary = bin(a - 55)[2:]
        else:
            return "Error: character " + str_arg(ch) + " in key is out of range."
        while len(ch_binary) < 4:
            ch_binary = '0' + ch_binary
        k += ch_binary
    return k


def gen_key_blocks(c, d, shifts):
    for x in range(len(shifts)):
        sft = int(shifts[x])
        cf = c["c" + str(x)]
        df = d["d" + str(x)]

        while sft > 0:
            cf = cf << 1
            if len(bin(cf)[2:]) > 28:
                cf += 1
                cf = remove_first_bit(cf)

            df = df << 1
            if len(bin(df)[2:]) > 28:
                df += 1
                df = remove_first_bit(df)
            sft -= 1

        c["c{0}".format(x + 1)] = cf
        d["d{0}".format(x + 1)] = df

    return c, d


def generate_keys(k, pc_1, pc_2, shifts):
    """Function f operates on two blocks: a data block of 32 bits (rn_minus1) and a key (Kn) of 48 bits to produce a
    block of 32 bits.

    Args:
        k: The n minus one permutation of the right hand side of the message block.
        pc_1: The nth iteration of the key.
        pc_2: The E-bit selection table.
        shifts: A array of s boxes.

    Returns:
        A block of 32 bits.

    """

    ck, dk = split_key(substitution(pc_1, convert_string_to_hex(k)))
    cx, dx = gen_key_blocks(ck, dk, shifts)
    keys = substitution_pc_2(cx, dx, pc_2)
    # self.print_keys(keys)
    return keys
