import multiprocessing


def product(a, b):
	"""Computes a * b.

	We will use pool.starmap() to call this function since it
	has 2 arguments."""

	return a * b


"""Our main function. Notice that the parallel code is wrapped
inside the if __name__ == "__main__":"""
if __name__ == "__main__":
	numProcesses = 4
	
	#Create some random pairs of input numbers.
	pairs = [(1, 3), (5, 9), (2, 3), (4, 5), (10, 30), (5, 7)]

	#Calculate the product of each pair using pool.starmap()
	with multiprocessing.Pool(numProcesses) as pool:
		#Note the second argument for starmap() is a list of tuples
		products = pool.starmap(product, pairs)


		#Display our results.
		for i in range(len(pairs)):
			pair = pairs[i]

			print(f'{pair[0]} * {pair[1]} = {products[i]}.')

