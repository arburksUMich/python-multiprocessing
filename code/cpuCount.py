import multiprocessing

#Short example demonstrating how to determine the number of cores available.
numCores = multiprocessing.cpu_count()

print(f"I have {numCores} CPU cores available!")