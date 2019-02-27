'''
  File name: /block_ciphers/sea/constants
  Project: cryptofeather
  Python Version: 2.7
'''

N       = 48
B       = 8
NB      = N / (2 * B)
ROUNDS  = ((3 * N) / 4) + (2 * (NB + (B / 2)))