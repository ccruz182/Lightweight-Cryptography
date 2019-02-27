'''
  File name: example.py
  Author: Cesar Cruz
  Project: cryptofeather
  Python Version: 2.7
'''

from ciphers.block_ciphers.anu import Anu
from ciphers.block_ciphers.gift import Gift
from ciphers.block_ciphers.granule import Granule
from ciphers.block_ciphers.present import Present
from utils.others import pretty_print

from ciphers.block_ciphers.sparx import speckey, keys, cipher
from ciphers.block_ciphers.sea.keys import key_schedule

from ciphers.block_ciphers.anu2 import Anu2

"""
print "** ANU **"
anu = Anu.Anu()
anu.set_key([0] * 128)
anu.set_plaintext([0] * 64)
print pretty_print(anu.cipher(), 64)
"""

"""
print "** GIFT **"
gift  = Gift.Gift()
gift.set_key([1] * 128)
gift.set_plaintext([0] * 64)
print pretty_print(gift.cipher(), 64)
print pretty_print(gift.decipher(), 64)
"""

"""
print "** GRANULE **"
granule = Granule.Granule()
granule.set_key([1] * 128)
granule.set_plaintext([1] * 64)
print pretty_print(granule.cipher(), 64)
print pretty_print(granule.decipher(), 64)
"""

"""
print "** PRESENT **"
present = Present.Present()
present.set_key([0] * 80)
present.set_plaintext([0] * 64)
print pretty_print(present.cipher(), 64)
print pretty_print(present.decipher(), 64)
"""


"""
x = [0,0,0,0, 0,0,0,0, 0,0,0,0, 1,1,1,1]
y = [0,0,0,0, 0,0,0,0, 0,0,0,0, 0,1,0,0]

key = [0,0,0,0, 0,0,0,0, 0,0,0,1, 0,0,0,1,
	     0,0,1,0, 0,0,1,0, 0,0,1,1, 0,0,1,1,
       0,1,0,0, 0,1,0,0, 0,1,0,1, 0,1,0,1,
       0,1,1,0, 0,1,1,0, 0,1,1,1, 0,1,1,1,
       1,0,0,0, 1,0,0,0, 1,0,0,1, 1,0,0,1,
       1,0,1,0, 1,0,1,0, 1,0,1,1, 1,0,1,1,
       1,1,0,0, 1,1,0,0, 1,1,0,1, 1,1,0,1,
       1,1,1,0, 1,1,1,0, 1,1,1,1, 1,1,1,1]

plaintext = [0,0,0,0, 0,0,0,1, 0,0,1,0, 0,0,1,1,
              0,1,0,0, 0,1,0,1, 0,1,1,0, 0,1,1,1,
              1,0,0,0, 1,0,0,1, 1,0,1,0, 1,0,1,1,
              1,1,0,0, 1,1,0,1, 1,1,1,0, 1,1,1,1]

#print pretty_print(key, 128)
#print pretty_print(plaintext, 64)

cipher.step_structure(plaintext[:32], plaintext[32:], key)

"""

"""
a = [[0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0]]
b = [[0,0,0,0,0,0,0,1], [0,0,0,0,0,0,1,0], [0,0,0,0,0,0,1,1]]

master_key = [0] * 48
print key_schedule(master_key)
"""

anu2 = Anu2.Anu2()
anu2.set_key([0] * 128)
anu2.set_plaintext([1] * 64)
print pretty_print(anu2.cipher(), 64)
