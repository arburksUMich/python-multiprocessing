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



"""
This example function simulates a task that performs some I/O operation such as making a web request, connecting to a database, etc.
We pretend that this operation takes a total of two seconds by using the sleep() function.
"""
def doWork(taskNumber):
	sleep(2)
	print(f'Task {taskNumber} done.')



"""
Simple main function that creates an array of threads and runs our fancy doWork() function separately in each thread.
This shows one good use case of threads: threads are useful for speeding up code that is I/O-bound rather than CPU-bound.
"""
if __name__ == "__main__":
	threads = []

  #Create 8 threads and call the doWork() function in each thread
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

print(f"I have {multiprocessing.cpu_count()} CPU cores available!")

```

## Using the multiprocessing.Process class
```python
import multiprocessing
from random import choice
from multiprocessing import Process

def _mean(x):
    total = sum(x)
    mean = total / len(x)

    print(f'The mean of x is {mean}')


def product(x):
    result = 1

    for value in x:
        result = result * value

    print(f'The product of x is {result}')


def randomNumber(x):
    print(f'We selected {choice(x)} from x.')

if __name__=="__main__":
    x = [1, 3, 5, 7, 9]

    p1=Process(target=_mean, args=(x,))
    p2=Process(target=product, args=(x,))
    p3=Process(target=randomNumber, args=(x,))

    p1.start()
    p2.start()
    p3.start()

    p1.join()
    p2.join()
    p3.join()

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
	return (degrees - 32) * (5.0/9.0)



if __name__ == "__main__":
	numProcesses = 4

	#Generate some random temperatures in Fahrenheit
	temperatures = [random.uniform(32.0, 100.0) for i in range(50)]

	#Convert them using pool.map()
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
	return a * b



if __name__ == "__main__":
	numProcesses = 4
	
	#Create some random pairs.
	pairs = [(1, 3), (5, 9), (2, 3), (4, 5), (10, 30), (5, 7)]

	#Calculate the product of each pair using pool.starmap()
	with multiprocessing.Pool(numProcesses) as pool:
		products = pool.starmap(product, pairs)


		#Display our results.
		for i in range(len(pairs)):
			pair = pairs[i]

			print(f'{pair[0]} * {pair[1]} = {products[i]}.')

```


## Estimating the value of pi - Serial
```python
nsteps = 100000000
dx = 1.0 / nsteps
pi = 0.0
for i in range(nsteps):
    x = (i + 0.5) * dx
    pi += 4.0 / (1.0 + x * x)
pi *= dx

print(pi)

```


## Estimating the value of pi - Parallel
```python
import multiprocessing as mp

nsteps = 100000000
dx = 1.0 / nsteps
pi = 0.0

def calc_partial_pi(rank, nprocs, nsteps, dx):
    partial_pi = 0.0

    for i in range(rank, nsteps, nprocs):
        x = (i + 0.5) * dx
        partial_pi += 4.0 / (1.0 + x**2)
    partial_pi *= dx

    return partial_pi


nprocs = 4
inputs = [(rank, nprocs, nsteps, dx) for rank in range(nprocs)]

pool = mp.Pool(processes=nprocs)

result = pool.starmap(calc_partial_pi, inputs)
pi = sum(result)

print(pi)

```
