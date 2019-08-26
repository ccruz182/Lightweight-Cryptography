from keys import key_schedule_128
from cipher import _cipher, _decipher, _cipher_latex, _decipher_latex

class Anu:
  key = []
  plaintext = []

  def set_key(self, key):
    self.key = key

  def set_plaintext(self, plaintext):
    self.plaintext = plaintext

  def set_ciphertext(self, ciphertext):
    self.ciphertext = ciphertext

  def cipher(self):
    sub_keys = key_schedule_128(self.key)
    return _cipher_latex(self.plaintext, sub_keys)

  def decipher(self, ciphertext):
    sub_keys = key_schedule_128(self.key)    
    return _decipher_latex(ciphertext, sub_keys)
