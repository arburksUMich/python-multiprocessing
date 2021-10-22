# Getting Started with the Python Multiprocessing Package

This repository contains workshop materials for the workshop, "Getting Started with the Python Multiprocessing Package" at the University of Michigan.

## Python Memory Management
Reference counting

Tracks the number of references to every created object

When reference count is zero, the object can be released from memory

### Reference Counting and Multithreading
Multiple threads running simultaneously can cause problems

Race condition

Multiple threads change an object’s reference count simultaneously


## Mutual Exclusion (Lock)
Software mechanism that prevents multiple threads from executing critical code simultaneously

Critical code

Code that accesses a shared/critical resource (such as an object’s reference count)


## The Global Interpreter Lock (GIL)
A mutual exclusion/lock on the Python interpreter

Solution to protecting reference count

Allows only one thread to execute at any point in time

Causes bottleneck for CPU-bound code


## Why Use Threads in Python?
Allows work to be done in one thread while another thread is waiting

Examples:

I/O heavy process.

Can do other processing while waiting for disk

Web requests or database connection

Can do other processing while waiting for response from server

## Using threads to speed up I/O bound code.
```python
import random

from time import sleep
from threading import Thread
from multiprocessing import Pool



def doWork(taskNumber):
	"""This example function simulates a task that performs some
	I/O operation such as making a web request, connecting to a
	database, etc.

	We pretend that this operation takes a total of two seconds
	by using the sleep() function.

	Keyword arguments:
	taskNumber -- represents the thread in which this function is executing
	"""

	sleep(2)
	print(f'Task {taskNumber} done.')



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
```

## Concurrency vs Parallelism
Concurrency is when two or more tasks can start, run, and complete in overlapping time periods.
Example: multitasking on a single-core machine.

Parallelism is when tasks literally run at the same time, e.g., on a multicore processor.


## How Can We Achieve True Parallelism in Python?
The multiprocessing package​

Parallelizes code by using multiple processes instead of multiple threads​

Completely avoids the issue  of the GIL​

Each process has its own interpreter instance​

Multiple processes can take advantage of multicore CPU

## The multiprocessing package

We will cover some of the basic functionality of the multiprocessing package

There are MANY more features




## Determining the number of CPU cores available
```python
import multiprocessing

#Short example demonstrating how to determine the number of cores available.
numCores = multiprocessing.cpu_count()

print(f"I have {numCores} CPU cores available!")

```

## Using the multiprocessing.Process class
```python
import multiprocessing
from random import choice
from multiprocessing import Process


def _mean(x):
    """Simple function to calculate the mean of an input list, x."""

    total = sum(x)
    mean = total / len(x)

    print(f'The mean of x is {mean}')



def product(x):
    """Simple function to calculate the product of an input list, x."""

    result = 1

    for value in x:
        result = result * value

    print(f'The product of x is {result}')



def randomNumber(x):
    """Simple function to select a random item from the input list, x."""

    print(f'We selected {choice(x)} from x.')



"""Simple main function that creates 3 processes to run 3 separate
functions in parallel."""
if __name__=="__main__":
    x = [1, 3, 5, 7, 9]

    #Create 3 processes to run each of our functions on x, asynchronously.
    p1=Process(target=_mean, args=(x,))
    p2=Process(target=product, args=(x,))
    p3=Process(target=randomNumber, args=(x,))

    #Call start() on each of the processes to begin execution.
    p1.start()
    p2.start()
    p3.start()

    #Wait for each of the processes to return.
    p1.join()
    p2.join()
    p3.join()


    #This will print only after all 3 processes have returned.
    print('Done')
```

## multiprocessing.Pool class
Represents a pool of worker proceses

Run tasks in worker processes

Very easy way to parallelize code



## Using the Pool.map() function
```python
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

```

## Using the Pool.starmap() function
```python
import multiprocessing
import random


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

```


## Estimating the value of pi - Serial Version
```python
import sys

"""Get the number of steps to use from the command line.
As the number of steps increase, the estimate gets more
accurate. However, it also takes more time to process.
Let's try different nSteps, up to 100,000,000."""
nSteps = int(sys.argv[1])

#Estimate pi by summing our formula over nSteps
pi = 0.0

for i in range(nSteps):
    x = (i + 0.5) / nSteps
    pi += 4.0 / (1.0 + x * x)

pi /= nSteps

print(pi)

```


## Estimating the value of pi - Parallel Version
```python
#Adapted from https://www.kth.se/blogs/pdc/2019/02/parallel-programming-in-python-multiprocessing-part-1/
import multiprocessing
import sys



def partialPi(rank, numProcesses, nSteps):
    """This function uses our formula to calculate the partial result.

    Keyword arguments:    
    rank   -- determines where from 1 to numProcesses our loop should start
    nSteps -- the total number of iterations we will use to estimate Pi
    numProcesses -- how many processes we are using for parallelism."""

    partial = 0.0

    #The loop is setup so that each process will only sum it's own chunk
    #of numbers as we calculate the partial answer.
    for i in range(rank, nSteps, numProcesses):
        x = (i + 0.5) /nSteps
        partial += 4.0 / (1.0 + x**2)

    partial /= nSteps

    return partial



"""Remember to wrap your multiprocessing functionality in the main function."""
if __name__ == "__main__":
    nSteps = int(sys.argv[1]) #go up to 100,000,000
    numProcesses = 4


    #This is a way of splitting our problem (the range of iterations) into chunks
    inputs = [(rank, numProcesses, nSteps) for rank in range(numProcesses)]

    with multiprocessing.Pool(numProcesses) as pool:
        #Use pool.starmap() to run our partialPi() function, which requires multiple inputs
        result = pool.starmap(partialPi, inputs)

        #result is a list of the partial answers, we can sum them to estimate Pi.
        pi = sum(result)

        print(pi)
```
