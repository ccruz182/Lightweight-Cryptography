'''
  File name: cipher.py
  Author: Cesar Cruz
  Project: Granule_LWC
  Python Version: 2.7
'''

import numpy

from boxes import SBOX, PBOX, PBOX_INV

# Cipher method.
def cipher(plaintext, keys):
	# Plaintext is divided in two
	pt1 = plaintext[0:32]
	pt0 = plaintext[32:]

	# 32 rounds of the algorithm
	for i in range(32):
		# Execution of f function
		f_return  = f_function(pt1)

		# Add round key operation		
		temp = add_round_key(pt0, f_return, keys[i])	
		
		"""
		print i
		print "pt0", pt0
		print "ptX", pt1
		print "f_r", f_return
		print "kys", keys[i]
		print "............"
		"""

		# Exchange position of the chunks
		pt0 = pt1
		pt1 = temp

	return pt1, pt0	

# Decipher method.
def decipher(ciphertext, keys):
	# It is necessary to exchange position, due to how the cipher text is entered
	pt0 = ciphertext[0:32]
	pt1 = ciphertext[32:]

	# 32 rounds of the algorithm
	for i in range(32):
		# Execution of f funcion
		f_return  = f_function(pt1)	

		# Add round key operation	
		temp = add_round_key(pt0, f_return, keys[31 - i])

		"""
		print 31 - i		
		print "pt0", pt0
		print "ptX", pt1
		print "f_r", f_return
		print "kys", keys[31 - i]
		print "............"
		"""
		
		# Exchange position of the chunks
		pt0 = pt1
		pt1 = temp

	return pt0, pt1	

def f_function(pt1):	
	# First. p_layer
	new_state = p_layer(pt1)	

	# Then, sbox_layer
	new_state = sbox_layer(new_state)	

	# Next step, rp_layer
	new_state = rp_layer(new_state)
	
	return new_state

# Operation: p_layer
def p_layer(state):
	new_state = [0] * 32	

	# Permutation of all the bits, according to pbox
	for i in range(len(new_state) / 4):
		mark = PBOX[i]
		offset = mark * 4
		state_offset =  i * 4
		new_state[offset:offset + 4] = state[state_offset:state_offset + 4]

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

def rp_layer(state):
	# Two rotation
	temp0 = numpy.roll(state, -2)
	temp1 = numpy.roll(state, 7)
	
	# X-OR between the last operations
	y = temp0 ^ temp1
	
	return y.tolist()

# Operation: add_round_key
def add_round_key(pt0, f_ret, key):
	new_state = []

	# X-OR operation, bit per bit.
	for i in range(len(pt0)): 
		new_state.append(pt0[i] ^ f_ret[i] ^ key[i])

	return new_state

# Method to convert a number represented in binary in decimal
def get_fragment_int(array, begin, end):
	return int("".join(map(str, array[begin:end])), 2)

# Method to convert an integer to a string, representing the binary form of the integer
def int_to_bin(number, w):
	return map(int, numpy.binary_repr(number, width=w))

""" TEST """
a = []
for i in range(32):
	a.append(0)
a[0] = 1
a[31] = 1

# print f_function(a)