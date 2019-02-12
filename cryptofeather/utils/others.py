'''
  File name: utils/others.py
  Author: Cesar Cruz
  Project: cryptofeather
  Python Version: 2.7
'''
import numpy

# Print an array (in binary, just 0 and 1) in nibbles.
def pretty_print(array, lenght):
  _str = ""

  for i in range(0, lenght, 4):
    _str += hex(get_fragment_int(array, i, i + 4)).split('0x')[1]

  return _str

# Method to convert a number represented in binary in decimal
def get_fragment_int(array, begin, end):
	return int("".join(map(str, array[begin:end])), 2)

# Method to convert an integer to a string, representing the binary form of the integer
def int_to_bin(number, w):
	return map(int, numpy.binary_repr(number, width=w))