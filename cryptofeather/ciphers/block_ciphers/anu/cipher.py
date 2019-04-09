'''
  File name: /ciphers/block_ciphers/anu/cipher.py
  Author: Cesar Cruz
  Project: cryptofeather
  Python Version: 2.7
'''

import numpy

from constants import BLOCK_LENGTH, KEY_LENGTH, NUMBER_OF_ROUNDS, SBOX, PBOX, SBOX_INV
from utils.logic_operations import xor
from utils.crypto import sbox_operation, permutation_layer, generate_pboxinv
from utils.others import pretty_print


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

def _decipher(ciphertext, keys):
  pl = ciphertext[:(BLOCK_LENGTH / 2)]
  pr = ciphertext[(BLOCK_LENGTH / 2):]
  pbox_inv = generate_pboxinv(PBOX)  

  for i in range(NUMBER_OF_ROUNDS - 1, -1, -1):
    # Swap
    tmp_pl = pl
    pl = pr
    pr = tmp_pl    

    # Capa de permutacion
    pl = permutation_layer(pbox_inv, pl)
    pr = permutation_layer(pbox_inv, pr)
        
    # Funcion f
    f1, f2 = f_function(pl)

    # Operaciones X-OR
    pr = xor(pr, xor(f2, keys[i]))
    pr = xor(pr, f1)

  return pl + pr


def f_function(pl):
  f1 = list(numpy.roll(pl, -3))
  f2 = list(numpy.roll(pl, 8))
  
  f1 = sbox_operation(SBOX, f1)
  f2 = sbox_operation(SBOX, f2)

  return f1, f2