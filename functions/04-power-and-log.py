# Section 3: Functions: Power and log

# Imports and helper functions

import random
import itertools
import numpy as np
import sympy as sym
import matplotlib.pyplot as plt
from sympy.abc import x, a, b
import htmlprint

def randint():
  return random.randint(0, 100) / 10.

# Exercise 1: Adding powers

e = x**a * x**b
e_simp = sym.simplify(e)
htmlprint.expr('Simplified:', e_simp)

def generate_data():
  yield 'a', 'b', f'${sym.latex(e)}$', f'${sym.latex(e_simp)}$'
  rows = itertools.chain([(3.4, 7.3)], ((randint(), randint()) for _ in range(5)))
  for a_val, b_val in rows:
    sub1 = e.subs({a: a_val, b: b_val})
    sub2 = e_simp.subs({a: a_val, b: b_val})
    yield f'{a_val} | {b_val} | ${sym.latex(sub1)}$ | ${sym.latex(sub2)}$'

htmlprint.table(generate_data())

# Exercise 3:

# Exercise 3:

# Exercise 4:
