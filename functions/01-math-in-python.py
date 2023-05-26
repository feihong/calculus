# Section 3: Functions: Math in python

# Imports

import numpy as np
import matplotlib.pyplot as plt
import sympy as sym

# Exercise 1: Implement the function in numpy

start = -2
end = 2
x = np.linspace(start, end, 31)
print(x)
y = x**2 + 3*x**3 - x**4

plt.plot(x, y, label='$y = x^2 + 3x^3 - x^4$')
plt.legend()
plt.grid()
plt.xlabel('x')
plt.ylabel('y=f(x)')
plt.xlim(start, end)
plt.show()

# Exercise 2: Implement the function in sympy

s_beta = sym.symbols('beta')
s_y = s_beta**2 + 3*s_beta**3 - s_beta**4

sym.plot(s_y, (s_beta, start, end),
                  xlabel='x', ylabel=None, title=f'$f(\\beta) = {sym.printing.latex(s_y)}$')


# Exercise 3: Convert from sympy to numpy

fx = sym.lambdify(s_beta, s_y)
y_2 = fx(x)

plt.plot(x, y_2, label=f'${sym.printing.latex(s_y)}$')
plt.legend()
plt.grid()
plt.xlabel('$\\beta$')
plt.ylabel('$y=f(\\beta)$')
plt.xlim(start, end)
plt.show()
