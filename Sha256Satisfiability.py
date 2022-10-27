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


def rotate_right(num: List[ConjunctiveNormalForm.Variable], shift: int, size: int = 32) -> \
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


def sigma0(num: List[ConjunctiveNormalForm.Variable]) -> Tuple[List[ConjunctiveNormalForm.Variable], List[ConjunctiveNormalForm.Clause]]:
    size = 32
    if len(num) != size:
        raise ValueError("Error: len(num) != size")
    result_variable: List[ConjunctiveNormalForm.Variable] = []
    result_clause: List[ConjunctiveNormalForm.Clause] = []
    first_result = rotate_right(num, 7, size=size)
    result_clause.extend(first_result[1])
    first_result = first_result[0]
    second_result = rotate_right(num, 18, size=size)
    result_clause.extend(second_result[1])
    second_result = second_result[0]
    third_result = ConjunctiveNormalForm.right_shift(num, 3)
    # num = xor_multiple_binary_zfill([first_result, second_result, third_result])
    fourth_result = ConjunctiveNormalForm.xor_bitwise_multiple_input_same_size([first_result, second_result, third_result])
    result_clause.extend(fourth_result[1])
    fourth_result = fourth_result[0]
    result_variable = fourth_result
    return result_variable, result_clause


def sigma1(num: List[ConjunctiveNormalForm.Variable]) -> Tuple[List[ConjunctiveNormalForm.Variable], List[ConjunctiveNormalForm.Clause]]:
    size = 32
    if len(num) != size:
        raise ValueError("Error: len(num) != size")
    result_variable: List[ConjunctiveNormalForm.Variable] = []
    result_clause: List[ConjunctiveNormalForm.Clause] = []
    first_result = rotate_right(num, 17, size=size)
    result_clause.extend(first_result[1])
    first_result = first_result[0]
    second_result = rotate_right(num, 19, size=size)
    result_clause.extend(second_result[1])
    second_result = second_result[0]
    third_result = ConjunctiveNormalForm.right_shift(num, 10)
    # num = xor_multiple_binary_zfill([first_result, second_result, third_result])
    fourth_result = ConjunctiveNormalForm.xor_bitwise_multiple_input_same_size([first_result, second_result, third_result])
    result_clause.extend(fourth_result[1])
    fourth_result = fourth_result[0]
    result_variable = fourth_result
    return result_variable, result_clause


def capsigma0(num: List[ConjunctiveNormalForm.Variable]) -> \
        Tuple[List[ConjunctiveNormalForm.Variable], List[ConjunctiveNormalForm.Clause]]:
    size = 32
    if len(num) != size:
        raise ValueError("Error: len(num) != size")
    result_variable: List[ConjunctiveNormalForm.Variable] = []
    result_clause: List[ConjunctiveNormalForm.Clause] = []
    first_result = rotate_right(num, 2, size=size)
    result_clause.extend(first_result[1])
    first_result = first_result[0]
    second_result = rotate_right(num, 13, size=size)
    result_clause.extend(second_result[1])
    second_result = second_result[0]
    third_result = rotate_right(num, 22, size=size)
    result_clause.extend(third_result[1])
    third_result = third_result[0]
    # num = xor_multiple_binary_zfill([first_result, second_result, third_result])
    fourth_result = ConjunctiveNormalForm.xor_bitwise_multiple_input_same_size([first_result, second_result, third_result])
    result_clause.extend(fourth_result[1])
    fourth_result = fourth_result[0]
    result_variable = fourth_result
    return result_variable, result_clause


def capsigma1(num: List[ConjunctiveNormalForm.Variable]) -> \
        Tuple[List[ConjunctiveNormalForm.Variable], List[ConjunctiveNormalForm.Clause]]:
    size = 32
    if len(num) != size:
        raise ValueError("Error: len(num) != size")
    result_variable: List[ConjunctiveNormalForm.Variable] = []
    result_clause: List[ConjunctiveNormalForm.Clause] = []
    first_result = rotate_right(num, 6, size=size)
    result_clause.extend(first_result[1])
    first_result = first_result[0]
    second_result = rotate_right(num, 11, size=size)
    result_clause.extend(second_result[1])
    second_result = second_result[0]
    third_result = rotate_right(num, 25, size=size)
    result_clause.extend(third_result[1])
    third_result = third_result[0]
    # num = xor_multiple_binary_zfill([first_result, second_result, third_result])
    fourth_result = ConjunctiveNormalForm.xor_bitwise_multiple_input_same_size([first_result, second_result, third_result])
    result_clause.extend(fourth_result[1])
    fourth_result = fourth_result[0]
    result_variable = fourth_result
    return result_variable, result_clause


