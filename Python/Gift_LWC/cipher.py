'''
  File name: cipher.py
  Author: Cesar Cruz
  Project: Gift_LWC
  Python Version: 2.7
'''

import numpy

from boxes import BLOCK_SIZE, NUMBER_OF_ROUNDS, SBOX, PBOX, CONSTANTS_28

# Cipher method.
def cipher(plaintext, keys):
	state = plaintext

	# Rounds of the algorithm.
	for i in range(0, NUMBER_OF_ROUNDS):		
		state = subcells(state)
		
		state = permbits(state)	

		state = add_round_key(state, keys[i], i)

	return state

# Operation subcells
def subcells(state):
	for i in range(BLOCK_SIZE / 4):
		beg = 4 * i
		
		# Convert bin to dec
		sbox_index = get_fragment_int(state, beg, beg + 4)
		
		# SBOX operation
		state[beg:beg+4] = int_to_bin(SBOX[sbox_index], 4)

	return state

# Operation permbits
def permbits(state):
	new_state = [0] * BLOCK_SIZE
	offset = BLOCK_SIZE - 1

	# Permutation of all the bits, according to pbox
	for i in range(BLOCK_SIZE):
		new_state[offset - PBOX[i]] = state[offset - i]

	return new_state

def add_round_key(state, key, _round):	
	state_copy = state[:]
	u = key[:16]
	v = key[16:]
	c = int_to_bin(CONSTANTS_28[_round], 6)		
	offset = BLOCK_SIZE - 1
	
	for i in range(16):
		u_index = (4 * i) + 1
		v_index = 4 * i

		state_copy[offset - u_index] ^= u[15 - i]
		state_copy[offset - v_index] ^= v[15 - i]		
		
	# X-OR with constants
	state_copy.reverse() # To make easier operations	

	state_copy[BLOCK_SIZE - 1] ^= 1
	
	beg = 3
	for i in range(6):
		state_copy[beg] ^= c[5 - i]
		beg += 4

	state_copy.reverse() # Original order

	return state_copy

def pretty_print(array):
  _str = ""

  for i in range(0, 64, 4):
    _str += hex(get_fragment_int(array, i, i + 4)).split('0x')[1]

  return _str

# Method to convert a number represented in binary in decimal
def get_fragment_int(array, begin, end):
	return int("".join(map(str, array[begin:end])), 2)

# Method to convert an integer to a string, representing the binary form of the integer
def int_to_bin(number, w):
	return map(int, numpy.binary_repr(number, width=w))