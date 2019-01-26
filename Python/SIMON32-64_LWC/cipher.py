'''
  File name: cipher.py
  Author: Cesar Cruz Arredondo
  Project: SIMON32-64_LWC
  Python Version: 2.7
'''

from definitions import N, T
from operations import rotation, xor, _not, expand_bit, _and

def cipher(plaintext, keys):
	x = plaintext[:N]
	y = plaintext[N:]

	for i in range(T):
		temp = x

		temp_x = xor(y, rotation(x, 2))
		temp_x = xor(temp_x, keys[i])
		temp_x = xor(temp_x, _and(rotation(x, 1), rotation(x, 8)))

		x = temp_x
		y = temp

	return x + y