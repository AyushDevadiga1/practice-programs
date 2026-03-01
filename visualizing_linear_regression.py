import numpy as np
import plotly.graph_objects as go

# 1. Define the "Floor" (The Column Space of X)
# We'll create a plane centered at z=0 for visual clarity
x_range = np.linspace(-5, 5, 10)
y_range = np.linspace(-5, 5, 10)
X_grid, Y_grid = np.meshgrid(x_range, y_range)
Z_grid = np.zeros_like(X_grid) # The floor is at z=0

# 2. Define the "Floating Ball" (Vector y)
# This is our actual data point hanging in the air
y_point = np.array([3, 4, 6]) 

# 3. Define the "Shadow" (The Projection y_hat)
# Since our floor is the Z=0 plane, the closest point is simply (x, y, 0)
y_hat = np.array([3, 4, 0])

# 4. Build the Visual Components
fig = go.Figure()

# Add the Floor (Column Space)
fig.add_trace(go.Surface(x=X_grid, y=Y_grid, z=Z_grid, 
                         colorscale='Blues', opacity=0.5, showscale=False, name='The Floor (X)'))

# Add the Floating Ball (Actual Data y)
fig.add_trace(go.Scatter3d(x=[y_point[0]], y=[y_point[1]], z=[y_point[2]],
                           mode='markers+text', marker=dict(size=8, color='red'),
                           text=["Floating Ball (y)"], textposition="top center", name='Real Data'))

# Add the Shadow (Prediction y_hat)
fig.add_trace(go.Scatter3d(x=[y_hat[0]], y=[y_hat[1]], z=[y_hat[2]],
                           mode='markers+text', marker=dict(size=8, color='blue'),
                           text=["The Shadow (y-hat)"], textposition="bottom center", name='Prediction'))

# Add the "Vertical String" (The Residual Vector)
fig.add_trace(go.Scatter3d(x=[y_point[0], y_hat[0]], 
                           y=[y_point[1], y_hat[1]], 
                           z=[y_point[2], y_hat[2]],
                           mode='lines', line=dict(color='green', width=6, dash='dash'),
                           name='The String (Error)'))

# Add an arrow from the origin to the Ball
fig.add_trace(go.Scatter3d(x=[0, y_point[0]], y=[0, y_point[1]], z=[0, y_point[2]],
                           mode='lines', line=dict(color='black', width=2), name='Vector y'))

# 5. Layout and Labels
fig.update_layout(
    title="OLS Visualization: The Shortest Distance to the Floor",
    scene=dict(
        xaxis_title='Feature 1',
        yaxis_title='Feature 2',
        zaxis_title='Target Variable',
        camera=dict(eye=dict(x=1.5, y=1.5, z=0.8)) # Set initial view angle
    ),
    margin=dict(l=0, r=0, b=0, t=40)
)

fig.show()