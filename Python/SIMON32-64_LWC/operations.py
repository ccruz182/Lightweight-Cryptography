'''
  File name: operations.py
  Author: Cesar Cruz Arredondo
  Project: SIMON32-64_LWC
  Python Version: 2.7
'''

import numpy

def rotation(array, times):
	return numpy.roll(array, -(times))

def xor(v1, v2):
	return [v1[i] ^ v2[i] for i in range(len(v1))]


def _and(v1, v2):
	return [v1[i] & v2[i] for i in range(len(v1))]

def _not(v):
	one_v = [1 for i in range(16)]
	return xor(v, one_v)

def expand_bit(v, size):
	result = [0 for i in range(size)]
	result.append(v)

	return result