# Section 3: Functions: Polynomials

# Imports

import random
import math
from collections import namedtuple
import numpy as np
import matplotlib.pyplot as plt
import sympy as sym

Domain = namedtuple('Domain', ['start', 'end'])

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

domain = Domain(-6, 6)

x2 = np.linspace(domain.start, domain.end, 31)
steps = 10
compute_term = lambda x, n: ((-1)**(n+1)) * ((x**(2*n - 1)) / math.factorial(2*n - 1))
compute_sum = lambda x: sum(compute_term(x, n) for n in range(1, steps+1))
sine_est = [compute_sum(x) for x in x2]
plt.plot(x2, sine_est, label='sum over 10 terms')

sine_x = np.linspace(domain.start, domain.end, 11)
sine = np.sin(sine_x)
plt.plot(sine_x, sine, label='sin(x)', marker='o', markerfacecolor='white', markeredgecolor='black', linestyle='')

plt.legend()
plt.xlim(domain.start, domain.end)
plt.ylim(-5, 5)
plt.show()
