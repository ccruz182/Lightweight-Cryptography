'''
  File name: /ciphers/block_ciphers/sparx/speckey.py
  Author: Cesar Cruz
  Project: cryptofeather
  Python Version: 2.7
'''

from utils.logic_operations import xor, rot
from utils.others import get_fragment_int, int_to_bin, sum_mod, sub_mod
from constants import WORD_SIZE

def arx_box1(_in):
  x = _in[:WORD_SIZE / 2]
  y = _in[WORD_SIZE / 2:]

  # Right Rotation
  left = rot(x, 7)

  # Addition
  left = get_fragment_int(left, 0, WORD_SIZE / 2)
  t_right = get_fragment_int(y, 0, WORD_SIZE / 2)
  left = sum_mod(left, t_right, 16)
  left = int_to_bin(left, WORD_SIZE / 2)

  # Left rotation
  right = rot(y, -2)  
  right = xor(left, right)

  return left + right

def inv_arx_box1(_in):
  x = _in[:WORD_SIZE / 2]
  y = _in[WORD_SIZE / 2:]

  # XOR and right rotation
  y = xor(x, y)
  y = rot(y, 2)

  # substraction
  t_x = get_fragment_int(x, 0, WORD_SIZE / 2)
  t_y = get_fragment_int(y, 0, WORD_SIZE / 2)
  x = int_to_bin(sub_mod(t_x, t_y, 16), WORD_SIZE / 2)

  # Left Rotation
  x = rot(x, -7)

  return x + y

def arx_box(x, y):
  # Right Rotation
  left = rot(x, 7)

  # Addition
  left = get_fragment_int(left, 0, WORD_SIZE / 2)
  t_right = get_fragment_int(y, 0, WORD_SIZE / 2)
  left = sum_mod(left, t_right, 16)
  left = int_to_bin(left, WORD_SIZE / 2)

  # Left rotation
  right = rot(y, -2)  
  right = xor(left, right)

  return left, right