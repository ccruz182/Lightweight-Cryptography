'''
  File name: /ciphers/block_ciphers/anu2/cipher.py
  Author: Cesar Cruz
  Project: cryptofeather
  Python Version: 2.7
'''

import numpy

from constants import BLOCK_LENGTH, KEY_LENGTH, NUMBER_OF_ROUNDS, SBOX
from utils.logic_operations import xor
from utils.crypto import sbox_operation
from utils.others import pretty_print

def _cipher(plaintext, keys):
  pl = plaintext[:(BLOCK_LENGTH / 2)]
  pr = plaintext[(BLOCK_LENGTH / 2):]

  for i in range(NUMBER_OF_ROUNDS):    
    # First, sbox operation and rotation
    pl = sbox_operation(SBOX, pl)    
    pr_temp = list(numpy.roll(pr, 3))

    # XOR Left
    tmp_left = xor(pl, xor(keys[i][0], pr_temp))
    pl_temp = list(numpy.roll(tmp_left, -10))

    # XOR Rigth
    pl = xor(pr, xor(pl_temp, keys[i][1]))

    pr = tmp_left

  return pl + pr
