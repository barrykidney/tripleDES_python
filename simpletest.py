# import math
# import re
from f import f
from csv_read import read_csv

# text = "period_1_677278.ssa"
# print(text)
#
# m = re.match(r"period_1_(.*)\.ssa", text)
# print(m.group(1))




data = bytes(b"1")
print(data)
print(bin(int(data, base=16)))

data = bytes(b"9")
print(data)
print(bin(int(data, base=16)))

data = bytes(b"10")
print(data)
print(bin(int(data, base=16)))

data = bytes(b"a")
print(data)
print(bin(int(data, base=16)))

data = bytes(b"15")
print(data)
print(bin(int(data, base=16)))

data = bytes(b"f")
print(data)
print(bin(int(data, base=16)))

data = bytes(b"6f")
print(data)
print(bin(int(data, base=16)))

# data = bytes(b"w")
# print(data)
# print(bin(int(data, base=16)))



encrypted_message = ""

# split the message into 64bit blocks
for x in range(0, len(array), 8):
    print("\n", x)
    bit64_binary_string = ""
    bit64 = array[x:x+8]
    print(bit64)
    for y in bit64:
        print(bin(y)[2:], "", end='')
    print('')





'''
def substitution_X(sub_array, msg):
    s = ""
    for idx in sub_array:
        s += msg[int(idx)]
    return s


def substitution_Y(array, bin_str):
    sub = ""
    for i in array:
        sub += bin_str[int(i) - 1]
    return sub



file_path = "files/"
__sbox = []

pc_1 = read_csv(file_path, "pc_1.csv")
e_bit_table = read_csv(file_path, "e_bit_table.csv")
p_table = read_csv(file_path, "p_table.csv")
temp_box = read_csv(file_path, "__sbox.csv")
for x in range(8):
    __sbox.append([])
    for y in range(64):
        __sbox[x].append(temp_box[(x*64)+y])

K1 = 0b000110110000001011101111111111000111000001110010
R0 = 0b11110000101010101111000010101010

# print(R0, " : ", len(R0))
# print(R0[32-1], R0[1-1], R0[2-1], R0[3-1], R0[4-1], R0[5-1], R0[4-1], R0[5-1], R0[6-1], R0[7-1], R0[8-1], R0[9-1],)
print("outp:", bin(f(R0, K1, e_bit_table, __sbox, p_table))[2:].zfill(32))
print("f   : 00100011010010101010100110111011")
# print("  00100011010010101010100110111011")

# print(bin(ord('B'))[2:])
# print(bin(ord(' ')))



key = ''
for x in pwd:
    y = str(bin(ord(x)))[2:]
    if len(y) < 7:
        y = '0' + y
    key += y

if len(key) > 56:
    key = key[:56]

print(key)
print(len(key))
'''

# data = "ABCD"
# data = data.encode()
#
# print(data)

# pwd = "ABCD"
# b = bytearray()
# b.extend(map(ord, pwd))
#
# print(b)

'''
ch = 'd'
print(bin(ord(ch)))
print(hex(ord(ch)))
print(ord(ch))

key = bytearray([0x1f, 0x00, 0x00, 0x00, 0x08, 0x05])
print(key)

ch = "Hello World"

s = bytearray(b"Hello World")
for c in s: print(c)
s.append(33)
print(s)
# key.append(ord(ch))
# print(key)

print(chr(13))
'''

# f = 15
#
# # 8
#
# # print(int('111', 2))
# print('bin f', bin(f))
#
#
#
# print(int(math.pow(2, len(bin(f)[2:])-1)))
#
# print(bin(f - int(math.pow(2, len(bin(f)[2:])-1))))
#
#
# # ab = bytes(int('00110111', 2)) #55
# ab = 55
# cd = 240
# # cd = bytes(int('11110000', 2))
# print("ab: ", bin(ab)[2:].zfill(8))
# print("cd: ", bin(cd)[2:].zfill(8))
# print("XOR:", bin(ab^cd)[2:])
# #^


'''

def remove_first_bit(numb):

    numb -= int(math.pow(2, len(bin(numb)[2:]) - 1))
    return numb





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





key = "133457799BBCDFF1"

# key = '8s3H527j'

print("Original Hex key (chr): ", len(key), " : ", key)

k = ""
for ch in key:
    if ch.isdigit():
        sch = bin(int(ch))[2:]
    elif ch.isalpha() and 64 < ord(ch.upper()) < 71:
        sch = bin(ord(ch.upper())-55)[2:]
    while len(sch) < 4:
        sch = '0' + sch
    k += sch

print("\nBinary key (4 bit):", len(k), " : ", k)


sub_key = ""
for idx in pc_1:
    sub_key += k[idx]

print("\nKey after pc_1 permutation:", len(sub_key), " : ", sub_key)


c = {"c0": int(sub_key[:28], 2)}
d = {"d0": int(sub_key[28:], 2)}

print("Split into 2 28 bit parts c0 & d0:", bin(c['c0'])[2:].zfill(28) + bin(d['d0'])[2:].zfill(28))






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

'''


# from DES import data_encryption_system
#
#
# d = data_encryption_system()
# d.set_key("0")
# print(d.convert_to_ascii())
# d.set_key("1")
# print(d.convert_to_ascii())
# d.set_key("2")
# print(d.convert_to_ascii())
# d.set_key("3")
# print(d.convert_to_ascii())
# d.set_key("4")
# print(d.convert_to_ascii())
# d.set_key("5")
# print(d.convert_to_ascii())
# d.set_key("6")
# print(d.convert_to_ascii())
# d.set_key("7")
# print(d.convert_to_ascii())
# d.set_key("8")
# print(d.convert_to_ascii())
# d.set_key("9")
# print(d.convert_to_ascii())
# d.set_key("a")
# print(d.convert_to_ascii())
# d.set_key("b")
# print(d.convert_to_ascii())
# d.set_key("c")
# print(d.convert_to_ascii())
# d.set_key("d")
# print(d.convert_to_ascii())
# d.set_key("e")
# print(d.convert_to_ascii())
# d.set_key("f")
# print(d.convert_to_ascii())
# d.set_key("g")
# print(d.convert_to_ascii())

# 58 59 60 61 62 63 64
# c = ['a', 'b', 'c', 'd', 'e', 'f']
# g = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'l', '*', ' ']
# i = [':', ';', '<', '=', '>', '?', '@']
# s = '012356789abcdef'
#
# for ch in s:
#
#     # print(ch.upper())
#     ascii = ord(ch.upper())
#     # print(ascii)
#     if 47 < ascii < 58:
#         ch_binary = ord(ch.upper()) - 48
#         print(ch_binary)
#     elif 64 < ascii < 71:
#         ch_binary = ord(ch.upper()) - 55
#         print(ch_binary)
#     else:
#         print("out of range!!!!!")
#     # ch_binary = bin(ord(ch.upper()) - 55)
#     # ch_binary = ch_binary[2:]
#     # print(ch_binary)
# print()
# # 64 < ord(ch.upper()) < 71
