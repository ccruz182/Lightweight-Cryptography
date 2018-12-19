'''
  File name: boxes.py
  Author: Cesar Cruz
  Project: Present_LWC
  Python Version: 2.7
'''

# Definition of the SBOX, used in sbox_layer method and in generate_round_keys
SBOX = [12, 5, 6, 11, 9, 0, 10, 13, 3, 14, 15, 8, 4, 7, 1, 2]

# Generation of PBOX, used in pbox_layer
def generate_pbox():
	pbox = []
	for i in range(16):
		act = i
		for j in range(4):	
			pbox.append(act)
			act = act + 16

	return pbox