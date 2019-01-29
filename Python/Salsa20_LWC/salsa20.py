from functions import quarterround, rowround, columnround

test_vector = [0, 0, 1, 0]

rowround_test_vector = [1,0,0,0,
						1,0,0,0,
						1,0,0,0,
						1,0,0,0]

# print quarterround(*test_vector)

# print rowround(rowround_test_vector)

print columnround(rowround_test_vector)
