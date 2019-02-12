from ciphers.block_ciphers.anu import Anu
from ciphers.block_ciphers.gift import Gift
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