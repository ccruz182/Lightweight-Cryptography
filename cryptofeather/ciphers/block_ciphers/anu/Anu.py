from keys import key_schedule_128
from cipher import _cipher

class Anu:
  key = []
  plaintext = []

  def set_key(self, key):
    self.key = key

  def set_plaintext(self, plaintext):
    self.plaintext = plaintext

  def cipher(self):
    sub_keys = key_schedule_128(self.key)
    return _cipher(self.plaintext, sub_keys)
