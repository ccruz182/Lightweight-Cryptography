import numpy

from boxes import SBOX, generate_pbox

def cipher(plaintext, keys):
	state = plaintext

	for i in range(1, 32):
		#print "Round", i
		#print "State:", state
		# print "Key", keys[i - 1], len(keys[i-1])		
		
		state = add_round_key(state, keys[i - 1])
		# print "add_round_key:", state
		
		state = sbox_layer(state)
		# print "sbox_layer:", state

		state = p_layer(state)
		# print "p_layer:", state

		# print "............................................"

	return add_round_key(state, keys[i])

def add_round_key(state, key):
	new_state = []

	for i in range(len(state)):
		new_state.append(state[i] ^ key[i])

	return new_state

def sbox_layer(state):
	for i in range(len(state) / 4):
		beg = 4 * i
		sbox_index = get_fragment_int(state, beg, beg + 4)
		state[beg:beg+4] = int_to_bin(SBOX[sbox_index], 4)

	return state

def p_layer(state):
	new_state = [0] * 64
	pbox = generate_pbox()


	for i in range(len(new_state)):
		new_state[pbox[i]] = state[i]

	return new_state

def get_fragment_int(array, begin, end):
	return int("".join(map(str, array[begin:end])), 2)

def int_to_bin(number, w):
	return map(int, numpy.binary_repr(number, width=w))