'''
  File name: /ciphers/block_ciphers/anu2/keys.py
  Author: Cesar Cruz
  Project: cryptofeather
  Python Version: 2.7
'''
import numpy

from constants import NUMBER_OF_ROUNDS, SBOX
from utils.others import get_fragment_int, int_to_bin
from utils.crypto import sbox_operation
from utils.others import pretty_print


def key_schedule(key):
	round_keys = []
	the_key = key[:] # A copy of the key

	for i in range(NUMBER_OF_ROUNDS):
		# First step. Extract keys
		rk = []
		rk.append(the_key[-32:])
		rk.append(the_key[-64:-32])
		round_keys.append(rk)

		# Second step. Left circular shift by 13
		the_key = list(numpy.roll(the_key, -13))

		# Third step. SBOX of LSB 8-bits		
		the_key[-4:] = sbox_operation(SBOX, the_key[-4:])		
		the_key[-8:-4] = sbox_operation(SBOX, the_key[-8:-4])

		# Final step. XOR with round counter
		chunk = get_fragment_int(the_key, 64, 69)
		the_key[64:69] = int_to_bin(chunk ^ (i % 32), 5)


	return round_keys
