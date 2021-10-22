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