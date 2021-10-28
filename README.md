# Getting Started with the Python Multiprocessing Package

This repository contains workshop materials for the workshop, "Getting Started with the Python Multiprocessing Package" at the University of Michigan. See the slides directory for a PDF version of the slides. The code directory contains all the source code we will use for the exercises. The video recording from the workshop can be found at https://www.mivideo.it.umich.edu/media/t/1_i60d4nfu/181860561 (requires U-M authentication).

## Python Memory Management
We begin with a brief discussion on memory management in Python. Soon, we will see why this matters in the context of multitasking and multiprocessing.

Creating variables and objects in your code takes up space in memory (RAM). The bigger those variables/objects, and the longer your code is using them, the fuller the RAM can get. Modern programming languages such as Python and others, attempt to manage memory for you by releasing objects from memory when they are no longer used. Python uses *reference counting* to do this.

Reference counting works by keeping a count the number of times an object has been referenced in your code. Whenever this count reaches 0, then it is safe to release that object from memory.

### Reference Counting and Multithreading
Reference counting was a solution to memory management in Python, but it was problematic for multithreaded programs. When writing multithreaded programs, we must ensure that if two or more threads access the same variable, they do so safely. Otherwise, we end up with what's known as a *race condition*, in which multiple threads read and write the same variable at the same time. When this occurs, we cannot be sure of the integrity of the variable's value.

Since Python uses the reference count variable for managing memory, race conditions would be quite drastic. Therefore, Python needed some way of protecting the reference count variable whenever multiple threads are in use.



## Mutual Exclusion (Lock)
A mutual exclusion (MUTEX or lock for short) is a software mechanism that is used to protect against race conditions and other issues that arise with multithreaded programs. A MUTEX prevents multiple threads from executing what's called *critical code*. Critical code is any code that accesses a resource, such as the reference count variable, that is shared between multiple threads. Python uses a special type of MUTEX called the *global interpreter lock* to protect the reference count, allowing the memory management to actually work correctly.


### The Global Interpreter Lock (GIL)
The GIL is essentially a MUTEX that prevents multiple threads from changing the reference count at the same time. This is done by locking the Python interpreter so that only one thread at a time can execute instuctions.

This seemingly simple solution solved the memory management issue but it also created another one, which is the reason that the GIL gets a bad reputation. Because of the GIL, Python multithreaded code cannot be truly parallel since only exactly one thread can execute at a time.

This causes a big bottleneck with intensive CPU-bound code.


## Why Use Threads in Python?
Now that we have learned about the huge limitation imposed by the GIL, you may be wondering, "Why even use threads in Python?" We just stated that threads cause a huge bottleneck for CPU-bound code due to the GIL. However, threads actually can be quite useful in Python for I/O bound code. Multithreading in Python allows work to be done in one thread while the program is waiting in another thread such as in the below examples.

* **Disk I/O**: Consider the case in which we are doing a lot of I/O and we might have to wait for the disk. We can perform the I/O in one thread while we do other processing in another thread.

* **Web requests**: Imagine having a list of URLs, and for each URL we need to make a web request and wait for a response from a server. We can also use multithreading here to do other work while waiting for a response.

Before we move into our discussion on multiprocessing, let's look at a quick example of using threads for speeding up I/O-bound code.


## Using Threads to Speed up I/O-Bound Code.
Our first coding exercise shows how threading can be used in Python to speed up I/O bound code.
```Python
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
In the above example, we see that the multithreaded code runs significantly faster than the single-threaded version. Altough the threads appear to run at the same time, what we really are seeing is an example of *concurrency* rather than parallelism.

With concurrency, multiple threads execute in an interleaved fashion, rather than actually running at the same time. The CPU executes each task for a certain number of steps before switching to the next task, and so on, until all the tasks are completed.

In contrast to concurrency, parallelism actually allows us to run multiple tasks at the same point in time. This is where multi-core machines really shine.


## How Can We Achieve True Parallelism in Python?
The multiprocessing package is a very handy tool that allows us to very easily write parallel code in Python. The multiprocessing package is able to achieve true parallelism in Python since the parallel code is executed via multiple processes instead of threads. By relying on processes instead of threads, we completely avoid the issue of the GIL because each process has its own interpreter instance. Multiple processes can actually run at the same time on different cores since they are not restricted by the GIL.


### The multiprocessing Package

We will cover some of the basic functionality of the multiprocessing package in the rest of our coding exercises. There are MANY more features to learn about outside of this workshop.




## Determining the Number of CPU cores Available
```Python
import multiprocessing

#Short example demonstrating how to determine the number of cores available.
numCores = multiprocessing.cpu_count()

print(f"I have {numCores} CPU cores available!")

```

## Using the multiprocessing.Process Class
Next up is the Process class. This is the basic way of performing some work in a separate process, and one way of running multiple tasks in parallel. The following example shows how we can run three processes in parallel, although the later examples show more common ways of using multiprocessing.

```Python
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

## The multiprocessing.Pool Class
Next is the Pool class. This is a very useful class for a lot of parallel processing that one might do in Python. A pool represents a collection of worker processes that can be used to divide work in parallel.

We typically will have a large number of tasks that need to be run, and we can use the pool to automatically assign tasks to the workers until all the work is finished.

This is a very easy way of parallelizing code that involves a loop or some data that can be processed in chunks. The following code examples all use the Pool class in some way.



## Using the Pool.map() Function
The map() function allows us to execute a function in parallel, where the function requires just a single argument.
```Python
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

## Using the Pool.starmap() Function
The starmap() function is very similar to the map() function. However, it can be used to parallelly execute a function that requrires multiple arguments.
```Python
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
```Python
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
```Python
#Adapted from https://www.kth.se/blogs/pdc/2019/02/parallel-programming-in-Python-multiprocessing-part-1/
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

## Some Rules of Thumb
* Loops can often be easily parallelized
	* Use Pool for parallelizing loops
* Data can often be processed in chunks
	* Pool often is the way to go for this too
* Always use join() after using Process.start()
* Avoid sharing data between processes
