'''
  File name: /block_ciphers/sea/keys.py
  Project: cryptofeather
  Python Version: 2.7
'''
import numpy

from constants import N, ROUNDS, B, NB
from utils.others import sum_mod, get_fragment_int, int_to_bin
from utils.logic_operations import xor, _and, _or

def key_schedule(master_key):
  kl = split_by_words(master_key[:(N / 2)], B)
  kr = split_by_words(master_key[(N / 2):], B) 
  KL = []
  KR = [] 
  
  for i in range(1, ROUNDS / 2, 1):
    print i
    kl_sig = kr[:]

    counter_branch = to_branch(i)
    
    tmp = sum_by_words(kr, counter_branch)
    tmp = substitution_by_words(tmp)
    tmp = bit_rotation(tmp)
    tmp = word_rotation(tmp)

    kr = xor_by_words(kl, tmp)
    kl = kl_sig[:]

    KL.append(kl)
    KR.append(kr)
  
  for i in range(ROUNDS / 2, ROUNDS, 1):
    print i


def bit_rotation(word):
  reversed_word = word[:]
  reversed_word.reverse()
  y = []

  for i in range(NB / 3):
    y.append(list(numpy.roll(reversed_word[i], 1)))
    y.append(reversed_word[i + 1])
    y.append(list(numpy.roll(reversed_word[i + 2], -1)))

  y.reverse()

  return y

def word_rotation(branch):
  y = [0] * len(branch)

  reversed_branch = branch[:]
  reversed_branch.reverse()

  for i in range(NB - 1):
    y[i + 1] = reversed_branch[i]

  y[0] = reversed_branch[NB - 1]

  y.reverse()

  return y
      
def sum_by_words(branch_1, branch_2):
  result = []

  for i in range(len(branch_1)):    
    s_res = sum_mod(get_fragment_int(branch_1[i], 0, B), get_fragment_int(branch_2[i], 0, B), B)
    result.append(int_to_bin(s_res, B))

  return result

def substitution_by_words(branch):
  reversed_branch = branch[:]
  reversed_branch.reverse()

  for i in range(NB / 3):
    base = 3 * i
    reversed_branch[base] = xor(reversed_branch[base], _and(reversed_branch[base + 2], reversed_branch[base + 1]))
    reversed_branch[base + 1] = xor(reversed_branch[base + 1], _and(reversed_branch[base + 2], reversed_branch[base]))
    reversed_branch[base + 2] = xor(reversed_branch[base + 2], _or(reversed_branch[base], reversed_branch[base +  1]))
  
  reversed_branch.reverse()

  return reversed_branch

def split_by_words(key, word_size):
  words = []

  for i in range(0, len(key), word_size):
    words.append(key[i : i + word_size])

  return words
  
def to_branch(_int):
  arr_int = int_to_bin(_int, N / 2)
  the_branch = []

  for i in range(0, N / 2, B):
    the_branch.append(arr_int[i : i + B])

  return the_branch

def xor_by_words(branch_1, branch_2):
  result = []

  for i in range(len(branch_1)):
    result.append(xor(branch_1[i], branch_2[i]))

  return result