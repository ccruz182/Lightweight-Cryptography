'''
  File name: utils/logic_operations.py
  Author: Cesar Cruz
  Project: cryptofeather
  Python Version: 2.7
'''

import numpy

def _and(v1, v2):
  return [v1[i] & v2[i] for i in range(len(v1))]

def _or(v1, v2):
  return [v1[i] | v2[i] for i in range(len(v1))]

def xor(v1, v2):
  return [v1[i] ^ v2[i] for i in range(len(v1))]

# Positive -> Right
def rot(vector, times):
	return list(numpy.roll(vector, times))