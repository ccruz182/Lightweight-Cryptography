import numpy

from boxes import SBOX

# Method that generates the 32 keys of 128 bits that are used in the algorithm
def generate_round_keys(key):
	keys = []	

	for i in range(0, 32):			
		c, key = update_key(key, i)		
		keys.append(c)		

	return keys


# Method that updates the key, in each iteration of generate_round_keys method
def update_key(current_key, round_counter):
	# First step. Left rotation of the current key in 31 bits.
	new_key = numpy.roll(current_key, -31)		

	# Second step. 
	sbox_index = get_fragment_int(new_key, 124, 128)
	new_key[124:128] = int_to_bin(SBOX[sbox_index], 4)

	# Third step. 
	sbox_index = get_fragment_int(new_key, 120, 124)
	new_key[120:124] = int_to_bin(SBOX[sbox_index], 4)

	# Forth step.
	chunk = get_fragment_int(new_key, 57, 62)
	new_key[57:62] = int_to_bin(chunk ^ (round_counter % 32), 5)	
	
	return list(current_key)[-32:], list(new_key)
	
def get_fragment_int(array, begin, end):
	return int("".join(map(str, array[begin:end])), 2)

def int_to_bin(number, w):
	return map(int, numpy.binary_repr(number, width=w))