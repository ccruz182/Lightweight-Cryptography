'''
  File name: boxes.py
  Author: Cesar Cruz
  Project: Gift_LWC
  Python Version: 2.7
'''

BLOCK_SIZE = 64
NUMBER_OF_ROUNDS = 28
KEY_SIZE = 128

# Definition of the SBOX, used in subcells method
SBOX = [1, 10, 4, 12, 6, 15, 3, 9, 2, 13, 11, 7, 5, 0, 8, 14]
SBOX_INV = [13, 0, 8, 6, 2, 12, 4, 11, 14, 7, 1, 10, 3, 9, 15, 5]

# Definition of the PBOX, used in Permbits method
PBOX = [0, 17, 34, 51, 48, 1, 18, 35, 32, 49, 2, 19, 16, 33, 50, 3,
		4, 21, 38, 55, 52, 5, 22, 39, 36, 53, 6, 23, 20, 37, 54, 7,
		8, 25, 42, 59, 56, 9, 26, 43, 40, 57, 10, 27, 24, 41, 58, 11,
		12, 29, 46, 63, 60, 13, 30, 47, 44, 61, 14, 31, 28, 45, 62, 15]

PBOX_INV = [0, 5, 10, 15, 16, 21, 26, 31, 32, 37, 42, 47, 48, 53, 58, 63,
			12, 1, 6, 11, 28, 17, 22, 27, 44, 33, 38, 43, 60, 49, 54, 59,
			8, 13, 2, 7, 24, 29, 18, 23, 40, 45, 34, 39, 56, 61, 50, 55,
			4, 9, 14, 3, 20, 25, 30, 19, 36, 41, 46, 35, 52, 57, 62, 51]

# Definition of the NUMBER_OF_ROUNDS constants
CONSTANTS = [0x01, 0x03, 0x07, 0x0f, 0x1f, 0x3e, 0x3d, 0x3b, 0x37, 0x2f, 0x1e, 0x3c, 0x39, 0x33, 0x27, 0x0e,
			0x1d, 0x3a, 0x35, 0x2b, 0x16, 0x2c, 0x18, 0x30, 0x21, 0x02, 0x05, 0x0b, 0x17, 0x2e, 0x1c, 0x38,
			0x31, 0x23, 0x06, 0x0d, 0x1b, 0x36, 0x2d, 0x1a, 0x34, 0x29, 0x12, 0x24, 0x08, 0x11, 0x22, 0x04]

CONSTANTS_28 = CONSTANTS[:28]
