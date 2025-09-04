
# import random
# import string
import time
import random

from multiprocessing import Process, Queue, current_process, freeze_support

def worker(input_, output):
    for func, args in iter(input_.get, 'STOP'):
        result = calculate(func, args)
        output.put(result)
        
#
# Function used to calculate result
#

def calculate(func, args):
    result = func(*args)
    return '%s says that %s%s = %s' % \
        (current_process().name, func.__name__, args, result)        
        
#
# Functions referenced by tasks
#

def mul(a, b):
    time.sleep(0.5*random.random())
    return a * b

def plus(a, b):
    time.sleep(0.5*random.random())
    return a + b        
