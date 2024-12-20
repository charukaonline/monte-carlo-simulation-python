import random
import argparse
import pandas as pd
from statistics import mean, mode
import matplotlib.pyplot as plt


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

    # Compute probabilities
    prob_circular = circular_count / num_drops
    prob_rectangular = rectangular_count / num_drops

    return circular_count, rectangular_count, prob_circular, prob_rectangular


def run_simulation(trials, num_drops_list):

    # Run simulation for different values of N and repeat each experiment.

    results = []
    mean_values = []

    for num_drops in num_drops_list:
        estimates = []

        print(f"\nRunning Simulation for N = {num_drops} (Repetitions = {trials})")

        for trial in range(1, trials + 1):
            circular_count, rectangular_count, prob_circular, prob_rectangular = (
                drop_marbles(num_drops)
            )

            # Estimate pi based on the ratio of counts
            if rectangular_count > 0:
                pi_estimate = circular_count / rectangular_count
            else:
                pi_estimate = 0

            print(
                f"  Trial {trial}: Prob of circular={prob_circular:.6f}, Prob of rectangular={prob_rectangular:.6f}, π={pi_estimate:.5f}"
            )
            estimates.append(pi_estimate)

            # Append trial results including probabilities
            results.append(
                [num_drops, trial, pi_estimate, prob_circular, prob_rectangular]
            )

        # Compute mean and mode
        mean_pi = mean(estimates)
        try:
            mode_pi = mode(estimates)
        except:
            mode_pi = "All unique estimates"

        # Print mean and mode for the current N
        print(f"  Mean π for N={num_drops}: {mean_pi:.5f}")
        print(f"  Mode π for N={num_drops}: {mode_pi}")

        # Append results for mean and mode
        results.append([num_drops, "Mean", mean_pi, "", ""])
        results.append([num_drops, "Mode", mode_pi, "", ""])

        # Save the mean value for plotting
        mean_values.append((num_drops, mean_pi))

    return results, mean_values


def save_to_excel(results, filename="simulation_results.xlsx"):

    # Save the simulation results to an Excel file.
    df = pd.DataFrame(
        results,
        columns=[
            "N",
            "Trial",
            "Estimated π",
            "Prob for circular",
            "Prob for rectangular",
        ],
    )
    df.to_excel(filename, index=False)
    print(f"\nResults saved to {filename}")


def plot_convergence(mean_values, filename="pi_convergence_plot.png"):

    # Plot the mean values of π for each N and save the plot to a PNG file.
    n_values = [item[0] for item in mean_values]
    pi_means = [item[1] for item in mean_values]
    real_pi = [3.14159] * len(n_values)  # The real value of pi

    plt.figure(figsize=(10, 6))
    plt.plot(n_values, pi_means, label="Mean Estimated π", marker="o", linestyle="-")
    plt.plot(n_values, real_pi, label="Real π", color="red", linestyle="--")
    plt.xscale("log")  # Logarithmic scale for clarity
    plt.title("Convergence of Mean π to the Real Value")
    plt.xlabel("Number of Drops (N)")
    plt.ylabel("Estimated π")
    plt.legend()
    plt.grid()
    plt.savefig(filename)
    print(f"Plot saved to {filename}")


def main():
    parser = argparse.ArgumentParser(
        description="Monte Carlo simulation for estimating π"
    )
    parser.add_argument(
        "-t", "--trials", type=int, default=10, help="Number of trials per simulation"
    )
    parser.add_argument(
        "-n",
        "--drops",
        type=int,
        nargs="+",
        default=[1000, 10000, 100000, 1000000],
        help="List of marble drop counts (N)",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default="simulation_results.xlsx",
        help="Excel filename for simulation results",
    )
    parser.add_argument(
        "-p",
        "--plot",
        type=str,
        default="pi_convergence_plot.png",
        help="Plot filename for graph",
    )

    args = parser.parse_args()

    print("Starting simulation...")
    results, mean_values = run_simulation(args.trials, args.drops)
    save_to_excel(results, args.output)
    plot_convergence(mean_values, args.plot)
    print("Simulation complete!")


if __name__ == "__main__":
    main()
