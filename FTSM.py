import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata, interp1d
from scipy.spatial import Delaunay
from numpy.random import randn
import tkinter as tk
from tkinter import filedialog, simpledialog

# Function to load PES data file
def load_pes_file():
    """Open a file dialog to select the PES file."""
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    file_path = filedialog.askopenfilename(filetypes=(('Text files', '*.txt'), ('All files', '*.*')))
    return file_path

# Function to get initial string endpoints from the user
def get_initial_endpoints():
    """Ask the user for two pairs of coordinates to initialize the string."""
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    xa = simpledialog.askfloat("Input", "Enter x-coordinate for the first endpoint:")
    ya = simpledialog.askfloat("Input", "Enter y-coordinate for the first endpoint:")
    xb = simpledialog.askfloat("Input", "Enter x-coordinate for the second endpoint:")
    yb = simpledialog.askfloat("Input", "Enter y-coordinate for the second endpoint:")

    if None in (xa, ya, xb, yb):
        raise ValueError("All four coordinates must be provided.")

    return xa, ya, xb, yb

# Load PES data interactively
pes_file = load_pes_file()
if not pes_file:
    raise ValueError("No PES file selected.")

# Load and process PES data
data = np.loadtxt(pes_file)
x_unique = np.unique(data[:, 0])
y_unique = np.unique(data[:, 1])
xmin, xmax = x_unique.min(), x_unique.max()
ymin, ymax = y_unique.min(), y_unique.max()
x, y = np.meshgrid(x_unique, y_unique)
z = data[:, 2].reshape(x.shape)

# Ask the user for initial string endpoints
xa, ya, xb, yb = get_initial_endpoints()

# Initialization
mu = 9  # Temperature parameter
npts = 60  # Number of intermediate points on the string
stepmax = 100  # Maximum steps for evolution

# Create the initial string
g1 = np.linspace(0, 1, npts)
pts = np.vstack([
    np.linspace(xa, xb, npts),
    np.linspace(ya, yb, npts)
]).T

# Compute gradients of the potential
gradx, grady = np.gradient(z, np.unique(data[:, 0]), np.unique(data[:, 1]))
gridpoints = np.vstack([x.flatten(), y.flatten()]).T

# Best iteration tracking
best_iteration = 0
best_value = np.inf
best_pts = None

# String evolution loop
for i in range(stepmax):
    Dx = griddata(gridpoints, gradx.flatten(), (pts[:, 0], pts[:, 1]), method='linear')
    Dy = griddata(gridpoints, grady.flatten(), (pts[:, 0], pts[:, 1]), method='linear')
    h = np.amax(np.sqrt(np.square(Dx) + np.square(Dy)))
    pts -= 0.01 * np.vstack([Dx, Dy]).T / h

    # Reparameterize the string
    arclength = np.hstack([0, np.cumsum(np.linalg.norm(pts[1:] - pts[:-1], axis=1))])
    arclength /= arclength[-1]
    pts = np.vstack([
        interp1d(arclength, pts[:, 0])(np.linspace(0, 1, npts)),
        interp1d(arclength, pts[:, 1])(np.linspace(0, 1, npts))
    ]).T

    # Compute free energy sum and track the best result
    current_value = np.sum(griddata(gridpoints, z.flatten(), (pts[:, 0], pts[:, 1]), method='linear'))
    if current_value < best_value:
        best_value = current_value
        best_iteration = i
        best_pts = pts.copy()

print(f"Best iteration: {best_iteration} with free energy sum: {best_value}")

# Use best_pts for final coordinates
final_x = best_pts[:, 0]
final_y = best_pts[:, 1]
final_z = griddata(gridpoints, z.flatten(), (final_x, final_y), method='linear')

# Save final string coordinates
np.savetxt("final_string_coordinates.txt", np.column_stack([final_x, final_y, final_z]),
           header="X\tY\tZ", fmt="%.8f", delimiter="\t")

# Plot and save the final evolved string
plt.figure(figsize=(8, 6))
cbar_limits = (np.nanmin(z), np.nanmax(z))
plt.contourf(x_unique, y_unique, z, levels=40, cmap="coolwarm", vmin=cbar_limits[0], vmax=cbar_limits[1])
plt.plot(final_x, final_y, 'w.-', markersize=16)
plt.xlabel('x', fontsize=12, fontstyle='italic')
plt.ylabel('y', fontsize=12, fontstyle='italic')
plt.title('Final Evolved String', fontsize=14)
plt.colorbar(label="Energy")
plt.savefig("final_evolved_string.png", dpi=300)
plt.show()

print("Final string coordinates and plot saved.")
