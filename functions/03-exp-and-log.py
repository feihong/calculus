# Section 3: Functions: Exp and log

# Imports and helper functions

import numpy as np
import sympy as sym
import matplotlib.pyplot as plt

def printtable(data):
  data_iter = iter(data)
  header = next(data_iter)
  print('<html>')
  print(' | '.join(header))
  print(' | '.join('---' for h in header))
  for row in data_iter:
    if isinstance(row, str):
      print(row)
    else:
      print(' | '.join(str(v) for v in row))
  print('</html>')

"""
We have already established that ◊e = lim_(n->oo) (1+1/n)^n◊
"""

# Exercise 1: estimate e

def gen_data():
  yield 'n', 'ẽ', 'e-ẽ'
  for n in (1,2,5,10):
    estimate = (1.+1./n)**n
    yield f'{n} | {estimate:.5f} | {np.e - estimate:.5f}'

printtable(gen_data())

# Exercise 2:

# Exercise 3:

# Exercise 4:

# Exercise 5:
