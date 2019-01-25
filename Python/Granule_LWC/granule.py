'''
  File name: granule.py
  Author: Cesar Cruz
  Project: Granule_LWC
  Python Version: 2.7
'''

from keys import generate_round_keys
from cipher import cipher, decipher


plaintext = [0] * 64
key = [0] * 128

# First of all, generate all the keys, based on the user key.
keys = generate_round_keys(key)

# Cipher
ct1, ct0 = cipher(plaintext, keys)
ciphertext = ct1 + ct0
print "cipher", ciphertext

# Decipher
pt1, pt0 = decipher(ciphertext, keys)
pt = pt1 + pt0
print "recovered", pt

"""
# Cipher the plaint text with the keys generated in the last step
ciphertext = cipher(plaintext, keys)

# Just for a better printing
ciphertext = "".join(map(str, ciphertext))

for i in range(len(ciphertext) / 4):
	a = 4 * i
	print ciphertext[a:a+4]
"""
