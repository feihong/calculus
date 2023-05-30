# Section 3: Functions: Trigonometry

# Imports and helper functions

import numpy as np
import matplotlib.pyplot as plt

# Exercise 1: Fun with trig :)

def ex1():
  x = np.linspace(-np.pi, 2*np.pi, 61)
  plt.plot(x, np.sin(x), label='$sin(x)$')
  plt.plot(x, np.sin(x)**2, label='$sin^2(x)$')
  plt.plot(x, np.sin(x**2), label='$sin(x^2)$')

  plt.legend()
  plt.xlabel('Angle (radians)')
  plt.ylabel('y=f(x)')
  plt.xlim(x[[0, -1]])
  plt.show()

ex1()

# Exercise 2: More fun with trig :)

def ex2():
  x = np.linspace(-np.pi, 2*np.pi, 61)
  plt.plot(x, np.sin(np.cos(x)), label='$sin(cos(x))$')
  plt.plot(x, np.cos(np.sin(x)), label='$cos(sin(x))$')
  plt.plot(x, np.cos(x), label='$cos(x)$')

  plt.legend()
  plt.xlabel('Angle (radians)')
  plt.ylabel('y=f(x)')
  plt.xlim(x[[0, -1]])
  plt.show()

ex2()

# Exercise 3: Resolution and tan

def ex3(zoom=False):
  for i in range(2, 5):
    points = 10**i
    x = np.linspace(0, 2*np.pi, points)
    plt.plot(x, np.tan(x), 'o-', label=f'{points} pnts')

  plt.legend()
  plt.xlabel('Angle (radians)')
  plt.ylabel('y=f(x)')
  if zoom:
    plt.xlim(1.55, 1.60)
    plt.ylim(-400, 400)
  plt.show()

ex3()

ex3(zoom=True)
