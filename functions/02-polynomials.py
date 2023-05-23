# Section 3: Functions: Polynomials

# Imports

import random
import numpy as np
import matplotlib.pyplot as plt
import random

# Exercise 1: random polynomials in numpy

xstart, xend = -4, 4
x = np.linspace(xstart, xend, 31)

order = random.randint(3, 7)
# coefficients = [random.randint(-10, 10) for _ in range(order)]
coefficients = np.random.randn(order+1)
print(coefficients)

y = 0
label = []
for i, coefficient in enumerate(coefficients):
  exponent = order-i
  y = y + x**exponent
  sign = "+" if coefficient >= 0 else ""
  label.append(f'{sign}{coefficient:0.2f}x^{exponent}')

plt.plot(x, y)
plt.xlabel('x')
plt.ylabel('y=f(x)')
plt.title(f'$y = {" ".join(label)}$')
plt.show()
