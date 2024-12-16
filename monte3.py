import random
import matplotlib.pyplot as plt

def drop_marbles_circular_square(num_drops, edge_length=1):
    """
    Simulate dropping marbles randomly and compute cumulative ratios over time.
    """
    circular_count = 0
    square_count = 0
    ratios = []

    for i in range(1, num_drops + 1):
        # Generate random points within the square table
        x, y = random.uniform(-edge_length, edge_length), random.uniform(-edge_length, edge_length)

        # Check if the marble is within the square tray
        if abs(x) <= edge_length and abs(y) <= edge_length:
            square_count += 1
            # Check if the marble is also within the circular tray
            if x**2 + y**2 <= edge_length**2:
                circular_count += 1
        
        # Compute the current ratio
        if square_count > 0:
            ratio = circular_count / square_count
            ratios.append(ratio * 4)  # Multiply by 4 to estimate π

    return ratios

# Simulation parameters
num_drops = 10000  # Total number of marbles to drop
ratios = drop_marbles_circular_square(num_drops)

# Plot the results
plt.figure(figsize=(10, 6))
plt.plot(range(1, num_drops + 1), ratios, color='blue')
plt.axhline(y=3.14159, color='red', linestyle='--', label="π (Actual Value)")
plt.title("Convergence of Estimated π with Increasing Marble Drops")
plt.xlabel("Number of Marble Drops")
plt.ylabel("Estimated π")
plt.legend()
plt.grid()
plt.show()
