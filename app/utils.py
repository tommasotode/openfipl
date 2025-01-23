from time import time
from termcolor import colored

def benchmark(func):
    def wrapper(*args, **kwargs):
        start = time()
        res = func(*args, **kwargs)
        print(colored(f"[{func.__name__}()]: {time() - start:.6f} sec", 'yellow'))
        return res
    return wrapper