def ch(x: List[ConjunctiveNormalForm.Variable], y: List[ConjunctiveNormalForm.Variable],
       z: List[ConjunctiveNormalForm.Variable]) -> \
        Tuple[List[ConjunctiveNormalForm.Variable], List[ConjunctiveNormalForm.Clause]]:
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


def maj(x: List[ConjunctiveNormalForm.Variable], y: List[ConjunctiveNormalForm.Variable],
        z: List[ConjunctiveNormalForm.Variable]) -> \
        Tuple[List[ConjunctiveNormalForm.Variable], List[ConjunctiveNormalForm.Clause]]:
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


def binary_addition_two_input_same_size(
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


def binary_addition_multiple_input_same_size(
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
            addition_result = binary_addition_two_input_same_size(
                result_variable, num[i], append_carry_at_last=append_carry_at_last)
            result_clause.extend(addition_result[1])
            result_variable = addition_result[0]
        return result_variable, result_clause


# return tuple of 3 element
# 1st element: list of input variable
# 2nd element: list of output variable
# 3rd element: satisfiability formula
def generate_sha256_formula(message_length: int) -> \
        Tuple[List[ConjunctiveNormalForm.Variable], List[ConjunctiveNormalForm.Variable], ConjunctiveNormalForm]:
    result_formula: ConjunctiveNormalForm = ConjunctiveNormalForm()
    result_input_variable: List[ConjunctiveNormalForm.Variable] = \
        [ConjunctiveNormalForm.Variable() for i in range(message_length)]
    # shallow copy
    message: List[ConjunctiveNormalForm.Variable] = \
        [result_input_variable[i] for i in range(message_length)]
    x80_bitstring = bytearray_to_bitstring(bytearray.fromhex("80"))
    x80: List[ConjunctiveNormalForm.Variable] = []
    for x80_bit in x80_bitstring:
        variable_to_append = ConjunctiveNormalForm.Variable()
        if x80_bit == "0":
            variable_to_append.set_truth_value(False)
        elif x80_bit == "1":
            variable_to_append.set_truth_value(True)
        else:
            raise ValueError("Error: x80_bit contain symbol other than 0 and 1")
        x80.append(variable_to_append)
    message.extend(x80)
    while (len(message) + 64) % 512 != 0:
        variable_to_append = ConjunctiveNormalForm.Variable()
        variable_to_append.set_truth_value(False)
        message.append(variable_to_append)
    message_length_bitstring = bytearray_to_bitstring(bytearray(message_length.to_bytes(8, 'big')))
    if len(message_length_bitstring) != 8*8:
        raise ValueError("Error: len(message_length_bitstring) != 64 bit, got ", len(message_length_bitstring), " bit")
    message_length_bitstring_variable: List[ConjunctiveNormalForm.Variable] = []
    for message_length_bit in message_length_bitstring:
        variable_to_append = ConjunctiveNormalForm.Variable()
        if message_length_bit == "0":
            variable_to_append.set_truth_value(False)
        elif message_length_bit == "1":
            variable_to_append.set_truth_value(True)
        else:
            raise ValueError("Error: message_length_bit contain symbol other than 0 and 1")
        message_length_bitstring_variable.append(variable_to_append)
    message.extend(message_length_bitstring_variable)
    assert (len(message)) % 512 == 0, "Padding did not complete properly!"
    blocks: List[List[ConjunctiveNormalForm.Variable]] = []
    for i in range(0, message_length, 512):
        blocks.append(message[i:i + 512])
    # Setting Initial Hash Value
    h0 = 0x6a09e667
    h0 = hex(h0)[2:]
    h0 = h0.zfill(len(h0) + (len(h0) % 2))
    h0 = bytearray_to_bitstring(bytearray.fromhex(h0)).zfill(32)
    h0_variable: List[ConjunctiveNormalForm.Variable] = []
    for h0_bit in h0:
        variable_to_append = ConjunctiveNormalForm.Variable()
        if h0_bit == "0":
            variable_to_append.set_truth_value(False)
        elif h0_bit == "1":
            variable_to_append.set_truth_value(True)
        else:
            raise ValueError("Error: h0_bit contain symbol other than 0 and 1")
        h0_variable.append(variable_to_append)
    h1 = 0xbb67ae85
    h1 = hex(h1)[2:]
    h1 = h1.zfill(len(h1) + (len(h1) % 2))
    h1 = bytearray_to_bitstring(bytearray.fromhex(h1)).zfill(32)
    h1_variable: List[ConjunctiveNormalForm.Variable] = []
    for h1_bit in h1:
        variable_to_append = ConjunctiveNormalForm.Variable()
        if h1_bit == "0":
            variable_to_append.set_truth_value(False)
        elif h1_bit == "1":
            variable_to_append.set_truth_value(True)
        else:
            raise ValueError("Error: h1_bit contain symbol other than 0 and 1")
        h1_variable.append(variable_to_append)
    h2 = 0x3c6ef372
    h2 = hex(h2)[2:]
    h2 = h2.zfill(len(h2) + (len(h2) % 2))
    h2 = bytearray_to_bitstring(bytearray.fromhex(h2)).zfill(32)
    h2_variable: List[ConjunctiveNormalForm.Variable] = []
    for h2_bit in h2:
        variable_to_append = ConjunctiveNormalForm.Variable()
        if h2_bit == "0":
            variable_to_append.set_truth_value(False)
        elif h2_bit == "1":
            variable_to_append.set_truth_value(True)
        else:
            raise ValueError("Error: h2_bit contain symbol other than 0 and 1")
        h2_variable.append(variable_to_append)
    h3 = 0xa54ff53a
    h3 = hex(h3)[2:]
    h3 = h3.zfill(len(h3) + (len(h3) % 2))
    h3 = bytearray_to_bitstring(bytearray.fromhex(h3)).zfill(32)
    h3_variable: List[ConjunctiveNormalForm.Variable] = []
    for h3_bit in h3:
        variable_to_append = ConjunctiveNormalForm.Variable()
        if h3_bit == "0":
            variable_to_append.set_truth_value(False)
        elif h3_bit == "1":
            variable_to_append.set_truth_value(True)
        else:
            raise ValueError("Error: h3_bit contain symbol other than 0 and 1")
        h3_variable.append(variable_to_append)
    h4 = 0x510e527f
    h4 = hex(h4)[2:]
    h4 = h4.zfill(len(h4) + (len(h4) % 2))
    h4 = bytearray_to_bitstring(bytearray.fromhex(h4)).zfill(32)
    h4_variable: List[ConjunctiveNormalForm.Variable] = []
    for h4_bit in h4:
        variable_to_append = ConjunctiveNormalForm.Variable()
        if h4_bit == "0":
            variable_to_append.set_truth_value(False)
        elif h4_bit == "1":
            variable_to_append.set_truth_value(True)
        else:
            raise ValueError("Error: h4_bit contain symbol other than 0 and 1")
        h4_variable.append(variable_to_append)
    h5 = 0x9b05688c
    h5 = hex(h5)[2:]
    h5 = h5.zfill(len(h5) + (len(h5) % 2))
    h5 = bytearray_to_bitstring(bytearray.fromhex(h5)).zfill(32)
    h5_variable: List[ConjunctiveNormalForm.Variable] = []
    for h5_bit in h5:
        variable_to_append = ConjunctiveNormalForm.Variable()
        if h5_bit == "0":
            variable_to_append.set_truth_value(False)
        elif h5_bit == "1":
            variable_to_append.set_truth_value(True)
        else:
            raise ValueError("Error: h5_bit contain symbol other than 0 and 1")
        h5_variable.append(variable_to_append)
    h6 = 0x1f83d9ab
    h6 = hex(h6)[2:]
    h6 = h6.zfill(len(h6) + (len(h6) % 2))
    h6 = bytearray_to_bitstring(bytearray.fromhex(h6)).zfill(32)
    h6_variable: List[ConjunctiveNormalForm.Variable] = []
    for h6_bit in h6:
        variable_to_append = ConjunctiveNormalForm.Variable()
        if h6_bit == "0":
            variable_to_append.set_truth_value(False)
        elif h6_bit == "1":
            variable_to_append.set_truth_value(True)
        else:
            raise ValueError("Error: h6_bit contain symbol other than 0 and 1")
        h6_variable.append(variable_to_append)
    h7 = 0x5be0cd19
    h7 = hex(h7)[2:]
    h7 = h7.zfill(len(h7) + (len(h7) % 2))
    h7 = bytearray_to_bitstring(bytearray.fromhex(h7)).zfill(32)
    h7_variable: List[ConjunctiveNormalForm.Variable] = []
    for h7_bit in h7:
        variable_to_append = ConjunctiveNormalForm.Variable()
        if h7_bit == "0":
            variable_to_append.set_truth_value(False)
        elif h7_bit == "1":
            variable_to_append.set_truth_value(True)
        else:
            raise ValueError("Error: h7_bit contain symbol other than 0 and 1")
        h7_variable.append(variable_to_append)
    for message_block in blocks:
        message_schedule: List[List[ConjunctiveNormalForm.Variable]] = []
        for t in range(0, 64):
            if t <= 15:
                # adds the t'th 32 bit word of the block,
                # starting from leftmost word
                # 4 bytes at a time
                message_schedule.append(message_block[t * 4 * 8:(t * 4 * 8) + 4 * 8])
            else:
                term1 = sigma1(message_schedule[t - 2])
                result_formula.list_of_clause.extend(term1[1])
                term1 = term1[0]
                term2 = message_schedule[t - 7]
                term3 = sigma0(message_schedule[t - 15])
                result_formula.list_of_clause.extend(term3[1])
                term3 = term3[0]
                term4 = message_schedule[t - 16]

                if len(term1) != len(term2):
                    raise ValueError("Error: len(term1) != len(term2)")
                if len(term1) != len(term3):
                    raise ValueError("Error: len(term1) != len(term3)")
                if len(term1) != len(term4):
                    raise ValueError("Error: len(term1) != len(term4)")
                schedule = binary_addition_multiple_input_same_size([
                    term1, term2, term3, term4
                ], append_carry_at_last=False)
                result_formula.list_of_clause.extend(schedule[1])
                schedule = schedule[0]

                message_schedule.append(schedule)
        assert len(message_schedule) == 64
        # Initialize working variables
        a = h0_variable
        b = h1_variable
        c = h2_variable
        d = h3_variable
        e = h4_variable
        f = h5_variable
        g = h6_variable
        h = h7_variable
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
        K_binary = []
        for hex_number in K:
            to_append = hex(hex_number)[2:]
            to_append = to_append.zfill(len(to_append) + (len(to_append) % 2))
            to_append = bytearray_to_bitstring(bytearray.fromhex(to_append)).zfill(32)
            K_binary.append(to_append)
        satisfiability_K: List[List[Union[ConjunctiveNormalForm.Literal, ConjunctiveNormalForm.Variable]]] = []
        for hex_number_bitstring in K_binary:
            if len(hex_number_bitstring) != 32:
                raise ValueError("Error: hex_number_bitstring bitlength is not 32")
            else:
                K_element: List[Union[ConjunctiveNormalForm.Variable]] = \
                    [ConjunctiveNormalForm.Variable() for i in range(32)]
                for i in range(32):
                    if hex_number_bitstring[i] == "0":
                        K_element[i].set_truth_value(False)
                    elif hex_number_bitstring[i] == "1":
                        K_element[i].set_truth_value(True)
                    else:
                        raise ValueError("K_element_bitstring contain symbol other than 0 and 1")
                satisfiability_K.append(K_element)
        # Iterate for t=0 to 63
        for t in range(64):
            t1_capsigma1 = capsigma1(e)
            result_formula.list_of_clause.extend(t1_capsigma1[1])
            t1_capsigma1 = t1_capsigma1[0]
            t1_ch = ch(e, f, g)
            result_formula.list_of_clause.extend(t1_ch[1])
            t1_ch = t1_ch[0]
            t1 = binary_addition_multiple_input_same_size([
                h,
                t1_capsigma1,
                t1_ch,
                satisfiability_K[t],
                message_schedule[t]
            ], append_carry_at_last=False)
            result_formula.list_of_clause.extend(t1[1])
            t1 = t1[0]

            # t2 = binary_addition_zfill_multiple(
            #                 [_capsigma0_binary(a), _maj_binary_correct_size(a, b, c)], min_bitlength=32, max_bitlength=32)
            t2_capsigma0 = capsigma0(a)
            result_formula.list_of_clause.extend(t2_capsigma0[1])
            t2_capsigma0 = t2_capsigma0[0]
            t2_maj = maj(a, b, c)
            result_formula.list_of_clause.extend(t2_maj[1])
            t2_maj = t2_maj[0]
            t2 = binary_addition_two_input_same_size(
                t2_capsigma0,
                t2_maj)
            result_formula.list_of_clause.extend(t2[1])
            t2 = t2[0]

            # h = g
            h = g
            # g = f
            g = f
            # f = e
            f = e

            # e = binary_addition_zfill(d, t1, min_bitlength=32, max_bitlength=32)
            e = binary_addition_two_input_same_size(d,
                                                    t1,
                                                    append_carry_at_last=False)
            result_formula.list_of_clause.extend(e[1])
            e = e[0]

            # d = c
            d = c
            # c = b
            c = b
            # b = a
            b = a

            # a = binary_addition_zfill(t1, t2, min_bitlength=32, max_bitlength=32)
            a = binary_addition_two_input_same_size(t1,
                                                    t2,
                                                    append_carry_at_last=False)
            result_formula.list_of_clause.extend(a[1])
            a = a[0]
        # Compute intermediate hash value
        h0_addition = binary_addition_two_input_same_size(
            h0_variable,
            a,
            append_carry_at_last=False)
        result_formula.list_of_clause.extend(h0_addition[1])
        h0_variable = h0_addition[0]
        h0_addition = None
        h1_addition = binary_addition_two_input_same_size(
            h1_variable,
            b,
            append_carry_at_last=False)
        result_formula.list_of_clause.extend(h1_addition[1])
        h1_variable = h1_addition[0]
        h1_addition = None
        h2_addition = binary_addition_two_input_same_size(
            h2_variable,
            c,
            append_carry_at_last=False)
        result_formula.list_of_clause.extend(h2_addition[1])
        h2_variable = h2_addition[0]
        h2_addition = None
        h3_addition = binary_addition_two_input_same_size(
            h3_variable,
            d,
            append_carry_at_last=False)
        result_formula.list_of_clause.extend(h3_addition[1])
        h3_variable = h3_addition[0]
        h3_addition = None
        h4_addition = binary_addition_two_input_same_size(
            h4_variable,
            e,
            append_carry_at_last=False)
        result_formula.list_of_clause.extend(h4_addition[1])
        h4_variable = h4_addition[0]
        h4_addition = None
        h5_addition = binary_addition_two_input_same_size(
            h5_variable,
            f,
            append_carry_at_last=False)
        result_formula.list_of_clause.extend(h5_addition[1])
        h5_variable = h5_addition[0]
        h5_addition = None
        h6_addition = binary_addition_two_input_same_size(
            h6_variable,
            g,
            append_carry_at_last=False)
        result_formula.list_of_clause.extend(h6_addition[1])
        h6_variable = h6_addition[0]
        h6_addition = None
        h7_addition = binary_addition_two_input_same_size(
            h7_variable,
            h,
            append_carry_at_last=False)
        result_formula.list_of_clause.extend(h7_addition[1])
        h7_variable = h7_addition[0]
        h7_addition = None
    result_output_variable: List[ConjunctiveNormalForm.Variable] = []
    result_output_variable.extend(h0_variable)
    result_output_variable.extend(h1_variable)
    result_output_variable.extend(h2_variable)
    result_output_variable.extend(h3_variable)
    result_output_variable.extend(h4_variable)
    result_output_variable.extend(h5_variable)
    result_output_variable.extend(h6_variable)
    result_output_variable.extend(h7_variable)
    return result_input_variable, result_output_variable, result_formula


def generate_hash(message: bytearray) -> bytes:
    if type(message) != bytearray:
        raise TypeError("Error: message data type is not byte array")
    message = bytearray_to_bitstring(message)
    message_length = len(message)
    result_formula = generate_sha256_formula(message_length)
    result_formula_input_variable = result_formula[0]
    result_formula_output_variable = result_formula[1]
    result_formula = result_formula[2]
    if len(result_formula_input_variable) != message_length:
        raise ValueError("Error: len(result_formula_input_variable) != message_length")
    for i in range(message_length):
        if message[i] == "0":
            result_formula_input_variable[i].set_truth_value(False)
        elif message[i] == "1":
            result_formula_input_variable[i].set_truth_value(True)
        else:
            raise ValueError("Error: message[i] contain symbol other than 0 and 1")
    result_formula.solve_as_one_satisfiability(set_truth_value_inplace=True)
    result_bitstring_char_list: List[str] = []
    # 0 or 1 represent truth value
    # 2 represent that it can be either 0 or 1
    for literal_or_variable in result_formula_output_variable:
        if type(literal_or_variable.get_truth_value()) == bool:
            if literal_or_variable.get_truth_value():
                result_bitstring_char_list.append("1")
            else:
                result_bitstring_char_list.append("0")
        else:
            raise ValueError("Error: output contain symbol other than 0 and 1, got type ",
                             type(literal_or_variable.get_truth_value()))
            # result_bitstring_char_list.append("2")
    result_bitstring = "".join(result_bitstring_char_list)
    result = int(result_bitstring, 2).to_bytes(32, 'big')
    return result
