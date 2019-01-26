'''
  File name: simon32-64.py
  Author: Cesar Cruz Arredondo
  Project: SIMON32-64_LWC
  Python Version: 2.7
'''

from keys import key_expansion
from cipher import cipher

# Values of the paper (test vector)
key = [0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0,
		0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0 ,0,
		0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0 ,0, 0,
		0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0 ]

plaintext = [0,1,1,0, 0,1,0,1, 0,1,1,0, 0,1,0,1,
			0,1,1,0, 1,0,0,0, 0,1,1,1, 0,1,1,1]

keys = key_expansion(key)

ciphertext = cipher(plaintext, keys)

print "ciphertext", ciphertext