'''
  File name: /ciphers/block_ciphers/gift/keys.py
  Author: Cesar Cruz
  Project: cryptofeather
  Python Version: 2.7
'''

import numpy

from boxes import SBOX, NUMBER_OF_ROUNDS
from utils.others import get_fragment_int, int_to_bin

# Method that generates the 28 keys of 32 bits that are used in the algorithm
def key_schedule(key):	
	keys = []
	state = key

	for i in range(NUMBER_OF_ROUNDS):
		keys.append(state[-32:]) # Get U and V [32 bits]

		# Updating
		state = update_key(state)
	
	return keys


# Method that updates the key, in each iteration of generate_round_keys method
def update_key(state):
	k1 = state[-32:-16]
	k0 = state[-16:] 
	
	k1 = list(numpy.roll(k1, 2))
	k0 = list(numpy.roll(k0, 12))

	k1 += k0	
	k1 += state

	return k1[:128]