'''
  File name: /ciphers/block_ciphers/anu/constants.py
  Author: Cesar Cruz
  Project: cryptofeather
  Python Version: 2.7
'''

BLOCK_LENGTH = 64
KEY_LENGTH = 128
NUMBER_OF_ROUNDS = 25

SBOX = [2, 9, 7, 14, 1, 12, 10, 0, 4, 3, 8, 13, 15, 6, 5, 11]
PBOX = [20, 16, 28, 24, 17,21, 25, 29,
		22, 18, 30, 26, 19, 23, 27, 31,
		11, 15, 3, 7, 14, 10, 6, 2,
		9, 13, 1, 5, 12, 8, 4, 0]