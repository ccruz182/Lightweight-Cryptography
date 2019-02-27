'''
  File name: /ciphers/block_ciphers/sparx/keys.py
  Author: Cesar Cruz
  Project: cryptofeather
  Python Version: 2.7
'''
from constants import WORD_SIZE, KEY_SIZE
from speckey import arx_box
from utils.others import get_fragment_int, int_to_bin, sum_mod

def k_64(k, r):
  k0l, k0r, k1l, k1r, k2l, k2r, k3l, k3r = split(k)
  
  k0l, k0r = arx_box(k0l, k0r)

  k1l = sum_mod(get_fragment_int(k1l, 0, WORD_SIZE / 2), get_fragment_int(k0l, 0, WORD_SIZE / 2), 16)
  k1r = sum_mod(get_fragment_int(k1r, 0, WORD_SIZE / 2), get_fragment_int(k0r, 0, WORD_SIZE / 2), 16)

  k3r = sum_mod(get_fragment_int(k3r, 0, WORD_SIZE / 2), r, 16)

  return k3l + int_to_bin(k3r, WORD_SIZE / 2) + k0l + k0r + int_to_bin(k1l, WORD_SIZE / 2) + int_to_bin(k1r, WORD_SIZE / 2) + k2l + k2r


def split(key):
  slices = []

  for i in range(0, KEY_SIZE, WORD_SIZE / 2):
    slices.append(key[i:i + (WORD_SIZE / 2)])

  return slices