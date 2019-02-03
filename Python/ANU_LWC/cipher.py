'''
  File name: cipher.py
  Author: Cesar Cruz
  Project: ANU_LWC
  Python Version: 2.7
'''
import numpy

from constants import BLOCK_LENGTH, KEY_LENGTH, NUMBER_OF_ROUNDS, SBOX, PBOX

def cipher(plaintext, keys):
  pl = plaintext[:(BLOCK_LENGTH / 2)]
  pr = plaintext[(BLOCK_LENGTH / 2):]

  for i in range(NUMBER_OF_ROUNDS):
    f1, f2 = f_function(pl)

    pt = xor(f1, pr)    
    
    pt = xor(pt, xor(f2, keys[i]))

    pr = p_layer(pl)
    pl = p_layer(pt)
        
  return pl + pr

def f_function(pl):
  f1 = list(numpy.roll(pl, -3))
  f2 = list(numpy.roll(pl, 8))
  
  f1 = sbox_operation(f1)
  f2 = sbox_operation(f2)

  return f1, f2

def sbox_operation(_in):
  for i in range(0, 32, 4):    
    sbox_index = get_fragment_int(_in, i, i + 4)
    _in[i:i+4] = int_to_bin(SBOX[sbox_index], 4)

  return _in

# Operation: p_layer
def p_layer(state):
  state_copy = state[:] 
  state_copy.reverse() 
  new_state = [0] * (BLOCK_LENGTH / 2)

  # Permutation of all the bits, according to pbox
  for i in range(len(new_state)):    
    new_state[31 - PBOX[i]] = state_copy[i]    
  
  return new_state

def xor(v1, v2):
  return [v1[i] ^ v2[i] for i in range(len(v1))]

def pretty_print(array):
  _str = ""

  for i in range(0, 64, 4):
    _str += hex(get_fragment_int(array, i, i + 4)).split('0x')[1]

  return _str


def get_fragment_int(array, begin, end):
  return int("".join(map(str, array[begin:end])), 2)

def int_to_bin(number, w):
  return map(int, numpy.binary_repr(number, width=w))
