'''
  File name: anu.py
  Author: Cesar Cruz
  Project: cryptofeather
  Python Version: 2.7
'''

from constants import BLOCK_LENGTH, KEY_LENGTH
from keys import key_schedule_128
from cipher import cipher, pretty_print

key_1 = [0] * KEY_LENGTH
plt_1 = [0] * BLOCK_LENGTH

key_2 = [1] * KEY_LENGTH

keys_1 = key_schedule_128(key_1)
keys_2 = key_schedule_128(key_2)

ciphertext_1 = cipher(plt_1, keys_1)
ciphertext_2 = cipher(plt_1, keys_2)

print "ciphertext_1", pretty_print(ciphertext_1)
print "ciphertext_2", pretty_print(ciphertext_2)
