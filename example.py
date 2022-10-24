import hashlib
import sys
import Sha256Binary
import Sha256Satisfiability
from ConjunctiveNormalForm import ConjunctiveNormalForm
import string
import math
from typing import List
from typing import Tuple
from typing import Union


# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print(sys.byteorder)
    print("-- Input short --")
    test_string = "abc"
    print("Input : %s" % test_string)
    print("Input after encode: %s" % test_string.encode())
    print("Hashlib hash result\t\t\t\t: ", hashlib.sha256(test_string.encode()).digest())
    print("Sha256Binary hash result\t\t: ", Sha256Binary.generate_hash(bytearray(test_string.encode())))
    print("Sha256Satisfiability hash result: ", Sha256Satisfiability.generate_hash(bytearray(test_string.encode())))
    print("-- Input medium --")
    test_string = "abcdefghijklmnopqrstuvwxyz"
    print("Input : %s" % test_string)
    print("Input after encode: %s" % test_string.encode())
    print("Hashlib hash result\t\t\t\t: ", hashlib.sha256(test_string.encode()).digest())
    print("Sha256Binary hash result\t\t: ", Sha256Binary.generate_hash(bytearray(test_string.encode())))
    print("Sha256Satisfiability hash result: ", Sha256Satisfiability.generate_hash(bytearray(test_string.encode())))
    print("-- Input Long --")
    test_string = "abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
    print("Input : %s" % test_string)
    print("Input after encode: %s" % test_string.encode())
    print("Hashlib hash result\t\t\t\t: ", hashlib.sha256(test_string.encode()).digest())
    print("Sha256Binary hash result\t\t: ", Sha256Binary.generate_hash(bytearray(test_string.encode())))
    print("Sha256Satisfiability hash result: ", Sha256Satisfiability.generate_hash(bytearray(test_string.encode())))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
