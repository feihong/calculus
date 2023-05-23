# Section 3: Functions: Polynomials

# Imports

import random
import numpy as np
import sympy as sym
import matplotlib.pyplot as plt
import random

# Exercise 1: random polynomials in numpy

xstart, xend = -4, 4
x = np.linspace(xstart, xend, 31)

a, b, c, d = [random.randint(-10, 10) for i in range(4)]
y = a*x**3 + b*x**2 + c*x + d
s_x = sym.symbols('x')
s_y = a*s_x**3 + b*s_x**2 + c*s_x + d
plt.plot(x, y)
plt.xlabel('x')
plt.ylabel('y=f(x)')
plt.title(f'$y = {sym.printing.latex(s_y)}$')
plt.show()
