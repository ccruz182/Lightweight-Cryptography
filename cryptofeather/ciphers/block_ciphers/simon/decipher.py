'''
  File name: decipher.py
  Author: Cesar Cruz Arredondo
  Project: SIMON32-64_LWC
  Python Version: 2.7
'''

from definitions import N, T
from operations import rotation, xor, _not, expand_bit, _and

def decipher(ciphertext, keys):
	x = ciphertext[:N]
	y = ciphertext[N:]

	for i in range(T):
		temp = y

		temp_y = xor(x, rotation(y, 2))
		temp_y = xor(temp_y, keys[T - 1 - i])
		temp_y = xor(temp_y, _and(rotation(y, 1), rotation(y, 8)))
		
		x = temp
		y = temp_y

	return x + y