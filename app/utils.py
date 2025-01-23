from time import time
from termcolor import colored

def benchmark(func):
    def wrapper(*args, **kwargs):
        start = time()
        res = func(*args, **kwargs)
        end = time() - start

        color = 'yellow'
        if end > 1:
            color = 'red'
        elif end < 0.2:
            color = 'green'

        print(colored(f"[{func.__name__}()]: {end:.6f} sec", color))
        return res
    return wrapper
