'''
  File name: /ciphers/block_ciphers/gift/cipher.py
  Author: Cesar Cruz
  Project: cryptofeather
  Python Version: 2.7
'''
import numpy

from boxes import BLOCK_SIZE, NUMBER_OF_ROUNDS, SBOX, PBOX, CONSTANTS_28
from utils.crypto import sbox_operation, permutation_layer
from utils.others import int_to_bin, pretty_print

# Cipher method.
def _cipher(plaintext, keys):
	state = plaintext
	f = open("gift64.txt", "w")
	f.write("Texto plano: " + pretty_print(plaintext, len(plaintext)) + "\n")

	# Rounds of the algorithm.
	for i in range(0, NUMBER_OF_ROUNDS):
		f.write("Ronda " + str(i) + "\n")
		f.write("\t Llave de ronda: " + pretty_print(keys[i], len(keys[i])) + "\n")
		# f.write("\t Constante de ronda: " + )
		state = subcells(state)
		f.write("\t Salida subcells: " + pretty_print(state, len(state)) + "\n")
		
		state = permbits(state)	
		f.write("\t Salida permbits: " + pretty_print(state, len(state)) + "\n")

		state = add_round_key(state, keys[i], i)
		f.write("\t Salida add_round_key: " + pretty_print(state, len(state)) + "\n")

	return state

# Operation subcells
def subcells(state):
	return sbox_operation(SBOX, state)	

# Operation permbits
def permbits(state):
	return permutation_layer(PBOX, state)

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