def f(rn_minus1, kn, e_bit_table, __sbox, p_table):
    """Function f operates on two blocks: a data block of 32 bits (rn_minus1) and a key (Kn) of 48 bits to produce a
    block of 32 bits.

    Args:
        rn_minus1: The n minus one permutation of the right hand side of the message block.
        kn: The nth iteration of the key.
        e_bit_table: The E-bit selection table.
        __sbox: A array of s boxes.
        p_table: The permutation table P.

    Returns:
        A block of 32 bits.

    """

    e_bit = ""
    for e in e_bit_table:
        e_bit += bin(rn_minus1)[2:].zfill(32)[int(e) - 1]

    xored = int(e_bit, 2) ^ kn

    op = ""
    for l in range(0, 8):
        bit6 = bin(xored)[2:].zfill(48)[(l * 6):(l * 6) + 6]
        row = bit6[0] + bit6[5]
        col = bit6[1] + bit6[2] + bit6[3] + bit6[4]
        op += str(bin(int(__sbox[l][(int(row, 2) * 16) + int(col, 2)]))[2:].zfill(4))

    op2 = ""
    for p in range(0, len(p_table)):
        op2 += op[int(p_table[p]) - 1]

    return int(op2, 2)