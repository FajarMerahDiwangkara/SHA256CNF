import string
import sys
from typing import List, Union, Tuple
import ConjunctiveNormalForm
from ConjunctiveNormalForm import ConjunctiveNormalForm


def bytearray_to_bitstring(x: bytearray) -> str:
    byte_length = len(x)
    bit_length = byte_length * 8
    return (bin(int(x.hex(), 16))[2:]).zfill(bit_length)


def bitstring_to_bytearray_zfill(x: str) -> bytearray:
    if (len(x) % 4) != 0:
        x = x.zfill(len(x) + (len(x) % 4))
    if not isinstance(x, str):
        raise ValueError("Error: was expecting x to be str, got %s" % type(x))
    return bytearray.fromhex(
        '{:0{}X}'.format(int(x, 2), len(x) // 4)
    )


def bitstring_to_bytearray_correct_size(x: str) -> bytearray:
    if (len(x) % 4) != 0:
        raise ValueError("Error: bitstring length is not a multiple of four")
    else:
        return bitstring_to_bytearray_zfill(x)


K = [
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
    0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
]


def generate_hash(message: bytearray) -> bytes:
    """Return a SHA-256 hash from the message passed.
    The argument should be bytearray"""
    satisfiability_result_formula: ConjunctiveNormalForm = ConjunctiveNormalForm()
    if not isinstance(message, bytearray):
        raise TypeError
    message = bytearray_to_bitstring(message)
    # Padding
    message_length = len(message)
    satisfiability_message: List[ConjunctiveNormalForm.Variable] = [ConjunctiveNormalForm.Variable() for i in range(message_length)]
    if message_length != len(message):
        raise ValueError("Error: message_length and len(message) is not equal")
    for i in range(message_length):
        if message[i] == "0":
            satisfiability_message[i].set_truth_value(False)
        elif message[i] == "1":
            satisfiability_message[i].set_truth_value(True)
        else:
            raise ValueError("Error: message[i] contain symbol other than 0 and 1")
    x80_bitstring = bytearray_to_bitstring(bytearray.fromhex("80"))
    satisfiability_x80: List[ConjunctiveNormalForm.Variable] = []
    for x80_bit in x80_bitstring:
        satisfiability_variable_to_append = ConjunctiveNormalForm.Variable()
        if x80_bit == "0":
            satisfiability_variable_to_append.set_truth_value(False)
        elif x80_bit == "1":
            satisfiability_variable_to_append.set_truth_value(True)
        else:
            raise ValueError("Error: x80_bit contain symbol other than 0 and 1")
        satisfiability_x80.append(satisfiability_variable_to_append)
    message += x80_bitstring
    satisfiability_message.extend(satisfiability_x80)
    while (len(message) + 64) % 512 != 0:
        x00_bitstring = bytearray_to_bitstring(bytearray.fromhex("00"))
        message += x00_bitstring
    message_length_bitstring = bytearray_to_bitstring(bytearray(message_length.to_bytes(8, 'big')))
    if len(message_length_bitstring) != 8*8:
        raise ValueError("Error: len(message_length_bitstring) != 64 bit, got ", len(message_length_bitstring), " bit")
    message += message_length_bitstring  # pad to 8 bytes or 64 bits
    assert (len(message)) % 512 == 0, "Padding did not complete properly!"

    # Parsing
    blocks = []  # contains 512-bit chunks of message
    for i in range(0, message_length, 512):
        blocks.append(message[i:i + 512])

    # Setting Initial Hash Value
    h0 = 0x6a09e667
    h0 = hex(h0)[2:]
    h0 = h0.zfill(len(h0) + (len(h0) % 2))
    h0 = bytearray_to_bitstring(bytearray.fromhex(h0)).zfill(32)
    h1 = 0xbb67ae85
    h1 = hex(h1)[2:]
    h1 = h1.zfill(len(h1) + (len(h1) % 2))
    h1 = bytearray_to_bitstring(bytearray.fromhex(h1)).zfill(32)
    h2 = 0x3c6ef372
    h2 = hex(h2)[2:]
    h2 = h2.zfill(len(h2) + (len(h2) % 2))
    h2 = bytearray_to_bitstring(bytearray.fromhex(h2)).zfill(32)
    h3 = 0xa54ff53a
    h3 = hex(h3)[2:]
    h3 = h3.zfill(len(h3) + (len(h3) % 2))
    h3 = bytearray_to_bitstring(bytearray.fromhex(h3)).zfill(32)
    h4 = 0x510e527f
    h4 = hex(h4)[2:]
    h4 = h4.zfill(len(h4) + (len(h4) % 2))
    h4 = bytearray_to_bitstring(bytearray.fromhex(h4)).zfill(32)
    h5 = 0x9b05688c
    h5 = hex(h5)[2:]
    h5 = h5.zfill(len(h5) + (len(h5) % 2))
    h5 = bytearray_to_bitstring(bytearray.fromhex(h5)).zfill(32)
    h6 = 0x1f83d9ab
    h6 = hex(h6)[2:]
    h6 = h6.zfill(len(h6) + (len(h6) % 2))
    h6 = bytearray_to_bitstring(bytearray.fromhex(h6)).zfill(32)
    h7 = 0x5be0cd19
    h7 = hex(h7)[2:]
    h7 = h7.zfill(len(h7) + (len(h7) % 2))
    h7 = bytearray_to_bitstring(bytearray.fromhex(h7)).zfill(32)
    # SHA-256 Hash Computation
    for message_block in blocks:
        # Prepare message schedule
        message_schedule = []
        for t in range(0, 64):
            if t <= 15:
                # adds the t'th 32 bit word of the block,
                # starting from leftmost word
                # 4 bytes at a time
                message_schedule.append(message_block[t * 4 * 8:(t * 4 * 8) + 4 * 8])
            else:
                term1 = _sigma1_binary_correct_size(message_schedule[t - 2])
                term2 = message_schedule[t - 7]
                term3 = _sigma0_binary_correct_size(message_schedule[t - 15])
                term4 = message_schedule[t - 16]

                schedule = binary_addition_zfill_multiple(
                    [term1, term2, term3 , term4], min_bitlength=32, max_bitlength=32)
                message_schedule.append(schedule)
        assert len(message_schedule) == 64
        # Initialize working variables
        a = h0
        b = h1
        c = h2
        d = h3
        e = h4
        f = h5
        g = h6
        h = h7
        K_binary = []
        for hex_number in K:
            to_append = hex(hex_number)[2:]
            to_append = to_append.zfill(len(to_append) + (len(to_append) % 2))
            to_append = bytearray_to_bitstring(bytearray.fromhex(to_append)).zfill(32)
            K_binary.append(to_append)
        # Iterate for t=0 to 63
        for t in range(64):
            t1 = binary_addition_zfill_multiple(
                [h, _capsigma1_binary(e), _ch_binary_correct_size(e, f, g),
                 K_binary[t], message_schedule[t]], min_bitlength=32, max_bitlength=32)

            t2 = binary_addition_zfill_multiple(
                [_capsigma0_binary(a), _maj_binary_correct_size(a, b, c)], min_bitlength=32, max_bitlength=32)
            h = g
            g = f
            f = e
            e = binary_addition_zfill(d, t1, min_bitlength=32, max_bitlength=32)
            d = c
            c = b
            b = a
            a = binary_addition_zfill(t1, t2, min_bitlength=32, max_bitlength=32)
        # Compute intermediate hash value
        h0 = binary_addition_zfill(h0, a, min_bitlength=32, max_bitlength=32)
        h1 = binary_addition_zfill(h1, b, min_bitlength=32, max_bitlength=32)
        h2 = binary_addition_zfill(h2, c, min_bitlength=32, max_bitlength=32)
        h3 = binary_addition_zfill(h3, d, min_bitlength=32, max_bitlength=32)
        h4 = binary_addition_zfill(h4, e, min_bitlength=32, max_bitlength=32)
        h5 = binary_addition_zfill(h5, f, min_bitlength=32, max_bitlength=32)
        h6 = binary_addition_zfill(h6, g, min_bitlength=32, max_bitlength=32)
        h7 = binary_addition_zfill(h7, h, min_bitlength=32, max_bitlength=32)
    result = "".join([h0, h1, h2, h3, h4, h5, h6, h7])
    result = int(result, 2).to_bytes(32, 'big')

    return result


def xor_binary_zfill(num_one: string, num_two: string) -> string:
    biggest_length = max(len(num_one), len(num_two))
    if len(num_one) != biggest_length:
        num_one = num_one.zfill(biggest_length)
    if len(num_two) != biggest_length:
        num_two = num_two.zfill(biggest_length)
    return "".join([str(0) if num_one[i] == num_two[i] else str(1) for i in range(biggest_length)])


def xor_binary_correct_size(num_one: string, num_two: string) -> string:
    if len(num_one) != len(num_two):
        raise ValueError("Length of left input is not the same as length of right input")
    else:
        return xor_binary_zfill(num_one, num_two)


def xor_multiple_binary_zfill(list_of_number: List[str]) -> string:
    if len(list_of_number) == 0:
        return ""
    elif len(list_of_number) == 1:
        return list_of_number[0]
    else:
        highest_length = len(list_of_number[0])
        previous_xor_result = list_of_number[0]
        for i in range(1, len(list_of_number)):
            if len(list_of_number[i]) > highest_length:
                highest_length = len(list_of_number[i])
            if len(list_of_number[i]) < highest_length:
                list_of_number[i] = list_of_number[i].zfill(highest_length)
            if len(previous_xor_result) < highest_length:
                previous_xor_result = previous_xor_result.zfill(highest_length)
            previous_xor_result = xor_binary_zfill(previous_xor_result, list_of_number[i])
        return previous_xor_result
    pass


def xor_multiple_binary_correct_size(list_of_number: List[str]) -> string:
    if len(list_of_number) == 0:
        return ""
    elif len(list_of_number) == 1:
        return list_of_number[0]
    else:
        for i in range(1, len(list_of_number)):
            if len(list_of_number[i]) != len(list_of_number[i-1]):
                raise ValueError("XOR between bitstring of different length.")
        return xor_multiple_binary_zfill(list_of_number)
    pass


def _sigma0(num: int):
    """As defined in the specification."""
    num = (_rotate_right(num, 7) ^
           _rotate_right(num, 18) ^
           (num >> 3))
    return num


def satisfiability_sigma0(num: List[ConjunctiveNormalForm.Variable]):
    size = 32
    if len(num) != size:
        raise ValueError("Error: len(num) != size")
    result_variable: List[ConjunctiveNormalForm.Variable] = []
    result_clause: List[ConjunctiveNormalForm.Clause] = []
    first_result = satisfiability_rotate_right(num, 7, size=size)
    result_clause.extend(first_result[1])
    first_result = first_result[0]
    second_result = satisfiability_rotate_right(num, 18, size=size)
    result_clause.extend(second_result[1])
    second_result = second_result[0]
    third_result = ConjunctiveNormalForm.right_shift(num, 3)
    # num = xor_multiple_binary_zfill([first_result, second_result, third_result])
    fourth_result = ConjunctiveNormalForm.xor_bitwise_multiple_input_same_size([first_result, second_result, third_result])
    result_clause.extend(fourth_result[1])
    fourth_result = fourth_result[0]
    result_variable = fourth_result
    return result_variable, result_clause


def _sigma0_binary_zfill(num: str) -> string:
    """As defined in the specification."""
    size = 32
    if len(num) < size:
        num.zfill(size)
    if len(num) > size:
        num = num[(len(num) - size):]
    first_result = _rotate_right_binary_zfill(num, 7, size=size)
    second_result = _rotate_right_binary_zfill(num, 18, size=size)
    third_result = num[:(len(num)-3)].zfill(size)
    num = xor_multiple_binary_zfill([first_result, second_result, third_result])
    '''
    num = (_rotate_right(num, 7) ^
           _rotate_right(num, 18) ^
           (num >> 3))
    '''
    return num


def _sigma0_binary_correct_size(num: str) -> string:
    """As defined in the specification."""
    size = 32
    if len(num) < size:
        raise ValueError("Error: str length is less than 4 byte (32 bits)")
    elif len(num) > size:
        raise ValueError("Error: str length is bigger than 4 byte (32 bits)")
    else:
        return _sigma0_binary_zfill(num)


def _sigma1(num: int):
    """As defined in the specification."""
    num = (_rotate_right(num, 17) ^
           _rotate_right(num, 19) ^
           (num >> 10))
    return num


def satisfiability_sigma1(num: List[ConjunctiveNormalForm.Variable]):
    size = 32
    if len(num) != size:
        raise ValueError("Error: len(num) != size")
    result_variable: List[ConjunctiveNormalForm.Variable] = []
    result_clause: List[ConjunctiveNormalForm.Clause] = []
    first_result = satisfiability_rotate_right(num, 17, size=size)
    result_clause.extend(first_result[1])
    first_result = first_result[0]
    second_result = satisfiability_rotate_right(num, 19, size=size)
    result_clause.extend(second_result[1])
    second_result = second_result[0]
    third_result = ConjunctiveNormalForm.right_shift(num, 10)
    # num = xor_multiple_binary_zfill([first_result, second_result, third_result])
    fourth_result = ConjunctiveNormalForm.xor_bitwise_multiple_input_same_size([first_result, second_result, third_result])
    result_clause.extend(fourth_result[1])
    fourth_result = fourth_result[0]
    result_variable = fourth_result
    return result_variable, result_clause


def _sigma1_binary_zfill(num: str) -> string:
    """As defined in the specification."""
    size = 32
    if len(num) < size:
        num.zfill(size)
    if len(num) > size:
        num = num[(len(num) - size):]
    first_result = _rotate_right_binary_zfill(num, 17, size=size)
    second_result = _rotate_right_binary_zfill(num, 19, size=size)
    third_result = num[:(len(num)-10)].zfill(size)
    num = xor_multiple_binary_zfill([first_result, second_result, third_result])
    '''
    num = (_rotate_right(num, 17) ^
           _rotate_right(num, 19) ^
           (num >> 10))
    '''
    return num


def _sigma1_binary_correct_size(num: str) -> string:
    """As defined in the specification."""
    size = 32
    if len(num) < size:
        raise ValueError("Error: str length is less than 4 byte (32 bits)")
    elif len(num) > size:
        raise ValueError("Error: str length is bigger than 4 byte (32 bits)")
    else:
        return _sigma1_binary_zfill(num)


def _capsigma0(num: int):
    """As defined in the specification."""
    num = (_rotate_right(num, 2) ^
           _rotate_right(num, 13) ^
           _rotate_right(num, 22))
    return num


def satisfiability_capsigma0(num: List[ConjunctiveNormalForm.Variable]):
    size = 32
    if len(num) != size:
        raise ValueError("Error: len(num) != size")
    result_variable: List[ConjunctiveNormalForm.Variable] = []
    result_clause: List[ConjunctiveNormalForm.Clause] = []
    first_result = satisfiability_rotate_right(num, 2, size=size)
    result_clause.extend(first_result[1])
    first_result = first_result[0]
    second_result = satisfiability_rotate_right(num, 13, size=size)
    result_clause.extend(second_result[1])
    second_result = second_result[0]
    third_result = satisfiability_rotate_right(num, 22, size=size)
    result_clause.extend(third_result[1])
    third_result = third_result[0]
    # num = xor_multiple_binary_zfill([first_result, second_result, third_result])
    fourth_result = ConjunctiveNormalForm.xor_bitwise_multiple_input_same_size([first_result, second_result, third_result])
    result_clause.extend(fourth_result[1])
    fourth_result = fourth_result[0]
    result_variable = fourth_result
    return result_variable, result_clause


def _capsigma0_binary(num: string) -> string:
    """As defined in the specification."""
    num = xor_multiple_binary_correct_size([_rotate_right_binary_correct_size(num, 2, size=32),
                                            _rotate_right_binary_correct_size(num, 13, size=32),
                                            _rotate_right_binary_correct_size(num, 22, size=32)])
    return num


def _capsigma1(num: int):
    """As defined in the specification."""
    num = (_rotate_right(num, 6) ^
           _rotate_right(num, 11) ^
           _rotate_right(num, 25))
    return num


def satisfiability_capsigma1(num: List[ConjunctiveNormalForm.Variable]):
    size = 32
    if len(num) != size:
        raise ValueError("Error: len(num) != size")
    result_variable: List[ConjunctiveNormalForm.Variable] = []
    result_clause: List[ConjunctiveNormalForm.Clause] = []
    first_result = satisfiability_rotate_right(num, 6, size=size)
    result_clause.extend(first_result[1])
    first_result = first_result[0]
    second_result = satisfiability_rotate_right(num, 11, size=size)
    result_clause.extend(second_result[1])
    second_result = second_result[0]
    third_result = satisfiability_rotate_right(num, 25, size=size)
    result_clause.extend(third_result[1])
    third_result = third_result[0]
    # num = xor_multiple_binary_zfill([first_result, second_result, third_result])
    fourth_result = ConjunctiveNormalForm.xor_bitwise_multiple_input_same_size([first_result, second_result, third_result])
    result_clause.extend(fourth_result[1])
    fourth_result = fourth_result[0]
    result_variable = fourth_result
    return result_variable, result_clause


def _capsigma1_binary(num: string) -> string:
    """As defined in the specification."""
    if type(num) is not string and type(num) is not str:
        raise ValueError(num)
    num = xor_multiple_binary_correct_size([_rotate_right_binary_correct_size(num, 6, size=32),
                                            _rotate_right_binary_correct_size(num, 11, size=32),
                                            _rotate_right_binary_correct_size(num, 25, size=32)])
    return num


def not_gate_binary(x: string) -> string:
    result = []
    for char in x:
        if char == "1":
            result.append("0")
        elif char == "0":
            result.append("1")
        else:
            raise ValueError("X contain character other than 0 and 1")
    return "".join(result)


def and_gate_binary_zfill(x: string, y: string) -> string:
    biggest_bitlength = max(len(x), len(y))
    if len(x) < biggest_bitlength:
        x.zfill(biggest_bitlength)
    if len(y) < biggest_bitlength:
        y.zfill(biggest_bitlength)
    result = []
    for i in range(biggest_bitlength):
        if x[i] == "0" or y[i] == "0":
            result.append("0")
        elif x[i] == "1" and y[i] == "1":
            result.append("1")
        else:
            raise ValueError("X or Y contain character other than 0 and 1")
    return "".join(result)


def _ch(x: int, y: int, z: int):
    """As defined in the specification."""
    return (x & y) ^ (~x & z)


def satisfiability_ch(x: List[ConjunctiveNormalForm.Variable], y: List[ConjunctiveNormalForm.Variable],
                      z: List[ConjunctiveNormalForm.Variable]):
    size = 32
    if len(x) != size:
        raise ValueError("Error: len(x) != size")
    result_variable: List[ConjunctiveNormalForm.Variable] = []
    result_clause: List[ConjunctiveNormalForm.Clause] = []
    first_result = ConjunctiveNormalForm.and_bitwise_two_input_same_size(x, y)
    result_clause.extend(first_result[1])
    first_result = first_result[0]
    second_result = ConjunctiveNormalForm.and_bitwise_two_input_same_size(ConjunctiveNormalForm.not_bitwise(x), z)
    result_clause.extend(second_result[1])
    second_result = second_result[0]
    third_result = ConjunctiveNormalForm.xor_bitwise_two_input_same_size(first_result, second_result)
    result_clause.extend(third_result[1])
    third_result = third_result[0]
    result_variable = third_result
    return result_variable, result_clause


def _ch_binary_zfill(x: string, y: string, z: string) -> string:
    biggest_bitlength = max(len(x), len(y), len(z))
    if len(x) < biggest_bitlength:
        x = x.zfill(biggest_bitlength)
    if len(y) < biggest_bitlength:
        y = y.zfill(biggest_bitlength)
    if len(z) < biggest_bitlength:
        z = z.zfill(biggest_bitlength)
    return xor_binary_zfill(and_gate_binary_zfill(x, y), and_gate_binary_zfill(not_gate_binary(x), z))


def _ch_binary_correct_size(x: string, y: string, z: string) -> string:
    if len(x) == len(y) == len(z):
        return _ch_binary_zfill(x, y, z)
    else:
        raise ValueError("not all X, Y, and Z contain same bitlength")


def _maj(x: int, y: int, z: int):
    """As defined in the specification."""
    return (x & y) ^ (x & z) ^ (y & z)


def satisfiability_maj(x: List[ConjunctiveNormalForm.Variable], y: List[ConjunctiveNormalForm.Variable],
                       z: List[ConjunctiveNormalForm.Variable]):
    size = 32
    if len(x) != size:
        raise ValueError("Error: len(x) != size")
    result_variable: List[ConjunctiveNormalForm.Variable] = []
    result_clause: List[ConjunctiveNormalForm.Clause] = []
    first_result = ConjunctiveNormalForm.and_bitwise_two_input_same_size(x, y)
    result_clause.extend(first_result[1])
    first_result = first_result[0]
    second_result = ConjunctiveNormalForm.and_bitwise_two_input_same_size(x, z)
    result_clause.extend(second_result[1])
    second_result = second_result[0]
    third_result = ConjunctiveNormalForm.and_bitwise_two_input_same_size(y, z)
    result_clause.extend(third_result[1])
    third_result = third_result[0]
    fourth_result = ConjunctiveNormalForm.xor_bitwise_multiple_input_same_size([first_result, second_result, third_result])
    result_clause.extend(fourth_result[1])
    fourth_result = fourth_result[0]
    result_variable = fourth_result
    return result_variable, result_clause


def _maj_binary_zfill(x: string, y: string, z: string) -> string:
    biggest_bitlength = max(len(x), len(y), len(z))
    if len(x) < biggest_bitlength:
        x = x.zfill(biggest_bitlength)
    if len(y) < biggest_bitlength:
        y = y.zfill(biggest_bitlength)
    if len(z) < biggest_bitlength:
        z = z.zfill(biggest_bitlength)
    return xor_multiple_binary_zfill([and_gate_binary_zfill(x, y), and_gate_binary_zfill(x, z),
                                      and_gate_binary_zfill(y, z)])


def _maj_binary_correct_size(x: string, y: string, z: string) -> string:
    if len(x) == len(y) == len(z):
        return _maj_binary_zfill(x, y, z)
    else:
        raise ValueError("not all X, Y, and Z contain same bitlength")


def _rotate_right(num: int, shift: int, size: int = 32):
    """Rotate an integer right."""
    return (num >> shift) | (num << size - shift)


def satisfiability_rotate_right(num: List[ConjunctiveNormalForm.Variable], shift: int, size: int = 32) -> \
        Tuple[List[ConjunctiveNormalForm.Variable], List[ConjunctiveNormalForm.Clause]]:
    if len(num) != size:
        raise ValueError("Error: len(num) != size")
    shift = shift % size
    result_variable: List[ConjunctiveNormalForm.Variable] = []
    result_clause: List[ConjunctiveNormalForm.Clause] = []
    for i in range(size):
        left_bit: Union[ConjunctiveNormalForm.Variable, None] = None
        right_bit: Union[ConjunctiveNormalForm.Variable, None] = None
        if i - shift >= 0:
            left_bit = num[i - shift]
        else:
            left_bit = ConjunctiveNormalForm.Variable()
            left_bit.set_truth_value(False)
        if i + size - shift < size:
            right_bit = num[i + size - shift]
        else:
            right_bit = ConjunctiveNormalForm.Variable()
            right_bit.set_truth_value(False)
        or_gate_result = ConjunctiveNormalForm.or_gate_two_input(left_bit, right_bit)
        result_variable.append(or_gate_result[0])
        result_clause.extend(or_gate_result[1])
    return result_variable, result_clause


def _rotate_right_binary_zfill(num: string, shift: int, size: int = 32) -> string:
    """Rotate an integer right."""
    if size < 0:
        raise ValueError("Error: shift value less than 0")
    if size == 0:
        return ""
    else:
        if len(num) < size:
            num = num.zfill(size)
        shift = shift % size
        to_join = []
        for i in range(size):
            left_bit = None
            right_bit = None
            if i - shift >= 0:
                left_bit = num[i-shift]
            else:
                left_bit = "0"
            if i + size-shift < size:
                right_bit = num[i + size-shift]
            else:
                right_bit = "0"
            if left_bit == "1" or right_bit == "1":
                to_join.append("1")
            else:
                to_join.append("0")
        return "".join(to_join)


def _rotate_right_binary_correct_size(num: string, shift: int, size: int = 32) -> string:
    if len(num) < size:
        raise ValueError("number bitlength is less than size")
    else:
        return _rotate_right_binary_zfill(num, shift, size)


def satisfiability_binary_addition_two_input_same_size(
        num_one: List[Union[ConjunctiveNormalForm.Variable, ConjunctiveNormalForm.Literal]],
        num_two: List[Union[ConjunctiveNormalForm.Variable, ConjunctiveNormalForm.Literal]],
        append_carry_at_last: bool = False) -> \
        Tuple[List[ConjunctiveNormalForm.Variable], List[ConjunctiveNormalForm.Clause]]:
    if len(num_one) != len(num_two):
        raise ValueError("Error: len(num_one) != len(num_two)")
    bitlength = len(num_one)
    result_variable: List[ConjunctiveNormalForm.Variable] = [ConjunctiveNormalForm.Variable() for i in range(bitlength)]
    result_clause: List[ConjunctiveNormalForm.Clause] = []
    carry: List[ConjunctiveNormalForm.Variable] = [ConjunctiveNormalForm.Variable() for i in range(bitlength)]
    # first carry is 0
    carry[bitlength-1].set_truth_value(False)
    for i in range(bitlength - 1, -1, -1):
        if i == bitlength-1:
            result_clause.append(ConjunctiveNormalForm.Clause(list_of_literal=[
                ConjunctiveNormalForm.not_gate(carry[i])
            ]))
        else:
            '''
            if (carry == "1" and left_bit == "1" and right_bit == "1") or \
                (carry == "1" and left_bit == "1" and right_bit == "0") or \
                (carry == "1" and left_bit == "0" and right_bit == "1") or \
                (carry == "0" and left_bit == "1" and right_bit == "1"):
                carry = "1"
            else:
                carry = "0"
            '''
            # At+1 AND Bt+1 -> Ct = NOT At+1 OR NOT Bt+1 OR Ct
            # At+1 AND Ct+1 -> Ct = NOT At+1 OR NOT Ct+1 OR Ct
            # Bt+1 AND Ct+1 -> Ct = NOT Bt+1 OR NOT Ct+1 OR Ct
            # NOT At+1 AND NOT Bt+1 -> NOT Ct = At+1 OR Bt+1 OR NOT Ct
            # NOT At+1 AND NOT Ct+1 -> NOT Ct = At+1 OR Ct+1 OR NOT Ct
            # NOT Bt+1 AND NOT Ct+1 -> NOT Ct = Bt+1 OR Ct+1 OR NOT Ct

            # At+1 AND Bt+1 -> Ct = NOT At+1 OR NOT Bt+1 OR Ct
            # At+1 AND Ct+1 -> Ct = NOT At+1 OR NOT Ct+1 OR Ct
            # Bt+1 AND Ct+1 -> Ct = NOT Bt+1 OR NOT Ct+1 OR Ct

            # At+1 AND Bt+1 -> Ct = NOT At+1 OR NOT Bt+1 OR Ct
            result_clause.append(ConjunctiveNormalForm.Clause(list_of_literal=[
                ConjunctiveNormalForm.not_gate(num_one[i + 1]), ConjunctiveNormalForm.not_gate(num_two[i + 1]), carry[i]
            ]))

            # At+1 AND Ct+1 -> Ct = NOT At+1 OR NOT Ct+1 OR Ct
            result_clause.append(ConjunctiveNormalForm.Clause(list_of_literal=[
                ConjunctiveNormalForm.not_gate(num_one[i + 1]), ConjunctiveNormalForm.not_gate(carry[i + 1]), carry[i]
            ]))

            # Bt+1 AND Ct+1 -> Ct = NOT Bt+1 OR NOT Ct+1 OR Ct
            result_clause.append(ConjunctiveNormalForm.Clause(list_of_literal=[
                ConjunctiveNormalForm.not_gate(num_two[i + 1]), ConjunctiveNormalForm.not_gate(carry[i + 1]), carry[i]
            ]))

            # NOT At+1 AND NOT Bt+1 -> NOT Ct = At+1 OR Bt+1 OR NOT Ct
            # NOT At+1 AND NOT Ct+1 -> NOT Ct = At+1 OR Ct+1 OR NOT Ct
            # NOT Bt+1 AND NOT Ct+1 -> NOT Ct = Bt+1 OR Ct+1 OR NOT Ct

            # NOT At+1 AND NOT Bt+1 -> NOT Ct = At+1 OR Bt+1 OR NOT Ct
            result_clause.append(ConjunctiveNormalForm.Clause(list_of_literal=[
                num_one[i+1], num_two[i+1], ConjunctiveNormalForm.not_gate(carry[i])
            ]))

            # NOT At+1 AND NOT Ct+1 -> NOT Ct = At+1 OR Ct+1 OR NOT Ct
            result_clause.append(ConjunctiveNormalForm.Clause(list_of_literal=[
                num_one[i + 1], carry[i + 1], ConjunctiveNormalForm.not_gate(carry[i])
            ]))

            # NOT Bt+1 AND NOT Ct+1 -> NOT Ct = Bt+1 OR Ct+1 OR NOT Ct
            result_clause.append(ConjunctiveNormalForm.Clause(list_of_literal=[
                num_two[i + 1], carry[i + 1], ConjunctiveNormalForm.not_gate(carry[i])
            ]))
        '''
        if (carry == "1" and left_bit == "1" and right_bit == "1") or \
            (carry == "1" and left_bit == "0" and right_bit == "0") or \
            (carry == "0" and left_bit == "1" and right_bit == "0") or \
            (carry == "0" and left_bit == "0" and right_bit == "1"):
            result_bitstring.append("1")
        else:
            result_bitstring.append("0")
        '''

        # At AND Bt AND Ct -> Dt = NOT At OR NOT Bt OR NOT Ct OR Dt
        # At AND NOT Bt AND NOT Ct -> Dt = NOT At OR Bt OR Ct OR Dt
        # NOT At AND Bt AND NOT Ct -> Dt = At OR NOT Bt OR Ct OR Dt
        # NOT At AND NOT Bt AND Ct -> Dt = At OR Bt OR NOT Ct OR Dt
        # NOT At AND NOT Bt AND NOT Ct -> NOT Dt = At OR Bt OR Ct OR NOT Dt
        # At AND Bt AND NOT Ct -> NOT Dt = NOT At OR NOT Bt OR Ct OR NOT Dt
        # At AND NOT Bt AND Ct -> NOT Dt = NOT At OR Bt OR NOT Ct OR NOT Dt
        # NOT At AND Bt AND Ct -> NOT Dt = At OR NOT Bt OR NOT Ct OR NOT Dt

        # At AND Bt AND Ct -> Dt = NOT At OR NOT Bt OR NOT Ct OR Dt
        # At AND NOT Bt AND NOT Ct -> Dt = NOT At OR Bt OR Ct OR Dt
        # NOT At AND Bt AND NOT Ct -> Dt = At OR NOT Bt OR Ct OR Dt
        # NOT At AND NOT Bt AND Ct -> Dt = At OR Bt OR NOT Ct OR Dt

        # At AND Bt AND Ct -> Dt = NOT At OR NOT Bt OR NOT Ct OR Dt
        result_clause.append(ConjunctiveNormalForm.Clause(list_of_literal=[
            ConjunctiveNormalForm.not_gate(num_one[i]),
            ConjunctiveNormalForm.not_gate(num_two[i]),
            ConjunctiveNormalForm.not_gate(carry[i]),
            result_variable[i]
        ]))

        # At AND NOT Bt AND NOT Ct -> Dt = NOT At OR Bt OR Ct OR Dt
        result_clause.append(ConjunctiveNormalForm.Clause(list_of_literal=[
            ConjunctiveNormalForm.not_gate(num_one[i]),
            num_two[i],
            carry[i],
            result_variable[i]
        ]))

        # NOT At AND Bt AND NOT Ct -> Dt = At OR NOT Bt OR Ct OR Dt
        result_clause.append(ConjunctiveNormalForm.Clause(list_of_literal=[
            num_one[i],
            ConjunctiveNormalForm.not_gate(num_two[i]),
            carry[i],
            result_variable[i]
        ]))

        # NOT At AND NOT Bt AND Ct -> Dt = At OR Bt OR NOT Ct OR Dt
        result_clause.append(ConjunctiveNormalForm.Clause(list_of_literal=[
            num_one[i],
            num_two[i],
            ConjunctiveNormalForm.not_gate(carry[i]),
            result_variable[i]
        ]))

        # NOT At AND NOT Bt AND NOT Ct -> NOT Dt = At OR Bt OR Ct OR NOT Dt
        # At AND Bt AND NOT Ct -> NOT Dt = NOT At OR NOT Bt OR Ct OR NOT Dt
        # At AND NOT Bt AND Ct -> NOT Dt = NOT At OR Bt OR NOT Ct OR NOT Dt
        # NOT At AND Bt AND Ct -> NOT Dt = At OR NOT Bt OR NOT Ct OR NOT Dt

        # NOT At AND NOT Bt AND NOT Ct -> NOT Dt = At OR Bt OR Ct OR NOT Dt
        result_clause.append(ConjunctiveNormalForm.Clause(list_of_literal=[
            num_one[i],
            num_two[i],
            carry[i],
            ConjunctiveNormalForm.not_gate(result_variable[i])
        ]))

        # At AND Bt AND NOT Ct -> NOT Dt = NOT At OR NOT Bt OR Ct OR NOT Dt
        result_clause.append(ConjunctiveNormalForm.Clause(list_of_literal=[
            ConjunctiveNormalForm.not_gate(num_one[i]),
            ConjunctiveNormalForm.not_gate(num_two[i]),
            carry[i],
            ConjunctiveNormalForm.not_gate(result_variable[i])
        ]))

        # At AND NOT Bt AND Ct -> NOT Dt = NOT At OR Bt OR NOT Ct OR NOT Dt
        result_clause.append(ConjunctiveNormalForm.Clause(list_of_literal=[
            ConjunctiveNormalForm.not_gate(num_one[i]),
            num_two[i],
            ConjunctiveNormalForm.not_gate(carry[i]),
            ConjunctiveNormalForm.not_gate(result_variable[i])
        ]))

        # NOT At AND Bt AND Ct -> NOT Dt = At OR NOT Bt OR NOT Ct OR NOT Dt
        result_clause.append(ConjunctiveNormalForm.Clause(list_of_literal=[
            num_one[i],
            ConjunctiveNormalForm.not_gate(num_two[i]),
            ConjunctiveNormalForm.not_gate(carry[i]),
            ConjunctiveNormalForm.not_gate(result_variable[i])
        ]))

    if append_carry_at_last:
        new_carry = ConjunctiveNormalForm.Variable()
        # At+1 AND Bt+1 -> Ct = NOT At+1 OR NOT Bt+1 OR Ct
        # At+1 AND Ct+1 -> Ct = NOT At+1 OR NOT Ct+1 OR Ct
        # Bt+1 AND Ct+1 -> Ct = NOT Bt+1 OR NOT Ct+1 OR Ct
        # NOT At+1 AND NOT Bt+1 -> NOT Ct = At+1 OR Bt+1 OR NOT Ct
        # NOT At+1 AND NOT Ct+1 -> NOT Ct = At+1 OR Ct+1 OR NOT Ct
        # NOT Bt+1 AND NOT Ct+1 -> NOT Ct = Bt+1 OR Ct+1 OR NOT Ct

        # At+1 AND Bt+1 -> Ct = NOT At+1 OR NOT Bt+1 OR Ct
        # At+1 AND Ct+1 -> Ct = NOT At+1 OR NOT Ct+1 OR Ct
        # Bt+1 AND Ct+1 -> Ct = NOT Bt+1 OR NOT Ct+1 OR Ct

        # At+1 AND Bt+1 -> Ct = NOT At+1 OR NOT Bt+1 OR Ct
        result_clause.append(ConjunctiveNormalForm.Clause(list_of_literal=[
            ConjunctiveNormalForm.not_gate(num_one[0]), ConjunctiveNormalForm.not_gate(num_two[0]), new_carry
        ]))

        # At+1 AND Ct+1 -> Ct = NOT At+1 OR NOT Ct+1 OR Ct
        result_clause.append(ConjunctiveNormalForm.Clause(list_of_literal=[
            ConjunctiveNormalForm.not_gate(num_one[0]), ConjunctiveNormalForm.not_gate(carry[0]), new_carry
        ]))

        # Bt+1 AND Ct+1 -> Ct = NOT Bt+1 OR NOT Ct+1 OR Ct
        result_clause.append(ConjunctiveNormalForm.Clause(list_of_literal=[
            ConjunctiveNormalForm.not_gate(num_two[0]), ConjunctiveNormalForm.not_gate(carry[0]), new_carry
        ]))

        # NOT At+1 AND NOT Bt+1 -> NOT Ct = At+1 OR Bt+1 OR NOT Ct
        # NOT At+1 AND NOT Ct+1 -> NOT Ct = At+1 OR Ct+1 OR NOT Ct
        # NOT Bt+1 AND NOT Ct+1 -> NOT Ct = Bt+1 OR Ct+1 OR NOT Ct

        # NOT At+1 AND NOT Bt+1 -> NOT Ct = At+1 OR Bt+1 OR NOT Ct
        result_clause.append(ConjunctiveNormalForm.Clause(list_of_literal=[
            num_one[0], num_two[0], ConjunctiveNormalForm.not_gate(new_carry)
        ]))

        # NOT At+1 AND NOT Ct+1 -> NOT Ct = At+1 OR Ct+1 OR NOT Ct
        result_clause.append(ConjunctiveNormalForm.Clause(list_of_literal=[
            num_one[0], carry[0], ConjunctiveNormalForm.not_gate(new_carry)
        ]))

        # NOT Bt+1 AND NOT Ct+1 -> NOT Ct = Bt+1 OR Ct+1 OR NOT Ct
        result_clause.append(ConjunctiveNormalForm.Clause(list_of_literal=[
            num_two[0], carry[0], ConjunctiveNormalForm.not_gate(new_carry)
        ]))

        result_variable.insert(0, new_carry)
    return result_variable, result_clause


def satisfiability_binary_addition_multiple_input_same_size(
        num: List[List[Union[ConjunctiveNormalForm.Variable, ConjunctiveNormalForm.Literal]]],
        append_carry_at_last: bool = False) -> \
        Tuple[List[ConjunctiveNormalForm.Variable], List[ConjunctiveNormalForm.Clause]]:
    if len(num) == 0:
        return [], []
    else:
        bitlength = len(num[0])
        result_variable: List[ConjunctiveNormalForm.Variable] = num[0]
        result_clause: List[ConjunctiveNormalForm.Clause] = []
        for i in range(1, len(num)):
            if len(num[i]) != bitlength:
                raise ValueError("Error: len(num[%s]) != bitlength" % i)
            addition_result = satisfiability_binary_addition_two_input_same_size(
                result_variable, num[i], append_carry_at_last=append_carry_at_last)
            result_clause.extend(addition_result[1])
            result_variable = addition_result[0]
        return result_variable, result_clause


# return in big endian
def binary_addition_zfill(
        num_left: string, num_right: string, min_bitlength: int = 0, max_bitlength: int = -1) -> string:
    if max_bitlength == 0:
        return ""
    if min_bitlength > 0 and 0 < max_bitlength < min_bitlength:
        raise ValueError("Error: min_bitlength is bigger than max_bitlength")
    if min_bitlength > 0 and len(num_left) < min_bitlength:
        num_left = num_left.zfill(min_bitlength)
    if min_bitlength > 0 and len(num_right) < min_bitlength:
        num_right = num_right.zfill(min_bitlength)
    if 0 < max_bitlength < len(num_left):
        num_left = num_left[(len(num_left)-max_bitlength):]
    if 0 < max_bitlength < len(num_right):
        num_right = num_right[(len(num_right)-max_bitlength):]
    biggest_length = max(len(num_left), len(num_right))
    if len(num_left) < biggest_length:
        num_left = num_left.zfill(biggest_length)
    if len(num_right) < biggest_length:
        num_right = num_right.zfill(biggest_length)
    carry = "0"
    result_bitstring = []
    for i in range(biggest_length-1, -1, -1):
        left_bit = num_left[i]
        right_bit = num_right[i]
        if left_bit != "1" and left_bit != "0":
            raise ValueError(left_bit)
        if right_bit != "1" and right_bit != "0":
            raise ValueError(right_bit)
        if carry != "1" and carry != "0":
            raise ValueError(carry)
        if (carry == "1" and left_bit == "1" and right_bit == "1") or \
                (carry == "1" and left_bit == "0" and right_bit == "0") or \
                (carry == "0" and left_bit == "1" and right_bit == "0") or \
                (carry == "0" and left_bit == "0" and right_bit == "1"):
            result_bitstring.append("1")
        else:
            result_bitstring.append("0")
        if (carry == "1" and left_bit == "1" and right_bit == "1") or \
                (carry == "1" and left_bit == "1" and right_bit == "0") or \
                (carry == "1" and left_bit == "0" and right_bit == "1") or \
                (carry == "0" and left_bit == "1" and right_bit == "1"):
            carry = "1"
        else:
            carry = "0"
    if carry == "1":
        result_bitstring.append("1")
    result_bitstring = "".join(reversed(result_bitstring))
    if min_bitlength > 0 and len(result_bitstring) < min_bitlength:
        result_bitstring = result_bitstring.zfill(min_bitlength)
    if 0 < max_bitlength < len(result_bitstring):
        result_bitstring = result_bitstring[(len(result_bitstring)-max_bitlength):]
    return result_bitstring


def binary_addition_zfill_multiple(
        list_of_num: List[str], min_bitlength: int = 0, max_bitlength: int = -1) -> string:
    if max_bitlength == 0 or len(list_of_num) == 0:
        return ""
    if len(list_of_num) == 1:
        if min_bitlength > 0 and 0 < max_bitlength < min_bitlength:
            raise ValueError("Error: min_bitlength is bigger than max_bitlength")
        if min_bitlength > 0 and len(list_of_num[0]) < min_bitlength:
            list_of_num[0] = list_of_num[0].zfill(min_bitlength)
        if 0 < max_bitlength < len(list_of_num[0]):
            list_of_num[0] = list_of_num[0][(len(list_of_num[0]) - max_bitlength):]
        return list_of_num[0]
    previous_sum = list_of_num[0]
    for i in range(1, len(list_of_num)):
        previous_sum = binary_addition_zfill(previous_sum, list_of_num[i], min_bitlength, max_bitlength)
    return previous_sum
