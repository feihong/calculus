# Section 3: Functions: Exp and log

# Imports and helper functions

import numpy as np
import sympy as sym
import matplotlib.pyplot as plt
import htmlprint

# Is ◊e = lim_(n->oo) (1+1/n)^n◊ really equivalent to ◊e◊?

n = sym.symbols('n')
print(sym.limit((1+1/n)**n, n, sym.oo) == sym.E)

print(sym.N(sym.E))

# Exercise 1: estimate e

def gen_data():
  yield 'n', 'ẽ', 'e-ẽ'
  ns = np.array([1,2,5,10,20])
  estimates = (1 + 1/ns)**ns
  diffs = np.e - estimates
  for n, estimate, diff in zip(ns, estimates, diffs):
    yield f'{n} | {estimate:.5f} | {diff:.5f}'

htmlprint.table(gen_data())

# Exercise 2: visualize e's approach

def ex2():
  n = np.arange(1, 1001)
  diffs = np.e - (1 + 1/n)**n
  plt.plot(n, diffs)
  plt.xlabel('n')
  plt.ylabel('Difference to np.e')
  plt.show()

ex2()

# Exercise 3: exploring e in numpy

def ex3():
  x = np.linspace(-2, 2, 21)
  plt.plot(x, np.exp(x), label='$y=e^x$')
  plt.plot(x, np.exp(x**2), label='$y=e^{x^2}$')
  plt.plot(x, np.exp((-x)**2), 'g--', label='$y=e^{(-x)^2}$')
  plt.plot(x, np.exp(-(x**2)), label='$y=e^{-(x^2)}$')
  plt.plot(x, np.exp(x)**2, label='$y=(e^x)^2$')
  plt.ylim(-1, 10)
  plt.grid()
  plt.legend()
  plt.show()

ex3()

# Exercise 4: exploring e in sympy

def ex4():
  beta = sym.symbols('beta')
  y = sym.exp(beta) - sym.log(beta) - sym.E
  # Using (beta, 0, 2) will actually result in a math domain error. But starting at -2 is OK.
  sym.plot(y, (beta, -2, 2), xlabel=r'$\beta$', ylabel=r'$y=f(\beta)$',
           title=f'$f(\\beta) = {sym.printing.latex(y)}$')

ex4()

# Exercise 5: exp and log

def ex5():
  x = np.linspace(-4, 4, 21)
  x_more = np.linspace(x[0], x[-1], 301)
  # this one will get cut off around 0.3 or so
  plt.plot(x, np.log(x), '+', label='log(x)')
  # you need way more points to plot log when it gets close to 0
  plt.plot(x_more, np.log(x_more), label='log(x) with more points')
  plt.plot(x, np.exp(x), label='exp(x)')
  plt.plot(x, np.log(np.exp(x)), label='log(exp(x))')
  plt.plot(x, np.exp(np.log(x)), '.', label='exp(log(x))', markeredgewidth=3)
  plt.ylim(-4, 4)
  plt.legend()
  plt.show()

ex5()
