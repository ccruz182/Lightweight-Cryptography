'''
  File name: decipher.py
  Author: Cesar Cruz
  Project: Present_LWC
  Python Version: 2.7
'''

import numpy

from boxes import SBOX_INV, generate_pbox_inv
from utils.crypto import sbox_operation, permutation_layer

# Cipher method.
def _decipher(plaintext, keys):
	state = plaintext

	# Generation of PBOX, used in p_layer
	pbox_inv = generate_pbox_inv()	
	
	# Rounds of the algorithm.
	for i in range(1, 32):	
		state = add_round_key(state, keys[32 - i])
		
		state = p_layer(state, pbox_inv)
		
		
		state = sbox_layer(state)
		
	return add_round_key(state, keys[0]) # The last operation of the cipher operation

# Operation: add_round_key
def add_round_key(state, key):
	new_state = []

	# X-OR operation, bit per bit.
	for i in range(len(state)): 
		new_state.append(state[i] ^ key[i])

	return new_state

# Operation: sbox_layer
def sbox_layer(state):
  return sbox_operation(SBOX_INV, state)

# Operation: p_layer
def p_layer(state, pbox):
	return permutation_layer(pbox, state)
