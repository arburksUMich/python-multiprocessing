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