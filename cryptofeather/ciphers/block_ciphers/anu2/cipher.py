'''
  File name: /ciphers/block_ciphers/anu2/cipher.py
  Author: Cesar Cruz
  Project: cryptofeather
  Python Version: 2.7
'''

import numpy

from constants import BLOCK_LENGTH, KEY_LENGTH, NUMBER_OF_ROUNDS, SBOX, SBOX_INV
from utils.logic_operations import xor
from utils.crypto import sbox_operation
from utils.others import pretty_print

def _cipher(plaintext, keys):
  pl = plaintext[:(BLOCK_LENGTH / 2)]
  pr = plaintext[(BLOCK_LENGTH / 2):]

  for i in range(NUMBER_OF_ROUNDS): 
    #print "i:", i   
    # First, sbox operation and rotation  
    #print "K1", pretty_print(keys[i][0], len(keys[i][0]))
    #print "K2", pretty_print(keys[i][1], len(keys[i][1]))

    pl = sbox_operation(SBOX, pl)  
    #print "\tA", pretty_print(pl, len(pl))
    pr_temp = list(numpy.roll(pr, 3))
    #print "\tB", pretty_print(pr_temp, len(pr_temp))   

    # XOR Left
    tmp_left = xor(pl, xor(keys[i][0], pr_temp))
    #print "\tC", pretty_print(tmp_left, len(tmp_left))
    pl_temp = list(numpy.roll(tmp_left, -10))
    #print "\tD", pretty_print(pl_temp, len(pl_temp))

    # XOR Rigth
    pl = xor(pr, xor(pl_temp, keys[i][1]))
    #print "\tE", pretty_print(pl, len(pl))

    pr = tmp_left

#    print "LEFT", pretty_print(pl, len(pl))
#    print "RIGHT", pretty_print(pr, len(pr))
#    print "--------------------\n"
  
  return pl + pr

def _decipher(ciphertext, keys):
  left = ciphertext[:(BLOCK_LENGTH / 2)]
  right = ciphertext[(BLOCK_LENGTH / 2):]  

  for i in range(NUMBER_OF_ROUNDS - 1, -1, -1):    
    # First, sbox operation and rotation  
#    print "K1", pretty_print(keys[i][0], len(keys[i][0]))
#    print "K2", pretty_print(keys[i][1], len(keys[i][1]))

    # SWAP
    tmp_left = right[:]
    right = left[:]
    left = tmp_left[:]

#    print "INIT", pretty_print(left, 32), pretty_print(right, 32)
    # ROR 10, XOR RIGHT
    pl_temp = list(numpy.roll(tmp_left, -10))
#    print "ROR Left", pretty_print(pl_temp, 32)
    right = xor(right, xor(pl_temp, keys[i][1]))
#    print "XOR Right", pretty_print(right, 32)

    # ROL 3, XOR LEFT
    pl_right = list(numpy.roll(right, 3))
    left = xor(left, xor(pl_right, keys[i][0]))

    left = sbox_operation(SBOX_INV, left)  

#    print "LEFT", pretty_print(left, len(left))
#    print "RIGHT", pretty_print(right, len(right))
#    print "--------------------\n"
  
  return left + right