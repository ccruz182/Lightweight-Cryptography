'''
  File name: utils/others.py
  Author: Cesar Cruz
  Project: cryptofeather
  Python Version: 2.7
'''
from utils.others import get_fragment_int, int_to_bin

# S-box operation nibble by nibble
def sbox_operation(sbox, _in):
  for i in range(0, len(_in), 4):    
    sbox_index = get_fragment_int(_in, i, i + 4)
    _in[i:i+4] = int_to_bin(sbox[sbox_index], 4)

  return _in

def permutation_layer(pbox, state):
  state_copy = state[:] 
  state_copy.reverse()

  new_state = [0] * len(state_copy)
  init = len(state_copy) - 1

  # Permutation of all the bits, according to pbox
  for i in range(len(new_state)):    
    new_state[init - pbox[i]] = state_copy[i]    
  
  return new_state