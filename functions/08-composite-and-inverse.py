# Section 3: Functions: Composite and inverse

# Imports and helper functions

import numpy as np
import sympy as sym
import matplotlib.pyplot as plt
import mdprint

# Intermediate value theorem

"""
A function f that is continuous in [a, b] has all the values between f(a) and f(b).
"""

# Exercise 1a: Composite functions in numpy

def ex1a():
  f = lambda x: 2*x**2 - 4
  g = lambda x: 7*np.abs(x) + 3
  x = np.linspace(-5, 5, 101)

  plt.plot(x, f(x), label='f(x)')
  plt.plot(x, g(x), label='g(x)')
  plt.plot(x, f(g(x)), label='f(g(x))')
  plt.plot(x, g(f(x)), '.', label='g(f(x))')
  plt.legend()
  plt.ylim(-10, 50)
  plt.show()

ex1a()

# Exercise 1b: Composite functions in numpy

def ex1b():
  f = lambda x: np.sin(x)
  g = lambda x: np.log(x)
  h = lambda x: 2*x**2 + 5
  x = np.arange(-300, 301)

  plt.plot(x, f(g(h(x))), label='f(g(h(x)))')
  plt.legend()
  plt.show()

ex1b()

# Exercise 2: Inverse function in numpy

def ex2():
  f = lambda x: np.log(2*x)
  g = lambda x: np.exp(x) / 2
  x = np.linspace(0.01, 5, 41)

  plt.plot(x, f(x), label='f(x)')
  plt.plot(x, g(x), label='g(x)')
  plt.plot(x, f(g(x)), label='f(g(x))')
  plt.plot(x, g(f(x)), '.', label='g(f(x))')
  plt.legend()
  plt.ylim(-5, 10)
  plt.show()

ex2()

# Exercise 3: Composite functions in sympy

def ex3():
  from sympy.abc import x
  f = sym.sin(x)
  g = sym.log(x)
  h = 2*x**2 + 5
  composite = f.subs(x, g.subs(x, h))
  sym.plot(composite, (x, -100, 100), title=f'${sym.latex(composite)}$')

ex3()

# Exercise 4: Inverting functions in sympy

def ex4():
  from sympy.abc import x, y

  f = 2*x + 3
  inverse = sym.solve(y - f, x)[0]
  mdprint.expr('Inverse of f(x):', inverse)
  mdprint.markdown(f'{f.subs(x, inverse.subs(y, 4))} = {inverse.subs(y, f.subs(x, 4))}')

  try:
    g = 2*x + sym.sin(x)
    ans = sym.solve(y - g, x)
  except NotImplementedError as e:
    print(e)

ex4()
