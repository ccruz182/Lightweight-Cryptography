'''
  File name: utils/logic_operations.py
  Author: Cesar Cruz
  Project: cryptofeather
  Python Version: 2.7
'''

def xor(v1, v2):
  return [v1[i] ^ v2[i] for i in range(len(v1))]