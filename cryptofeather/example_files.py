from ciphers.block_ciphers.gift import Gift
from utils.others import int_to_bin, pretty_print, get_fragment_int


def read_bits_from_file(file_name):
  file_bytes = []

  with open(file_name, "rb") as the_file:
    b = the_file.read(1)
    i = 0
    while b:
      for bit in int_to_bin(ord(b), 8):
        file_bytes.append(bit)
    
      b = the_file.read(1)

  return file_bytes

def write_dec_to_file(file_name, data):
  with open(file_name, "wb") as the_file:
    for d in data:
      the_file.write(chr(d))

def bits_to_dec(data):
  new_data = []

  for i in range(0, 64, 8):
    new_data.append(get_fragment_int(data, i, i + 8))

  return new_data


#file_bytes = read_bits_from_file("the_example.txt")
file_bytes = read_bits_from_file("cipher_file.txt")

the_key = [0] * 128
the_key[10] = 1
the_key[99] = 1
the_key[40] = 1

gift = Gift.Gift()
gift.set_key(the_key)

#gift.set_plaintext(file_bytes[:64])
gift.set_ciphertext(file_bytes[:64])

#ciphertext = gift.cipher()
recovered = gift.decipher()

#cipher_file = bits_to_dec(ciphertext)
recovered_file = bits_to_dec(recovered)

#write_dec_to_file("cipher_file.txt", cipher_file)
write_dec_to_file("recovered_file.txt", recovered_file)
