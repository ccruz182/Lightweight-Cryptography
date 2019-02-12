'''
  File name: decipher.py
  Author: Cesar Cruz
  Project: Gift_LWC
  Python Version: 2.7
'''
import numpy

from boxes import BLOCK_SIZE, NUMBER_OF_ROUNDS, SBOX_INV, PBOX_INV, CONSTANTS_28
from cipher import add_round_key
from utils.crypto import sbox_operation, permutation_layer

def _decipher(ciphertext, keys):
	state = ciphertext

	for i in range(NUMBER_OF_ROUNDS - 1, -1, -1):
		state = add_round_key(state, keys[i], i)
		
		state = permbits_inv(state)

		state = subcells_inv(state)
	
	return state


# Operation subcells
def subcells_inv(state):
	return sbox_operation(SBOX_INV, state)

# Operation permbits
def permbits_inv(state):
	return permutation_layer(PBOX_INV, state)