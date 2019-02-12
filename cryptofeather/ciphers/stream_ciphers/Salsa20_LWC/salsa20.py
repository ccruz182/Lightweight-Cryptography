from functions import quarterround, rowround, columnround, doubleround,little_endian, salsa20

test_vector = [0, 0, 1, 0]

rowround_test_vector = [1,0,0,0,
						1,0,0,0,
						1,0,0,0,
						1,0,0,0]

doubleround_test_vector = [1,0,0,0,
							0,0,0,0,
							0,0,0,0,
							0,0,0,0]
little_endian_test_vector = [86,75,30,9]

salsa20_test_vector = [211,159,13,115,76,55,82,183,3,117,222,37,191,187,234,136,
						49,237,179,48,1,106,178,219,175,199,166,48,86,16,179,207,
						31,240,32,63,15,83,93,161,116,147,48,113,238,55,204,36,
						79,201,235,79,3,81,156,47,203,26,244,243,88,118,104,54]
salsa20_test_vector_2 = [101,120,112,97,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,
						110,100,32,49,101,102,103,104,105,106,107,108,109,110,111,112,
						113,114,115,116,54,45,98,121,1,2,3,4,5,6,7,8,
						9,10,11,12,13,14,15,16,116,101,32,107]

# print quarterround(*test_vector)

# print rowround(rowround_test_vector)

# print columnround(rowround_test_vector)

# print doubleround(doubleround_test_vector)

#print little_endian(little_endian_test_vector)

salsa20(salsa20_test_vector_2)


