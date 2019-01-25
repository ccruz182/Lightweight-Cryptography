'''
  File name: boxes.py
  Author: Cesar Cruz
  Project: Granule_LWC
  Python Version: 2.7
'''

# Definition of the SBOX, used in sbox_layer method and in generate_round_keys
SBOX = [14, 7, 8, 4, 1, 9, 2, 15, 5, 10, 11, 0, 6, 12, 13, 3]

# Definition of the PBOX, used in pbox_layer
# PBOX = [4, 0, 3, 1, 6, 2, 7, 5]
PBOX = [2, 0, 5, 1, 6, 4, 7, 3]

ROUNDS = 32