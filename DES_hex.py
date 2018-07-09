# reference: http://page.math.tu-berlin.de/~kant/teaching/hess/krypto-ws2006/des.htm

import math

class DES:

    def __init__(self):
        pass

    def remove_first_bit(numb):

        numb -= int(math.pow(2, len(bin(numb)[2:]) - 1))
        return numb


    def f(r, k, ebt, sb, pt):

        e_bit = ""
        for s in ebt:
            e_bit += bin(r)[2:].zfill(32)[s - 1]

        xored = int(e_bit, 2) ^ k

        op = ""
        for l in range(0, 8):
            bit6 = bin(xored)[2:].zfill(48)[(l*6):(l*6)+6]
            row = bit6[0] + bit6[5]
            col = bit6[1] + bit6[2] + bit6[3] + bit6[4]
            op += str(bin(sb[l][(int(row, 2) * 16) + int(col, 2)])[2:].zfill(4))

        op2 = ""
        for p in range(0, len(pt)):
            op2 += op[(pt[p]-1)]

        return int(op2, 2)


    pc_1 = [57, 49, 41, 33, 25, 17, 9,
            1, 58, 50, 42, 34, 26, 18,
            10, 2, 59, 51, 43, 35, 27,
            19, 11, 3, 60, 52, 44, 36,
            63, 55, 47, 39, 31, 23, 15,
            7, 62, 54, 46, 38, 30, 22,
            14, 6, 61, 53, 45, 37, 29,
            21, 13, 5, 28, 20, 12, 4]


    shifts = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]


    pc_2 = [14, 17, 11, 24, 1, 5,
            3, 28, 15, 6, 21, 10,
            23, 19, 12, 4, 26, 8,
            16, 7, 27, 20, 13, 2,
            41, 52, 31, 37, 47, 55,
            30, 40, 51, 45, 33, 48,
            44, 49, 39, 56, 34, 53,
            46, 42, 50, 36, 29, 32]


    ip = [58, 50, 42, 34, 26, 18, 10, 2,
          60, 52, 44, 36, 28, 20, 12, 4,
          62, 54, 46, 38, 30, 22, 14, 6,
          64, 56, 48, 40, 32, 24, 16, 8,
          57, 49, 41, 33, 25, 17, 9, 1,
          59, 51, 43, 35, 27, 19, 11, 3,
          61, 53, 45, 37, 29, 21, 13, 5,
          63, 55, 47, 39, 31, 23, 15, 7]


    e_bit_table = [32, 1, 2, 3, 4, 5,
                   4, 5, 6, 7, 8, 9,
                   8, 9, 10, 11, 12, 13,
                   12, 13, 14, 15, 16, 17,
                   16, 17, 18, 19, 20, 21,
                   20, 21, 22, 23, 24, 25,
                   24, 25, 26, 27, 28, 29,
                   28, 29, 30, 31, 32, 1]


    __sbox = [[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7, 0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8,
               4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0, 15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13],
              [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10, 3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5,
               0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15, 13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9],
              [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8, 13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1,
               13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7, 1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12],
              [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15, 13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9,
               10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4, 3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14],
              [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9, 14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6,
               4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14, 11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3],
              [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11, 10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8,
               9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6, 4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13],
              [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1, 13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6,
               1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2, 6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12],
              [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7, 1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2,
               7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8, 2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]


    p_table = [16, 7, 20, 21,
               29, 12, 28, 17,
               1, 15, 23, 26,
               5, 18, 31, 10,
               2, 8, 24, 14,
               32, 27,  3, 9,
               19, 13, 30, 6,
               22, 11, 4, 25]


    ip_1 = [40, 8, 48, 16, 56, 24, 64, 32,
            39, 7, 47, 15, 55, 23, 63, 31,
            38, 6, 46, 14, 54, 22, 62, 30,
            37, 5, 45, 13, 53, 21, 61, 29,
            36, 4, 44, 12, 52, 20, 60, 28,
            35, 3, 43, 11, 51, 19, 59, 27,
            34, 2, 42, 10, 50, 18, 58, 26,
            33, 1, 41, 9, 49, 17, 57, 25]


    # message = "The DES (Data Encryption Standard) algorithm is the most widely used encryption algorithm in the \n" \
    #           "world. For many years, and among many people, 'secret code making' and DES have been synonymous. \n" \
    #           "And despite the recent coup by the Electronic Frontier Foundation in creating a $220,000 machine \n" \
    #           "to crack DES-encrypted messages, DES will live on in government and banking for years to come \n" \
    #           "through a life-extending version called 'triple-DES'. How does DES work? This article explains the \n" \
    #           "various steps involved in DES-encryption, illustrating each step by means of a simple example. \n" \
    #           "Since the creation of DES, many other algorithms (recipes for changing data) have emerged which are \n" \
    #           "based on design principles similar to DES. Once you understand the basic transformations that take \n" \
    #           "place in DES, you will find it easy to follow the steps involved in these more recent algorithms. \n" \
    #           "But first a bit of history of how DES came about is appropriate, as well as a look toward the future."

    # message = "The DES (Data Encryption Standard) algorithm is the most widely used encryption algorithm in the world."

    message = "0123456789ABCDEF"

    key = "133457799BBCDFF1"

    # key = '8s3H527j'

    """ Convert each char to its ASCII base 10 number using ord() then convert that number to binary using bin()
        then drop the leading '0b'. example: 8 -> 56 -> 0b111000 -> 111000. If a char conversion has less than 8 bits
        pad with zeros. Finally concatenate each bite (8 bits) to the string 'k'."""

    k = ""
    for ch in key:
        if ch.isdigit():
            sch = bin(int(ch))[2:]
        elif ch.isalpha() and 64 < ord(ch.upper()) < 71:
            sch = bin(ord(ch.upper())-55)[2:]
        while len(sch) < 4:
            sch = '0' + sch
        k += sch


    # for ch in key:
    #     sch = bin(ord(ch))[2:]
    #     while len(sch) < 8:
    #         sch = '0' + sch
    #     k += sch

    print("Plaintext key: ", key)
    print("Binary key: ", k)

    """ Create 16 sub-keys, each of which is 48-bits long. The 64-bit key is permuted according
        to the following table, PC-1. Since the first entry in the table is '57', this means that
        the 57th bit of the original key K becomes the first bit of the permuted key K+. The 49th
        bit of the original key becomes the second bit of the permuted key. The 4th bit of the original
        key is the last bit of the permuted key. Note only 56 bits of the original key appear in the
        permuted key."""

    """ Generate 56 bit sub key using the values in pc_1 as indexes in the original key."""
    sub_key = ""
    for idx in pc_1:
        sub_key += k[idx]

    """Next, split this key into left and right halves, C0 and D0, where each half has 28 bits."""

    c = {"c0": int(sub_key[:28], 2)}
    d = {"d0": int(sub_key[28:], 2)}
    print("\nkey: ", k)
    print("sub_key: ", sub_key)
    print("")
    print("c0: ", bin(int(sub_key[:28], 2))[2:].zfill(28))
    print("d0: ", bin(int(sub_key[28:], 2))[2:].zfill(28))

    """ With C0 and D0 defined, we now create sixteen blocks Cn and Dn, 1<=n<=16. Each pair of blocks Cn and Dn is 
        formed from the previous pair Cn-1 and Dn-1, respectively, for n = 1, 2, ..., 16, using the following schedule 
        of 'left shifts' of the previous block. To do a left shift, move each bit one place to the left, except for the 
        first bit, which is cycled to the end of the block. """

    for x in range(len(shifts)):
        sft = shifts[x]
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

    print("")
    print("c dictionary: ", c)
    print("d dictionary: ", d)

    """ We now form the keys Kn, for 1<=n<=16, by applying the following permutation table to each of the concatenated 
        pairs CnDn. Each pair has 56 bits, but PC-2 only uses 48 of these. """

    """ We now form the keys Kn, for 1<=n<=16, by applying the following permutation table to each of the concatenated 
        pairs CnDn. Each pair has 56 bits, but PC-2 only uses 48 of these. Therefore, the first bit of Kn is the 14th 
        bit of CnDn, the second bit the 17th, and so on, ending with the 48th bit of Kn being the 32th bit of CnDn. """

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

        for pc in pc_2:
            ky += cdky[pc-1]
        keys.append(int(ky, 2))

    for k in range(0, len(keys)):
        print("K" + str(k+1) + " = " + str(bin(keys[k])[2:].zfill(48)))

    """ Create an array of the ASCII base 10 representation of each character in the plain text message."""

    m_array = bytearray()
    for ch in message:
        m_array.append(ord(ch))

    """ Add '0D0A' to the end of the message indicates that the message has finished and everything after this is
        padding. Carriage return: '0D' (13 ASCII), line feed: '0A' (10 ASCII). """
    m_array.append(13)
    m_array.append(10)

    print("Original length of message array: ", len(m_array))

    """ If required pad the message array with zeros until it is a multiple of 8. """
    for x in range(0, 8 - (len(m_array) % 8)):
        m_array.append(0)

    print("Length of message array after padding: ", len(m_array))

    """ DES operates on the 64-bit blocks using key sizes of 56- bits. The keys are actually stored as being 64 bits 
        long, but every 8th bit in the key is not used (i.e. bits numbered 8, 16, 24, 32, 40, 48, 56, and 64). However, 
        we will nevertheless number the bits from 1 - 64, going left to right, in the following calculations. But, as 
        you will see, the eight bits just mentioned get eliminated when we create sub-keys. """

    """ Split the message into 64 bit sections and then split these into a left and a right 32 bit sections. """











    encrypted_message = ""

    for x in range(0, len(m_array), 8):
        ip_m = ""
        bit64 = m_array[x:x+8]

        for y in bit64:
            ip_m += str(bin(y)[2:].zfill(8))

        ln = 0
        rn = 0
        ln_minus_1 = int(ip_m[:32], 2)
        rn_minus_1 = int(ip_m[32:], 2)

        for y in range(0, 16):
            ln = rn_minus_1
            rn = ln_minus_1 ^ f(rn_minus_1, keys[y], e_bit_table, __sbox, p_table)
            ln_minus_1 = ln
            rn_minus_1 = rn

        bit64 = bin(rn)[2:].zfill(32) + bin(ln)[2:].zfill(32)

        final_block = ""
        for p in range(0, 64):
            final_block += bit64[(ip_1[p]-1)]

        encrypted_message += final_block

    hex_encryption = ""
    for x in range(0, len(encrypted_message), 4):
        # print(encrypted_message[x:x+4])
        # print(int(encrypted_message[x:x + 4], 2))

        t = int(encrypted_message[x:x + 4], 2)

        if t > 9:
            hex_encryption += chr(t + 55)
        else:
            hex_encryption += str(t)

    print("\nOriginal message:\n" + message)
    print("\nEncrypted message (Hex):\n" + hex_encryption)
    print("\nEncrypted message (Binary):\n" + encrypted_message)
    print("Plaintext message length (ASCII):", len(message))
    print("Encrypted message length (Hex):", len(hex_encryption))
    print("Encrypted message length (Binary):", len(encrypted_message))
    print("Ratio: ", len(encrypted_message) / len(message), ": 1")