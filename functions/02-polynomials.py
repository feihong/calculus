# Section 3: Functions: Polynomials

# Imports

import random
import math
import numpy as np
import matplotlib.pyplot as plt
import sympy as sym

printexpr = lambda expr: print(f'<html>\n${sym.latex(expr)}$\n</html>')

# Exercise 1: random polynomials in numpy

x = np.linspace(-5, 5, 31)

degree = random.randint(3, 7)
# coefficients = [random.randint(-10, 10) for _ in range(order)]
coefficients = np.random.randn(degree + 1)
print(coefficients)

y = 0
terms = []
for i, coefficient in enumerate(coefficients):
  exponent = degree - i
  y = y + x**exponent
  sign = "+ "[coefficient < 0]
  terms.append(f'{sign}{coefficient:0.2f}x^{exponent}')

title = 'y = ' + ''.join(terms).lstrip('+')
print(title)

plt.plot(x, y)
plt.xlabel('x')
plt.ylabel('y=f(x)')
plt.title(f'${title}$')
plt.show()

# Exercise 2: polynomials in sympy

from sympy.abc import x as sx
sy = (sx**2 - 2*sx) / (sx**2 - 4)

sym.plot(sy, (sx, -3, 3), ylim=(-10,10), title=f'$y={sym.printing.latex(sy)}$')

# Exercise 3: estimate a sine wave with polynomials

"""
We'll use the Maclaurin series

◊sum_(n=1)^oo (-1)^(n+1) (x^(2n-1))/((2n-1)!)◊

to generate a polynomial to estimate sine
"""

x2 = np.linspace(-2*np.pi, 2*np.pi, 31)
plt.plot(x2[::2], np.sin(x2[::2]), 'ok', label='sin(x)', markerfacecolor='w', linestyle='')

steps = 10
sine_estimate = np.zeros(len(x2))

for n in range(1, steps + 1):
  temp_y = ((-1)**(n+1)) * ((x2**(2*n - 1)) / math.factorial(2*n - 1))
  sine_estimate += temp_y
  plt.plot(x2, temp_y, linestyle='--')

plt.plot(x2, sine_estimate, 'k', label=f'sum over {steps} terms', linewidth=2)

plt.legend()
plt.xlim(x2[[0, -1]])
plt.ylim(-5, 5)
plt.show()

# Exercise 3: estimate a sine wave with polynomials using sympy

# Zoom out a little to see how the estimate degrades the further you get from origin
x3 = np.linspace(-10, 10, 41)
plt.plot(x3[::2], np.sin(x3[::2]), 'ok', label='sin(x)', markerfacecolor='w', linestyle='')

sn = sym.symbols('n')
maclaurin_series = sym.summation(((-1)**(sn+1)) * (sx**(2*sn - 1)) / sym.factorial(2*sn - 1), (sn, 1, 10))
printexpr(maclaurin_series)

fx = sym.lambdify(sx, maclaurin_series)
plt.plot(x3, fx(x3), 'k', label='sum over 10 terms', linewidth=2)

for ((exponent,), coeff) in sym.poly(maclaurin_series).all_terms():
  if coeff != 0:
    term = coeff*sx**exponent
    gx = sym.lambdify(sx, term)
    plt.plot(x3, gx(x3), linestyle='--')

plt.legend()
plt.xlim(x3[[0, -1]])
plt.ylim(-5, 5)
plt.show()

# Is Maclaurin series really equivalent to sine?

maclaurin_series2 = sym.summation(((-1)**(sn+1)) * (sx**(2*sn - 1)) / sym.factorial(2*sn - 1), (sn, 1, sym.oo))
printexpr(maclaurin_series2)

"""
Sympy says yes
"""
