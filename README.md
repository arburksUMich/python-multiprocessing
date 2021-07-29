# Getting Started with the Python Multiprocessing Package

This repository contains workshop materials for the workshop, "Getting Started with the Python Multiprocessing Package" at the University of Michigan.


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




## Determining the number of CPU cores available
```python
import multiprocessing

print(f"I have {multiprocessing.cpu_count()} CPU cores available!")

```

## Using the multiprocessing.Process class
```python
import multiprocessing
from multiprocessing import Process

def testing():
       print("Works")
def square(n):
       print("The number squares to ",n**2)

def cube(n):
       print("The number cubes to ",n**3)

if __name__=="__main__":
       p1=Process(target=square,args=(7,))
       p2=Process(target=cube,args=(7,))
       p3=Process(target=testing)
       p1.start()
       p2.start()
       p3.start()
       p1.join()
       p2.join()
       p3.join()
       print("We're done")

```



## Using the Pool.map() function
```python


```

## Using the Pool.starmap() function
```python


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
