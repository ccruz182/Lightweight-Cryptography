'''
  File name: present.py
  Author: Cesar Cruz
  Project: Present_LWC
  Python Version: 2.7
'''

from keys import generate_round_keys
from cipher import cipher
from decipher import decipher


key = [0] * 80

plaintext = [0] * 64

# key = [1] * 80

# plaintext = [1] * 64

# First of all, generate all the keys, based on the user key
keys = generate_round_keys(key)

""" 
	** Cipher ** 
"""
ciphertext = cipher(plaintext, keys)

print "Cipher", ciphertext


""" 
	** Decipher ** 
"""
recovered_text = decipher(ciphertext, keys)
print "Recover", recovered_text
