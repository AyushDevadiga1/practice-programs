"""
LOGISTIC REGRESSION — SCIENTIST STYLE VISUAL LAB

Goal:
Understand logistic regression by visualizing EVERY mathematical object.

We will visualize:

X  -> feature matrix
w  -> parameter vector
b  -> bias
z  -> linear score
σ  -> sigmoid transformation
P  -> probability
Loss -> log likelihood
Training -> gradient descent

Run this file step-by-step.
"""

import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go

np.random.seed(0)

# ============================================================
# STEP 1 — CREATE A DATASET (OBSERVATIONS)
# ============================================================

print("\nSTEP 1 — Creating observations")

class0 = np.random.randn(50,2) + np.array([-2,-2])
class1 = np.random.randn(50,2) + np.array([2,2])

X = np.vstack([class0, class1])
y = np.hstack([np.zeros(50), np.ones(50)])

print("Feature matrix shape:", X.shape)
print("Label vector shape:", y.shape)

# ============================================================
# STEP 2 — VISUALIZE THE OBSERVATIONS
# ============================================================

print("\nSTEP 2 — Visualizing raw data geometry")

plt.figure(figsize=(6,6))

plt.scatter(class0[:,0], class0[:,1], label="Class 0")
plt.scatter(class1[:,0], class1[:,1], label="Class 1")

plt.xlabel("Feature x1")
plt.ylabel("Feature x2")

plt.title("Observed Data")

plt.legend()
plt.show()

# ============================================================
# STEP 3 — EXAMINE FEATURE MATRIX X
# ============================================================

print("\nSTEP 3 — Understanding the matrix X")

print("\nFirst 5 rows of X:")
print(X[:5])

print("\nInterpretation:")
print("Each row = one observation")
print("Each column = one feature")

# ============================================================
# STEP 4 — MODEL PARAMETERS
# ============================================================

print("\nSTEP 4 — Define parameter vector")

w = np.array([0.5, -0.5])
b = 0

print("Initial w:", w)
print("Initial b:", b)

# ============================================================
# STEP 5 — LINEAR MODEL
# ============================================================

print("\nSTEP 5 — Linear model z = w^T x + b")

z = X @ w + b

print("First 10 linear scores:")
print(z[:10])

plt.figure()

plt.scatter(range(len(z)), z)

plt.title("Linear Scores z")

plt.xlabel("Sample index")
plt.ylabel("z")

plt.show()

# ============================================================
# STEP 6 — DECISION BOUNDARY GEOMETRY
# ============================================================

print("\nSTEP 6 — Visualizing the decision boundary")

x_vals = np.linspace(-6,6,100)
y_vals = -(w[0]/w[1])*x_vals - b/w[1]

plt.figure(figsize=(6,6))

plt.scatter(class0[:,0], class0[:,1])
plt.scatter(class1[:,0], class1[:,1])

plt.plot(x_vals,y_vals)

plt.title("Initial Decision Boundary")

plt.show()

# ============================================================
# STEP 7 — SIGMOID TRANSFORMATION
# ============================================================

print("\nSTEP 7 — Sigmoid function")

def sigmoid(z):
    return 1/(1+np.exp(-z))

z_vals = np.linspace(-10,10,200)
s_vals = sigmoid(z_vals)

plt.figure()

plt.plot(z_vals,s_vals)

plt.title("Sigmoid Function")

plt.xlabel("z")
plt.ylabel("σ(z)")

plt.show()

# ============================================================
# STEP 8 — CONVERT SCORES TO PROBABILITIES
# ============================================================

print("\nSTEP 8 — Convert linear scores to probabilities")

probs = sigmoid(z)

plt.figure()

plt.scatter(range(len(probs)), probs)

plt.title("Predicted Probabilities")

plt.xlabel("Sample index")
plt.ylabel("P(y=1|x)")

plt.show()

# ============================================================
# STEP 9 — PROBABILITY LANDSCAPE
# ============================================================

print("\nSTEP 9 — Probability surface")

x_range = np.linspace(-6,6,50)
y_range = np.linspace(-6,6,50)

xx,yy = np.meshgrid(x_range,y_range)

grid = np.c_[xx.ravel(),yy.ravel()]

z_grid = sigmoid(grid @ w + b)

z_grid = z_grid.reshape(xx.shape)

fig = go.Figure(data=[go.Surface(x=xx,y=yy,z=z_grid)])

fig.update_layout(
    title="Probability Surface P(y=1|x)",
    scene=dict(
        xaxis_title="x1",
        yaxis_title="x2",
        zaxis_title="Probability"
    )
)

fig.show()

# ============================================================
# STEP 10 — LOSS FUNCTION
# ============================================================

print("\nSTEP 10 — Log loss visualization")

p = np.linspace(0.001,0.999,200)

loss_y1 = -np.log(p)
loss_y0 = -np.log(1-p)

plt.figure()

plt.plot(p,loss_y1,label="True label = 1")
plt.plot(p,loss_y0,label="True label = 0")

plt.title("Logistic Loss")

plt.xlabel("Predicted probability")

plt.ylabel("Loss")

plt.legend()

plt.show()

# ============================================================
# STEP 11 — GRADIENT DESCENT
# ============================================================

print("\nSTEP 11 — Training using gradient descent")

lr = 0.1

for epoch in range(100):

    z = X @ w + b
    p = sigmoid(z)

    grad_w = X.T @ (p - y)/len(y)
    grad_b = np.mean(p - y)

    w -= lr*grad_w
    b -= lr*grad_b

print("\nLearned parameters:")
print("w:", w)
print("b:", b)

# ============================================================
# STEP 12 — FINAL DECISION BOUNDARY
# ============================================================

print("\nSTEP 12 — Final learned boundary")

x_vals = np.linspace(-6,6,100)
y_vals = -(w[0]/w[1])*x_vals - b/w[1]

plt.figure(figsize=(6,6))

plt.scatter(class0[:,0],class0[:,1])
plt.scatter(class1[:,0],class1[:,1])

plt.plot(x_vals,y_vals)

plt.title("Learned Decision Boundary")

plt.show()

print("\nExperiment complete.")