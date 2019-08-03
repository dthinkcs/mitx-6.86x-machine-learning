#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 22:18:22 2019

@author: dileepn

Kernel Perceptron Algorithm: Toy Example
"""
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Data points
x = np.array([[5,2], [1,4], [2,0], [4,1], [3,3], [4,4], [1,1], [0,2], [5,5], [0,0]])
#x = np.array([[0,0], [0,2], [1,1], [2,0], [3,3], [1,4], [4,1], [4,4], [5,2], [5,5]])

# Labels
y = np.array([[1],[1],[-1],[1],[-1],[1],[-1],[-1],[1],[-1]])
#y = np.array([[-1],[-1],[-1],[-1],[-1],[1],[1],[1],[1],[1]])

# Plot data
colors = ['r' if y == 1 else 'b' for y in y]
#f, ax = plt.subplots(figsize=(7, 7))
#ax.scatter(x[:,0], x[:,1], s=40, c=colors)

# Number of examples
n = x.shape[0]

# Number of features
m = x.shape[1]

# No. of iterations
T = 100

# Initialize alphas to zero
alphas = np.zeros((n,1))
#alphas = np.array([[1],[31],[11],[65],[72],[21],[30],[4],[0],[15]])
theta0 = 0.0

# Tolerance for floating point errors
eps = 1e-8

# Kernel matrix: quadratic kernel, phi(x) = [x1^2, sqrt(2)*x1*x2, x2^2]
def kernel_matrix(x, y):
    """ 
    Returns kernel matrix (quadratic kernel, in this case) for input arrays, x 
    and y: K(x,y) = phi(x).phi(y), which for a quadratic kernel is (x.y)^2 
    """
    K = (x.dot(y.T))**2
    
    return K

def quad_kernel(x):
    """
    Returns the kernel representation (quadratic, in this case) of input array, x
    """
    try:
        k1 = x[:,0]**2
        k2 = x[:,1]**2
        k12 = np.sqrt(2)*x[:,0]*x[:,1]
        return np.vstack((k1,k12,k2))
    except IndexError:
        k1 = x[0]**2
        k2 = x[1]**2
        k12 = np.sqrt(2)*x[0]*x[1]
        return np.array([[k1],[k12],[k2]])

# Kernel matrix for our case
#indices = np.random.permutation(len(x))
#x = x[indices,:]
#y = y[indices]
K = kernel_matrix(x,x)

# Start kernel perceptron loop
for t in range(T):
    counter = 0     # To check if all examples are classified correctly in loop
    for i in range(n):
        agreement = y[i]*(np.sum(alphas*y*(K[:,i].reshape(-1,1))) + theta0)
        if abs(agreement) < eps or agreement < 0.0:
            alphas[i] = alphas[i] + 1
            theta0 = theta0 + y[i]
        else:
            counter += 1
        
    # If all examples classified correctly, stop
    if counter == n:
        print("--------------------------------------------------------------")
        print("No. of iteration loops through the dataset:", t+1)
        print("--------------------------------------------------------------")
        break

# Initialize theta vector
theta = np.zeros((3,1))

# Calculate theta from calculated alphas
for i in range(n):
    theta = theta + alphas[i]*y[i]*quad_kernel(x[i,:])

print("theta0 =", theta0.item())
print("theta = [{:.2f}, {:.2f}, {:.2f}]".format(theta[0,0], theta[1,0], theta[2,0]))
print("----------------------------------------------------------------------")

print("=== Mistake Counts ===")
for i in range(n):
    print(x[i,:],":\t",alphas[i].item())

print("----------------------------------------------------------------------")
print("=== Classification Status ===")

for i in range(n):
    agreement = (y[i]*(theta.T.dot(quad_kernel(x[i,:])) + theta0)).item()
    if abs(agreement) < eps or agreement < 0.0:
        print("FAIL:\t", x[i,:])
    else:
        print("PASS:\t", x[i,:])

def decision_boundary(x, theta, theta0):
    return theta.T.dot(quad_kernel(x)) + theta0

# Plot in feature space
fig = plt.figure()
ax = Axes3D(fig)
pts = quad_kernel(x).T
ax.scatter3D(pts[:,0], pts[:,1], pts[:,2], s=30, c=colors)
xx, yy = np.meshgrid(np.linspace(*ax.get_xlim()), np.linspace(*ax.get_ylim()))
zz = (-theta0 - theta[0]*xx - theta[1]*yy)/theta[2]   # Linear decision boundary in feature space
ax.plot_surface(xx, yy, zz, cmap='winter', alpha=0.2)
ax.view_init(elev=10, azim=60)
ax.set_xlabel(r'$\Phi_1 = x_1^2$', fontsize=10)
ax.set_ylabel(r'$\Phi_2 = \sqrt{2}x_1x_2$', fontsize=10)
#ax.zaxis.set_rotate_label(False) 
ax.set_zlabel(r'$\Phi_3 = x_2^2$', fontsize=10)

# Plot decision boundary
#xx, yy = np.meshgrid(np.linspace(*ax.get_xlim()), np.linspace(*ax.get_ylim()))
#xx = xx.reshape(-1,2)
#z = decision_boundary(xx, theta, theta0)
#z = z.T
#ax.contour(xx, z, levels=[0])