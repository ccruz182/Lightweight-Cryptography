'''
  File name: /block_ciphers/granule/cipher.py
  Author: Cesar Cruz
  Project: cryptofeather
  Python Version: 2.7
'''

import numpy

from boxes import SBOX, PBOX, ROUNDS, PBOX_2
from utils.others import get_fragment_int, int_to_bin, pretty_print
from utils.crypto import sbox_operation

# Cipher method.
def _cipher(plaintext, keys):
	# Plaintext is divided in two
	pt1 = plaintext[0:32]
	pt0 = plaintext[32:]

	f = open("granule64_128.txt", "w")
	f.write("Plaintext: " + pretty_print(plaintext, len(plaintext)) + "\n")

	# 32 rounds of the algorithm
	for i in range(ROUNDS):
		f.write("Ronda " + str(i) + "\n")
		f.write("\tLlave: " + pretty_print(keys[i], len(keys[i])) + "\n")
		# Execution of f function
		f_return, res  = f_function(pt1)

		f.write("\tSalida de f: " + pretty_print(f_return, len(f_return)) + "\n")
		f.write("\t\tPlayer: " + pretty_print(res[0], len(res[0])) + "\n")
		f.write("\t\tSbox: " + pretty_print(res[1], len(res[1])) + "\n")
		f.write("\t\tRP: " + pretty_print(res[2], len(res[2])) + "\n")

		# Add round key operation
		#print "pt0", pt0
		#print "key", keys[i]	
		temp = add_round_key(pt0, f_return, keys[i])
		f.write("\tSalida de add_round_key: " + pretty_print(temp, len(temp)) + "\n")	
		#print "temp", temp
		
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

	f.write("\n\nCIFRADO: " + pretty_print(pt1 + pt0, len(pt1+pt0)))
	return pt1 + pt0	

# Decipher method.
def _decipher(ciphertext, keys):
	# It is necessary to exchange position, due to how the cipher text is entered
	pt0 = ciphertext[0:32]
	pt1 = ciphertext[32:]

	# 32 rounds of the algorithm
	for i in range(ROUNDS):
		# Execution of f funcion
		f_return, x = f_function(pt1)	

		# Add round key operation	
		temp = add_round_key(pt0, f_return, keys[ROUNDS - 1 - i])

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

	return pt0 + pt1	

def f_function(pt1):	
	# First. p_layer	
	res = []
	new_state = p_layer2(pt1[:])	
	res.append(new_state[:])		
	
	# Then, sbox_layer
	new_state = sbox_layer(new_state[:])		
	res.append(new_state[:])

	# Next step, rp_layer
	new_state = rp_layer(new_state[:])
	res.append(new_state[:])	

	
	return new_state, res

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

def p_layer2(state):
	new_state = [0] * 32

	for i in range(len(new_state) / 4):
		mark = PBOX_2[i]
		offset = mark * 4;
		ns_o = 4 * i
		new_state[ns_o:ns_o+4] = state[offset:offset+4]

	return new_state



# Operation: sbox_layer
def sbox_layer(state):
	return sbox_operation(SBOX, state)

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


