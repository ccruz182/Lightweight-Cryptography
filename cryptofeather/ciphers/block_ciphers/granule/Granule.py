'''
  File name: /ciphers/block_ciphers/granule/Granule.py
  Author: Cesar Cruz
  Project: cryptofeather
  Python Version: 2.7
'''
from keys import key_schedule
from cipher import _cipher, _decipher

class Granule:
  key = []
  plaintext = []
  ciphertext = []

  def set_key(self, key):
    self.key = key

  def set_plaintext(self, plaintext):
    self.plaintext = plaintext

  def set_ciphertext(self, ciphertext):
    self.ciphertext = ciphertext

  def cipher(self):
    sub_keys = key_schedule(self.key)
    self.ciphertext = _cipher(self.plaintext, sub_keys)

    return self.ciphertext

  def decipher(self):
    sub_keys = key_schedule(self.key)
    return _decipher(self.ciphertext, sub_keys)