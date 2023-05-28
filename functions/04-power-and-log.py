# Section 3: Functions: Power and log

# Imports and helper functions

import random
import itertools
import numpy as np
import sympy as sym
import matplotlib.pyplot as plt
from sympy.abc import x, a, b
import htmlprint

def compare_with_simplified(e, data, use_ints=False, equivalent=None):
  def rand():
    if use_ints:
      return random.randint(0, 100)
    else:
      return random.randint(0, 100) / 10.

  equivalent = sym.simplify(e) if equivalent is None else equivalent
  htmlprint.expr(e, 'is equivalent to', equivalent)

  def generate_data():
    yield 'a', 'b', f'${sym.latex(e)}$', f'${sym.latex(equivalent)}$'

    rows = itertools.chain([data], ((rand(), rand()) for _ in range(4)))

    for a_val, b_val in rows:
      sub1 = e.subs({a: a_val, b: b_val})
      sub2 = equivalent.subs({a: a_val, b: b_val})
      yield f'{a_val} | {b_val} | ${sym.latex(sub1)}$ | ${sym.latex(sub2)}$'

  htmlprint.table(generate_data())

# What is ◊0^0◊?

f"""
It has been a point of contention, but mathematicians hashed it out and decided that ◊0^0 = {0**0}◊.
"""

# Exercise 1: Adding powers

compare_with_simplified(x**a * x**b, (3.4, 7.3))

# Exercise 2: Subtracting powers

compare_with_simplified(x**a / x**b, (4, 4))

# Exercise 3:

compare_with_simplified((x**a)**b, (3, 7), use_ints=True, equivalent=(x**(a*b)))

# Exercise 4:
