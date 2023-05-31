# Section 3: Functions: Piecewise functions

# Imports and helper functions

import numpy as np
import sympy as sym
import matplotlib.pyplot as plt
import mdprint

# Exercise 1: piecewise function in numpy

def ex1():
  x = np.linspace(-3, 5, 31)
  # y = np.select([x<0, (x>=0) & (x<3), x>=3], [np.zeros(len(x)), -2*x, .1*x**3], 0)
  y = np.select([(x>=0) & (x<3), x>=3], [-2*x, .1*x**3], 0)
  plt.plot(x, y, '-o')
  plt.xlabel('x')
  plt.ylabel('y=f(x)')
  plt.title('A piecewise function')
  plt.show()

ex1()

# Exercise 1: piecewise function in numpy without using numpy.select

def ex1_no_select():
  x = np.linspace(-3, 5, 31)
  # y = 0*(x<0) + (-2*x)*((x>=0) & (x<3)) + (.1*x**3)*(x>=3)
  y = (-2*x)*((x>=0) & (x<3)) + (.1*x**3)*(x>=3)
  plt.plot(x, y, '-o')
  plt.xlabel('x')
  plt.ylabel('y=f(x)')
  plt.title('A piecewise function')
  plt.show()

ex1_no_select()

# Exercise 2: draw separate lines

def ex2():
  x = np.linspace(-3, 5, 41)
  pairs = [
    (x[x<0], lambda x: np.zeros(len(x))),
    (x[(x>=0) & (x<3)], lambda x: -2*x),
    (x[x>=3], lambda x: x**3/10),
  ]
  for i, (x, cb) in enumerate(pairs, 1):
    plt.plot(x, cb(x), '-o', label=f'Piece {i}')
  plt.xlabel('x')
  plt.ylabel('y=f(x)')
  plt.title('A piecewise function')
  plt.show()

ex2()

# Exercise 3: piecewise function in sympy

def ex3():
  from sympy.abc import x
  y = sym.Piecewise((0, x<0), (-2*x, (x>=0) & (x<3)), (x**3/10, x>=3))
  mdprint.expr('Piecewise function:', y)
  sym.plot(y, (x, -3, 5), xlabel='x', ylabel='y', title=f'Piecewise function')

ex3()

# Exercise 4: evaluate the function at or near a point

def ex4():
  x = sym.symbols('x')
  y = sym.Piecewise((0, x<0), (-2*x, (x>=0) & (x<3)), (x**3/10, x>=3))
  print('Compute f(0.5) using sympy:', y.subs(x, 0.5))

  # This isn't always practical because we might have to rely on whatever data we happen to have
  # x = np.array([0.5])
  # y = np.select([(x>=0)&(x<3), x>=3], [-2*x, .1*x**3], 0)
  # print('Compute f(0.5) using numpy:', y[0])

  x = np.linspace(-3, 5, 42)
  y = np.select([(x>=0)&(x<3), x>=3], [-2*x, .1*x**3], 0)
  x_closest = np.argmin(np.abs(0.5 - x)) # number in x closest to 0.5
  print(f'Estimate f(0.5) using f({x[x_closest]}) from numpy array:', y[x_closest])

ex4()
