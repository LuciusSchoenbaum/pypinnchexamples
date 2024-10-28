

# Noisy data measuring the solution u to the equation
#     c*u_x - mu*u_xx = 1
# on [0, 1] with BC's u(0) = u(1) = 0
# The value of c is taken as 1 for simplicity.
#
# Baty arXiv:2403.00599v1 1 Mar 2024


import numpy as np
from math import exp
from problem1 import mu_true_value

variance = 0.01

# Warning: this solution assumes c = 1.0
def u_ref(x):
    mu = mu_true_value
    a = np.exp((x-1.0)/mu)
    b = np.full_like(a, exp(-1.0/mu))
    c = np.full_like(a, 1.0)
    subexp = (a - b)/(c - b)
    return x - subexp

# Baty's test: 40 values
data_size = 40
x_values = np.random.uniform(low=0.0, high=1.0, size=(data_size, 1))
# x_values = np.sort(x_values, axis=None).reshape((data_size, 1))
data = u_ref(x_values)
noise = np.random.normal(loc=0.0, scale=variance, size=(data_size,1))
noisydata = np.hstack((x_values, data+noise))
np.savetxt("noisydata.dat", noisydata)

