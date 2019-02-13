'''
  File name: /ciphers/block_ciphers/present/cipher.py
  Author: Cesar Cruz
  Project: cryptofeather
  Python Version: 2.7
'''

import numpy

from boxes import SBOX, generate_pbox
from utils.crypto import sbox_operation, permutation_layer

# Cipher method.
def _cipher(plaintext, keys):
	state = plaintext

	# Generation of PBOX, used in p_layer
	pbox = generate_pbox()

	# Rounds of the algorithm.
	for i in range(1, 32):
			
		state = add_round_key(state, keys[i - 1])
		
		state = sbox_layer(state)		

		state = p_layer(state, pbox)
		
	return add_round_key(state, keys[i]) # The last operation of the cipher operation

# Operation: add_round_key
def add_round_key(state, key):
	new_state = []

	# X-OR operation, bit per bit.
	for i in range(len(state)): 
		new_state.append(state[i] ^ key[i])

	return new_state

# Operation: sbox_layer
def sbox_layer(state):
  return sbox_operation(SBOX, state)

# Operation: p_layer
def p_layer(state, pbox):
	return permutation_layer(pbox, state)