'''
  File name: boxes.py
  Author: Cesar Cruz
  Project: Present_LWC
  Python Version: 2.7
'''

# Definition of the SBOX and SBOX_INV, used in sbox_layer method and in generate_round_keys
SBOX = [12, 5, 6, 11, 9, 0, 10, 13, 3, 14, 15, 8, 4, 7, 1, 2]
SBOX_INV = [5, 14, 15, 8, 12, 1, 2, 13, 11, 4, 6, 3, 0, 7, 9, 10]

# Generation of PBOX, used in pbox_layer
def generate_pbox():
	pbox = []
	for i in range(16):
		act = i
		for j in range(4):	
			pbox.append(act)
			act = act + 16

	return pbox

def generate_pbox_inv():
	pbox_inv = []
	for i in range(4):
		temp = i
		for j in range(16):			
			pbox_inv.append(temp)
			temp += 4

	return pbox_inv