SBOX = [12, 5, 6, 11, 9, 0, 10, 13, 3, 14, 15, 8, 4, 7, 1, 2]


def generate_pbox():
	pbox = []
	for i in range(16):
		act = i
		for j in range(4):	
			pbox.append(act)
			act = act + 16

	return pbox