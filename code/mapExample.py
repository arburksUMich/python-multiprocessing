import multiprocessing
import random


def toCelsius(degrees):
	"""Function to convert a temperature from Fahrenheit to Celsius."""

	return (degrees - 32) * (5.0/9.0)



"""Our main function. Notice that the parallel code is wrapped
inside the if __name__ == "__main__":"""
if __name__ == "__main__":
	numProcesses = 4

	#Generate a list of random temperatures in Fahrenheit
	temperatures = [random.uniform(32.0, 100.0) for i in range(50)]

	#Convert them in parallel using pool.map()
	with multiprocessing.Pool(numProcesses) as pool:
		converted = pool.map(toCelsius, temperatures)

		#Display our results.
		for i in range(len(temperatures)):
			print(f'{temperatures[i]:.1f} Fahrenheit is the same as {converted[i]:.1f} Celsius.')