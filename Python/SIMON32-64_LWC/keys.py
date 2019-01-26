'''
  File name: keys.py
  Author: Cesar Cruz Arredondo
  Project: SIMON32-64_LWC
  Python Version: 2.7
'''

import numpy

from definitions import N, M, T, J, Z
from operations import rotation, xor, _not, expand_bit

def key_expansion(key_words):
	keys = init_keys(key_words)

	for i in range(M, T):			
		tmp = rotation(keys[i - 1], -3)
		tmp = xor(tmp, keys[i - 3])
		tmp = xor(tmp, rotation(tmp, -1))

		not_k = _not(keys[i - M])
		tmp = xor(not_k, tmp)
		tmp = xor(tmp, [0 if x < 14 else 1 for x in range(16)])	
		z_expand = expand_bit(Z[i - M], 15)				
		tmp = xor(tmp, z_expand)
		
		keys.append(tmp)
	
	return keys

def init_keys(key_words):
	keys = []
	keys.append(key_words[48:])
	keys.append(key_words[32:48])
	keys.append(key_words[16:32])
	keys.append(key_words[:16])

	return keys
