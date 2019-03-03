'''
  File name: /ciphers/block_ciphers/sparx/keys.py
  Author: Cesar Cruz
  Project: cryptofeather
  Python Version: 2.7
'''
from constants import WORD_SIZE, KEY_SIZE
from speckey import arx_box
from utils.others import get_fragment_int, int_to_bin, sum_mod, pretty_print

NS = 8

def key_schedule(key):
  k = []
  keys = []

  # Debug con archivos
  f = open("sparxKeys.txt", "w");

  for i in range(0, len(key), WORD_SIZE):
    k.append(key[i: i + WORD_SIZE])

  for q in range(1, 2 * NS + 2, 1):    
    keys.append(k)
    
    # File debug
    f.write("q = " + str(q) + "\n")
    
    for subk in k:
      f.write("\tsubk -> " + pretty_print(subk, len(subk)) + "\n")
    # End of debug

    k = k_64(k, q)

  f.close()
  return keys

def k_64(k, r):
  t_k = sum(k, [])

  k0l, k0r, k1l, k1r, k2l, k2r, k3l, k3r = split(t_k)  
  k0l, k0r = arx_box(k0l, k0r)

  k1l = sum_mod(get_fragment_int(k1l, 0, WORD_SIZE / 2), get_fragment_int(k0l, 0, WORD_SIZE / 2), 16)  
  k1r = sum_mod(get_fragment_int(k1r, 0, WORD_SIZE / 2), get_fragment_int(k0r, 0, WORD_SIZE / 2), 16)

  k3r = sum_mod(get_fragment_int(k3r, 0, WORD_SIZE / 2), r, 16)

  ret = k3l + int_to_bin(k3r, WORD_SIZE / 2) + k0l + k0r + int_to_bin(k1l, WORD_SIZE / 2) + int_to_bin(k1r, WORD_SIZE / 2) + k2l + k2r

  key_ret = []
  for i in range(0, len(t_k), WORD_SIZE):
    key_ret.append(ret[i: i + WORD_SIZE])

  return key_ret

def split(key):
  slices = []

  for i in range(0, KEY_SIZE, WORD_SIZE / 2):
    slices.append(key[i:i + (WORD_SIZE / 2)])

  return slices