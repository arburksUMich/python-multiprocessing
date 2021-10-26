from multiprocessing import Process
from random import choice


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
    print('Done.')