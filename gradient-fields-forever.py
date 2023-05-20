## Gradient fields forever

"""
https://www.udemy.com/course/pycalc1_x/learn/lecture/33947160
"""

import numpy as np
import matplotlib.pyplot as plt

# Get 51 points between -3 and 3, inclusive
xx = np.linspace(-3, 3, 51)
X, Y = np.meshgrid(xx, xx)

f1 = 4
f2 = 0.8
p1 = 0.6
p2 = -0.77

Z = np.sin(f1*X * np.cos(f2*Y + p2) + p1)
gx, gy = np.gradient(Z)

plt.contourf(xx, xx, Z, 40, cmap='coolwarm')
plt.quiver(xx, xx, gx, gy)
plt.show()
