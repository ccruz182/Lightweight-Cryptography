'''
  File name: gift.py
  Author: Cesar Cruz
  Project: Gift_LWC
  Python Version: 2.7
'''

from keys import generate_round_keys
from cipher import cipher, pretty_print
from decipher import decipher
from boxes import BLOCK_SIZE, NUMBER_OF_ROUNDS, KEY_SIZE

key = [0] * 128
#key[18] = 1
plaintext = [0] * BLOCK_SIZE
#plaintext[0] = 0
#plaintext[38] = 0

print "plaintext\t->", pretty_print(plaintext)
# First of all, generate all the keys, based on the user key
keys = generate_round_keys(key)
ciphertext = cipher(plaintext, keys)
print "ciphertext\t->", pretty_print(ciphertext)

# Decipher
recovered = decipher(ciphertext, keys)
print "recovered\t->", pretty_print(recovered)