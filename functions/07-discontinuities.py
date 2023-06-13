# Section 3: Functions: Discontinuities

# Imports and helper functions

import numpy as np
import sympy as sym
import matplotlib.pyplot as plt
import mdprint

# Exercise 1: Jump discontinuity in numpy

def ex1():
  data = [
    (np.linspace(-1, 0, 11, endpoint=False), '-', lambda x: np.sin(x*np.pi)),
    ([0], 'o', lambda _: 1.5),
    (np.linspace(0, 2, 21)[1:], '-', lambda x: -(x-2)**2)
  ]
  for x, fmt, cb in data:
    plt.plot(x, cb(x), fmt)

  plt.title('A function with a jump discontinuity')
  plt.xlabel('x')
  plt.ylabel('y=f(x)')
  plt.show()

ex1()

# Exercise 1: Jump discontinuity in numpy (using a single domain)

def ex1_single_domain():
  resolution = 0.1
  x = np.arange(-1, 2, resolution)

  data = [
    (x<0, '-', np.sin(x*np.pi)),
    (np.abs(x)<resolution/2, 'o', np.ones(len(x))*1.5),
    (x>0, '-', -(x-2)**2)
  ]
  for cond, fmt, y in data:
    plt.plot(x[cond], y[cond], fmt)

  plt.title('A function with a jump discontinuity')
  plt.xlabel('x')
  plt.ylabel('y=f(x)')
  plt.show()

ex1_single_domain()

# Exercise 2: Jump discontinuity in sympy

def ex2():
  from sympy.abc import x
  e = sym.Piecewise((sym.sin(x*sym.pi), x<0), (1.5, sym.Eq(x, 0)), (-(x-2)**2, x>0))
  mdprint.expr('Piecewise function:', e)
  mdprint.markdown(f'Value at 0: {e.subs(x, 0)}')
  sym.plot(e, (x, -1, 2))

ex2()

# Exercise 3: Removable discontinuity

def ex3():
  x = np.linspace(-1, 2, 31)
  y = np.sin(x*np.pi)+x**2
  closest = np.argmin(x**2)
  y[closest] = np.pi
  plt.plot(x, y, 'o')
  plt.show()

ex3()

# Exercise 4: Infinite discontinuity

def ex4_numpy():
  x = np.linspace(-2, 2, 40)
  plt.plot(x, 3/(1-x**2))
  plt.show()

ex4_numpy()
#

def ex4_sympy():
  from sympy.calculus.util import continuous_domain
  from sympy.calculus.singularities import singularities
  from sympy.abc import x
  e = 3/(1-x**2)
  mdprint.expr('Singularities:', singularities(e, x))
  mdprint.expr('Continuous domain:', continuous_domain(e, x, sym.S.Reals))
  sym.plot(e, (x, -2, 2), ylim=(-20, 20))

ex4_sympy()

# Exercise 5: Oscillating discontinuity

def ex5_numpy():
  x = np.linspace(-1, 2, 41)
  plt.plot(x, np.sin(1/(x-1)), '-o')
  plt.show()

ex5_numpy()
#

def ex5_sympy():
  from sympy.abc import x
  e = sym.sin(1/(x-1))
  sym.plot(e, (x, -1, 2))

ex5_sympy()
