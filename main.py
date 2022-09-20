from numba import njit
import time

import numpy as np

def func(arr):
    v = 0
    for i in arr:
        v += i*i
    
    return v

numbers = np.array(range(10000000))

t = time.time()
func(numbers)
print(time.time() -t)

jitfunc = njit()(func)

t = time.time()
jitfunc(numbers)
print(time.time() -t)

t = time.time()
jitfunc(numbers)
print(time.time() -t)