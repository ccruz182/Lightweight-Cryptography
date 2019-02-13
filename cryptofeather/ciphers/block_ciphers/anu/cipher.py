'''
  File name: /ciphers/block_ciphers/anu/cipher.py
  Author: Cesar Cruz
  Project: cryptofeather
  Python Version: 2.7
'''

import numpy

from constants import BLOCK_LENGTH, KEY_LENGTH, NUMBER_OF_ROUNDS, SBOX, PBOX
from utils.logic_operations import xor
from utils.crypto import sbox_operation, permutation_layer


def _cipher(plaintext, keys):
  pl = plaintext[:(BLOCK_LENGTH / 2)]
  pr = plaintext[(BLOCK_LENGTH / 2):]

  for i in range(NUMBER_OF_ROUNDS):
    f1, f2 = f_function(pl)

    pt = xor(f1, pr)    
    
    pt = xor(pt, xor(f2, keys[i]))

    pr = permutation_layer(PBOX, pl)
    pl = permutation_layer(PBOX, pt)
        
  return pl + pr

def f_function(pl):
  f1 = list(numpy.roll(pl, -3))
  f2 = list(numpy.roll(pl, 8))
  
  f1 = sbox_operation(SBOX, f1)
  f2 = sbox_operation(SBOX, f2)

  return f1, f2