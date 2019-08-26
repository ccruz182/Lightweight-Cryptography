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

from utils.latex.table_generator import generate_table

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

def _cipher_latex(plaintext, keys):
  pl = plaintext[:(BLOCK_LENGTH / 2)]
  pr = plaintext[(BLOCK_LENGTH / 2):]

  rows = []

  for i in range(NUMBER_OF_ROUNDS):
    RK = pretty_print(keys[i], len(keys[i]))

    f1, f2 = f_function(pl)
    f1_lat = pretty_print(f1, len(f1))
    f2_lat = pretty_print(f2, len(f2))

    pt = xor(f1, pr)
    A = pretty_print(pt, len(pt))
    
    pt = xor(pt, xor(f2, keys[i]))
    B = pretty_print(pt, len(pt))
        
    pr = permutation_layer(PBOX, pl)
    C = pretty_print(pr, len(pr))
    pl = permutation_layer(PBOX, pt)
    D = pretty_print(pl, len(pl))
    
    row = [i, RK, f1_lat, f2_lat, A, B, C, D]
    rows.append(row)
  
  header_row1 = ["Ronda", "RK", "F1", "F2", "A", "B", "C", "D"]
  generate_table("ANU Cifrado", header_row1, rows, "anuCifrado")
        
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


def _decipher_latex(ciphertext, keys):
  pl = ciphertext[:(BLOCK_LENGTH / 2)]
  pr = ciphertext[(BLOCK_LENGTH / 2):]
  pbox_inv = generate_pboxinv(PBOX)

  rows = []

  for i in range(NUMBER_OF_ROUNDS - 1, -1, -1):
    RK = pretty_print(keys[i], len(keys[i]))

    # Swap
    tmp_pl = pl
    pl = pr
    pr = tmp_pl    

    A = pretty_print(pl, len(pl))
    B = pretty_print(pr, len(pr))

    # Capa de permutacion
    pl = permutation_layer(pbox_inv, pl)
    pr = permutation_layer(pbox_inv, pr)

    C = pretty_print(pl, len(pl))
    D = pretty_print(pr, len(pr))
        
    # Funcion f
    f1, f2 = f_function(pl)

    F1 = pretty_print(f1, len(f1))
    F2 = pretty_print(f2, len(f2))

    # Operaciones X-OR
    pr = xor(pr, xor(f2, keys[i]))
    E = pretty_print(pr, len(pr))
    pr = xor(pr, f1)
    F = pretty_print(pr, len(pr))

    row = [i, RK, A, B, C, D, F1, F2, E, F]
    rows.append(row)
  
  header_row1 = ["Ronda", "RK", "A", "B", "C", "D","F1", "F2", "E", "F"]
  generate_table("ANU Decifrado", header_row1, rows, "anuDecifrado")

  return pl + pr


def f_function(pl):
  f1 = list(numpy.roll(pl, -3))
  f2 = list(numpy.roll(pl, 8))
  
  f1 = sbox_operation(SBOX, f1)
  f2 = sbox_operation(SBOX, f2)

  return f1, f2