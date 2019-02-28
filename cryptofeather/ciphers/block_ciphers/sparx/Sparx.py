from cipher import _cipher

class Sparx:
  key = []
  plaintext = []

  def set_key(self, key):
    self.key = key

  def set_plaintext(self, plaintext):
    self.plaintext = plaintext

  def set_ciphertext(self, ciphertext):
    self.ciphertext = ciphertext

  def cipher(self):      
    return _cipher(self.plaintext, self.key)
