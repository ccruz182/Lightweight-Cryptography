'''
  File name: /ciphers/block_ciphers/anu/keys.py
  Author: Cesar Cruz
  Project: cryptofeather
  Python Version: 2.7
'''

import numpy

from constants import NUMBER_OF_ROUNDS, SBOX
from utils.others import get_fragment_int, int_to_bin, pretty_print

def key_schedule_128(key):
  round_keys = []

  for i in range(NUMBER_OF_ROUNDS):
    # First step, add the round_key
    # print "i", pretty_print(key, 128)
    round_keys.append(key[-32:])

    # Then, key_update
    key = key_update(key, i)

  return round_keys

def key_update(key, round_counter):
  # Step 1. Left rotation by 13 bits.
  new_key = numpy.roll(key, -13)

  # Step 2. S-box operation
  sbox_index = get_fragment_int(new_key, 124, 128)
  new_key[124:128] = int_to_bin(SBOX[sbox_index], 4)

  # Step 3. S-box operation
  sbox_index = get_fragment_int(new_key, 120, 124)
  new_key[120:124] = int_to_bin(SBOX[sbox_index], 4)

  # Step 4. X-OR with round_counter
  chunk = get_fragment_int(new_key, 64, 69)
  new_key[64:69] = int_to_bin(chunk ^ (round_counter % 32), 5)

  return list(new_key)