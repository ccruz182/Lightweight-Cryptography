import numpy

def quarterround(y0, y1, y2, y3):
	z1 = y1 ^ (rotation(suma(y0, y3), -7))
	z2 = y2 ^ (rotation(suma(z1, y0), -9))
	z3 = y3 ^ (rotation(suma(z2, z1), -13))
	z0 = y0 ^ (rotation(suma(z3, z2), -18))

	return z0, z1, z2, z3

def rowround(y):
	z = [0] * 16
	z[0], z[1], z[2], z[3] = quarterround(y[0], y[1], y[2], y[3])
	z[5], z[6], z[7], z[4] = quarterround(y[5], y[6], y[7], y[4])
	z[10], z[11], z[8], z[9] = quarterround(y[10], y[11], y[8], y[9])
	z[15], z[12], z[13], z[14] = quarterround(y[15], y[12], y[13], y[14])

	return z

def columnround(x):
	y = [0] * 16
	y[0], y[4], y[8], y[12] = quarterround(x[0], x[4], x[8], x[12])
	y[5], y[9], y[13], y[1] = quarterround(x[5], x[9], x[13], x[1])
	y[10], y[14], y[2], y[6] = quarterround(x[10], x[14], x[2], x[6])
	y[15], y[3], y[7], y[11] = quarterround(x[15], x[3], x[7], x[11])

	return y

def suma(a, b):
	return (a + b) % pow(2, 32)

def rotation(number, times):
	array_number = list(numpy.binary_repr(number, 32))
	rotated = numpy.roll(array_number, times)
	
	return int(rotated.tostring(), 2)
