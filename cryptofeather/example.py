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
from ciphers.block_ciphers.anu2 import Anu2
from utils.others import pretty_print

from ciphers.block_ciphers.sparx import Sparx

print "** ANU (Descifrado) **"
anu = Anu.Anu()
anu.set_key([0] * 128)
anu.set_plaintext([0] * 64)
ciphertext = anu.cipher()
recovered_text = anu.decipher(ciphertext)

#print "Texto plano:\t0x", pretty_print([0] * 64, 64)
#print "Llave a usar:\t0x", pretty_print([0] * 128, 128)
#print "Texto cifrado:\t\t0x", pretty_print(ciphertext, 64)
#print "Llave a usar:\t\t0x", pretty_print([0] * 128, 128)
#print "Texto descifrado:\t0x", pretty_print(recovered_text, 64)



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
granule.set_key([0] * 128)
granule.set_plaintext([0] * 64)
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



print "** ANU II**"
anu2 = Anu2.Anu2()
anu2.set_key([0] * 128)
anu2.set_plaintext([0] * 64)
#print "Texto plano:\t0x", pretty_print([0] * 64, 64)
#print "Llave a usar:\t0x", pretty_print([0] * 128, 128)
ciphertext = anu2.cipher()
#print "Texto cifrado:\t\t0x", pretty_print(ciphertext, 64)
#print "Llave a usar:\t\t0x", pretty_print([0] * 128, 128)
recovered_text = anu2.decipher(ciphertext)
#print "Texto descifrado:\t0x", pretty_print(recovered_text, 64)


"""
sparx_key = [0,0,0,0, 0,0,0,0, 0,0,0,1, 0,0,0,1, 0,0,1,0, 0,0,1,0, 0,0,1,1, 0,0,1,1,
            0,1,0,0, 0,1,0,0, 0,1,0,1, 0,1,0,1, 0,1,1,0, 0,1,1,0, 0,1,1,1, 0,1,1,1,
            1,0,0,0, 1,0,0,0, 1,0,0,1, 1,0,0,1, 1,0,1,0, 1,0,1,0, 1,0,1,1, 1,0,1,1,
            1,1,0,0, 1,1,0,0, 1,1,0,1, 1,1,0,1, 1,1,1,0, 1,1,1,0, 1,1,1,1, 1,1,1,1]

sparx_pt = [0,0,0,0, 0,0,0,1, 0,0,1,0, 0,0,1,1,
            0,1,0,0, 0,1,0,1, 0,1,1,0, 0,1,1,1,
            1,0,0,0, 1,0,0,1, 1,0,1,0, 1,0,1,1,
            1,1,0,0, 1,1,0,1, 1,1,1,0, 1,1,1,1]

print "** SPARX 64_128 ** "
print "Key:\t\t", pretty_print(sparx_key, 128)
print "Plaintext:\t", pretty_print(sparx_pt, 64)
sparx = Sparx.Sparx()
sparx.set_key(sparx_key)
sparx.set_plaintext(sparx_pt)
cipher = sparx.cipher()
print "Ciphertext:\t", pretty_print(cipher, 64)
decipher = sparx.decipher(cipher)
print "Recovered:\t", pretty_print(decipher, 64)
"""