'''
  File name: /ciphers/block_ciphers/present/keys.py
  Author: Cesar Cruz
  Project: cryptofeather
  Python Version: 2.7
'''

import numpy

from boxes import SBOX
from utils.others import get_fragment_int, int_to_bin

# Method that generates the 32 keys of 80 bits that are used in the algorithm
def key_schedule(key):
	keys = []	

	for i in range(1, 33):			
		c, key = update_key(key, i)		
		keys.append(c)		

	return keys


# Method that updates the key, in each iteration of generate_round_keys method
def update_key(current_key, round_counter):
	# First step. Left rotation of the current key in 61 bits.
	new_key = numpy.roll(current_key, -61)		

	# Second step. Four most significant bits of new_key into SBOX.
	sbox_index = get_fragment_int(new_key, 0, 4)
	new_key[0:4] = int_to_bin(SBOX[sbox_index], 4)

	# Third step. Bits 19-15 X-OR with round_counter
	chunk = get_fragment_int(new_key, -20, -15)
	new_key[-20:-15] = int_to_bin(chunk ^ (round_counter % 32), 5)	
	
	return list(current_key)[0:64], list(new_key)
	