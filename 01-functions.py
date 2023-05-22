# Functions Code Challenges

## Imports

import numpy as np
import sympy as sym
import matplotlib.pyplot as plt

## Graph a function

x = np.linspace(-2, 2, 30)
y = 2*x**2 + 3*x**3 - x**4
plt.plot(x, y)
print(plt, format='png')
