'''
  File name: /ciphers/block_ciphers/sparx/cipher.py
  Author: Cesar Cruz
  Project: cryptofeather
  Python Version: 2.7
'''
from utils.logic_operations import xor, rot
from utils.others import pretty_print
from constants import WORD_SIZE

from speckey import inv_arx_box1, arx_box1, arx_box
from keys import k_64, split, key_schedule

W = 2
NS = 8
RA = 3

# Example version for Sparx64_128
def _cipher(plaintext, key):
  y = []  
  keys = key_schedule(key)

  for i in range(0, len(plaintext), WORD_SIZE):
    y.append(plaintext[i:i + WORD_SIZE])

  q = 0
  for s in range(NS):
    for i in range(W):      
      for r in range(RA):        
        y[i] = xor(y[i], keys[q][r])         
        y[i] = arx_box1(y[i])        
      # End for         
      q += 1
    # End for
    y = linear_mixing(y)# Linear mixing
  # End for
  
  for i in range(W):    
    y[i] = xor(y[i], keys[q][i])
  
  return y[0] + y[1]

def _decipher(ciphertext, key):
  y = []
  keys = key_schedule(key)
  q = len(keys) - 1  

  for i in range(0, len(ciphertext), WORD_SIZE):
    y.append(ciphertext[i:i + WORD_SIZE])

  for i in range(W):
    y[i] = xor(y[i], keys[q][i])

  q -= 1
    
  for s in range(NS - 1, -1, -1):
    y = inv_linear_mixing(y)# Linear mixing 
    for i in range(W - 1, -1, -1):
      for r in range(RA - 1, -1, -1):        
        y[i] = inv_arx_box1(y[i])        
        y[i] = xor(y[i], keys[q][r])        
      # End for          
      q -= 1
    # End for
  # End for
  
  return y[0] + y[1]  

def linear_mixing(y):  
  t_y = y[:] # Example 64_128, only has 2  

  # L-Function
  tmp = [0] * 2
  tmp[0], tmp[1] = l_function(t_y[0][:WORD_SIZE / 2], t_y[0][WORD_SIZE / 2:])
    
  # X-ORs
  tmp[0] = xor(tmp[0], t_y[1][:WORD_SIZE / 2])
  tmp[1] = xor(tmp[1], t_y[1][WORD_SIZE / 2:])

  t_y[1] = t_y[0][:]
  t_y[0] = sum(tmp[:], [])
    
  return t_y

def inv_linear_mixing(y):
  t_y = y[:] # Example 64_128, only has 2  

  right_t = t_y[0]
  t_y[0] = t_y[1]

  # L-Function
  tmp = [0] * 2
  tmp[0], tmp[1] = l_function(t_y[0][:WORD_SIZE / 2], t_y[0][WORD_SIZE / 2:])

  # X-ORs
  tmp[0] = xor(tmp[0], right_t[:WORD_SIZE / 2])
  tmp[1] = xor(tmp[1], right_t[WORD_SIZE / 2:])

  t_y[1] = sum(tmp[:], [])

  return t_y

def step_structure(x0, x1, ks):
  for r in range(8):
    ks1 = k_64(ks, r + 1)
    
    # Left side
    x0l, x0r = arx_function(x0[:WORD_SIZE / 2], x0[WORD_SIZE / 2 :], 3, ks)
    x1l, x1r = arx_function(x1[:WORD_SIZE / 2], x1[WORD_SIZE / 2 :], 3, ks1)

    l_0, l_1 = l_function(x0l, x0r)

    tmp_x1l = xor(l_0, x1l)
    tmp_x1r = xor(l_1, x1r)

    x1l, x1r = x0l, x0r
    x0l, x0r = tmp_x1l, tmp_x1r

    ks = ks1

  print x0l, x0r, x1l, x1r

def arx_function(x, y, r, keys):
  ks = split(keys)
  k_i = 0

  for i in range(r):
    x = xor(x, ks[k_i])
    y = xor(y, ks[k_i + 1])
    print "xs", pretty_print(x, 16), "ys", pretty_print(y, 16)
    x, y = arx_box(x, y)
    print "x", pretty_print(x, 16), "y", pretty_print(y, 16)

    k_i += 2

  return x, y

def l_function(_0, _1):  
  tmp = xor(_0, _1)  
  tmp = rot(tmp, -8)
  _0 = xor(_0, tmp)
  _1 = xor(_1, tmp)

  return _0, _1