import random


# function to simulate random marble drops
def drop_marbles(num_drops, radius=1):

    circular_count = 0
    rectangular_count = 0

    for _ in range(num_drops):
        # Generate random point within the table
        # table width = 6, height = 4
        x, y = random.uniform(-4, 2), random.uniform(-2, 2)

        # Check if the point falls inside the circular tray
        # radius = 1, center = (0, 0)
        if x**2 + y**2 <= radius**2:
            circular_count += 1

        # Check if the point falls inside the rectangular (square shape) tray
        # (side length = radius), positioned at (-2.5, 0)
        if -3 <= x <= -2 and -0.5 <= y <= 0.5:
            rectangular_count += 1

    prob_circular = circular_count / num_drops
    prob_rectangular = rectangular_count / num_drops

    return circular_count, rectangular_count, prob_circular, prob_rectangular


# Test drop_marbles function with a number of drops
circular_count, rectangular_count, prob_circular, prob_rectangular = drop_marbles(10000)
print(f"Marbles in Circular Tray: {circular_count}")
print(f"Marbles in Rectangular Tray: {rectangular_count}")
print(f"Probability of landing marbles in Circular Tray: {prob_circular}")
print(f"Probability of landing marbles in Rectangular Tray: {prob_rectangular}")

# Fraction of the counts
ratio = circular_count / rectangular_count
print(f"Ratio of marbles in circular tray to rectangular tray: {ratio}")
