'''
  File name: cipher.py
  Author: Cesar Cruz
  Project: Present_LWC
  Python Version: 2.7
'''

import numpy

from boxes import SBOX, generate_pbox

# Cipher method.
def cipher(plaintext, keys):
	state = plaintext

	# Generation of PBOX, used in p_layer
	pbox = generate_pbox()

	# Rounds of the algorithm.
	for i in range(1, 32):
		#print "Round", i
		#print "State:", state
		# print "Key", keys[i - 1], len(keys[i-1])		
		
		state = add_round_key(state, keys[i - 1])
		# print "add_round_key:", state
		
		state = sbox_layer(state)
		# print "sbox_layer:", state

		state = p_layer(state, pbox)
		# print "p_layer:", state

		# print "............................................"

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

	# Each nibble enters into the SBOX
	for i in range(len(state) / 4):
		# Offset in each nibble
		beg = 4 * i
		
		# Convert bin to dec
		sbox_index = get_fragment_int(state, beg, beg + 4)
		
		# SBOX operation
		state[beg:beg+4] = int_to_bin(SBOX[sbox_index], 4)

	return state

# Operation: p_layer
def p_layer(state, pbox):
	new_state = [0] * 64

	# Permutation of all the bits, according to pbox
	for i in range(len(new_state)):
		new_state[pbox[i]] = state[i]

	return new_state

# Method to convert a number represented in binary in decimal
def get_fragment_int(array, begin, end):
	return int("".join(map(str, array[begin:end])), 2)

# Method to convert an integer to a string, representing the binary form of the integer
def int_to_bin(number, w):
	return map(int, numpy.binary_repr(number, width=w))