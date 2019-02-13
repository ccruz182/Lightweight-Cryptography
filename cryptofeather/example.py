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

print "** ANU **"
anu = Anu.Anu()
anu.set_key([0] * 128)
anu.set_plaintext([0] * 64)
print pretty_print(anu.cipher(), 64)

print "** GIFT **"
gift  = Gift.Gift()
gift.set_key([1] * 128)
gift.set_plaintext([0] * 64)
print pretty_print(gift.cipher(), 64)
print pretty_print(gift.decipher(), 64)

print "** GRANULE **"
granule = Granule.Granule()
granule.set_key([1] * 128)
granule.set_plaintext([1] * 64)
print pretty_print(granule.cipher(), 64)
print pretty_print(granule.decipher(), 64)

print "** PRESENT **"
present = Present.Present()
present.set_key([0] * 80)
present.set_plaintext([0] * 64)
print pretty_print(present.cipher(), 64)
print pretty_print(present.decipher(), 64)