'''
  File name: decipher.py
  Author: Cesar Cruz
  Project: Gift_LWC
  Python Version: 2.7
'''
import numpy

from boxes import BLOCK_SIZE, NUMBER_OF_ROUNDS, SBOX_INV, PBOX, CONSTANTS_28
from cipher import subcells, add_round_key, pretty_print, get_fragment_int, int_to_bin

def decipher(ciphertext, keys):
	state = ciphertext

	for i in range(NUMBER_OF_ROUNDS - 1, -1, -1):
		state = add_round_key(state, keys[i], i)
		
		state = permbits_inv(state)

		state = subcells_inv(state)
	
	return state


# Operation subcells
def subcells_inv(state):
	for i in range(BLOCK_SIZE / 4):
		beg = 4 * i
		
		# Convert bin to dec
		sbox_index = get_fragment_int(state, beg, beg + 4)
		
		# SBOX operation
		state[beg:beg+4] = int_to_bin(SBOX_INV[sbox_index], 4)

	return state

# Operation permbits
def permbits_inv(state):
	new_state = [0] * BLOCK_SIZE
	offset = BLOCK_SIZE - 1

	# Permutation of all the bits, according to pbox
	for i in range(BLOCK_SIZE):
		new_state[offset - PBOX.index(i)] = state[offset - i]

	return new_state		