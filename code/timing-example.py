import requests

from threading import Thread



def doWork(taskNumber):
	"""This example function simulates a task that makes a web request, which takes
           a little bit of time to return.


	Keyword arguments:
	taskNumber -- represents the thread in which this function is executing
	"""
	response = requests.get('https://en.wikipedia.org/wiki/Special:Random')
	print(f'URL {taskNumber}: {response.url}')



"""
Simple main function that creates an array of threads and runs our fancy doWork() function separately in each thread.
This shows one good use case of threads: threads are useful for speeding up code that is I/O-bound rather than CPU-bound.
"""
if __name__ == "__main__":
	#First, let's call doWork() 8 times in a loop for comparison.
	print('Using a loop ...')

	for i in range(8):
		doWork(i)


	#Create 8 threads and call the doWork() function in each thread
	threads = []

	print('\nUsing threading ...')
	for i in range(8):	
		thread = Thread(target=doWork, args=(i,))
		threads.append(thread)
		thread.start()
	
	#Wait for all the threads to finish.
	for thread in threads:
		thread.join()
	

