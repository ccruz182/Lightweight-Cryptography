'''
  File name: /ciphers/block_ciphers/sparx/speckey.py
  Author: Cesar Cruz
  Project: cryptofeather
  Python Version: 2.7
'''

from utils.logic_operations import xor, rot
from utils.others import get_fragment_int, int_to_bin, sum_mod
from constants import WORD_SIZE

def arx_box(x, y):
  left = rot(x, 7)
  left = get_fragment_int(left, 0, WORD_SIZE / 2)
  t_right = get_fragment_int(y, 0, WORD_SIZE / 2)

  left = sum_mod(left, t_right, 16)
  left = int_to_bin(left, WORD_SIZE / 2)

  right = rot(y, -2)  
  right = xor(left, right)

  return left, right