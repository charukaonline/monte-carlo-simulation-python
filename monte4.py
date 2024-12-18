import random
import argparse
import pandas as pd
from statistics import mean, mode


def drop_marbles_circular_square(num_drops, edge_length=1):
    """
    Simulate dropping marbles randomly and compute an estimate for π.
    """
    circular_count = 0
    square_count = 0

    for _ in range(num_drops):
        x, y = random.uniform(-edge_length, edge_length), random.uniform(
            -edge_length, edge_length
        )

        # Count if within the square tray
        if abs(x) <= edge_length and abs(y) <= edge_length:
            square_count += 1
            # Check for circular tray
            if x**2 + y**2 <= edge_length**2:
                circular_count += 1

    # Estimate π based on ratio
    return (circular_count / square_count) * 4


def run_simulation(trials, num_drops_list):
    """
    Run the simulation for different values of N and repeat each experiment.
    """
    results = []
    for num_drops in num_drops_list:
        estimates = []
        for trial in range(1, trials + 1):
            pi_estimate = drop_marbles_circular_square(num_drops)
            estimates.append(pi_estimate)
            print(f"N={num_drops}, Trial={trial}, Estimated π={pi_estimate:.5f}")

        # Compute mean and mode
        mean_pi = mean(estimates)
        try:
            mode_pi = mode(estimates)
        except:
            mode_pi = "No mode"  # Handle case where there's no mode

        # Append results
        for trial, pi_value in enumerate(estimates, start=1):
            results.append([num_drops, trial, pi_value])
        results.append([num_drops, "Mean", mean_pi])
        results.append([num_drops, "Mode", mode_pi])
    return results


def save_to_excel(results, filename="pi_simulation_results.xlsx"):
    """
    Save the simulation results to an Excel file.
    """
    df = pd.DataFrame(results, columns=["Drops", "Trial", "Estimated π"])
    df.to_excel(filename, index=False)
    print(f"Results saved to {filename}")


def main():
    parser = argparse.ArgumentParser(
        description="Monte Carlo Simulation for Estimating π"
    )
    parser.add_argument(
        "-t",
        "--trials", type=int, default=10, help="Number of trials per simulation"
    )
    parser.add_argument(
        "-n",
        "--drops",
        type=int,
        nargs="+",
        default=[1000, 10000, 100000, 1000000],
        help="List of marble drop counts (space-separated)",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default="pi_simulation_results.xlsx",
        help="Output Excel filename",
    )

    args = parser.parse_args()

    print("Starting simulation...")
    results = run_simulation(args.trials, args.drops)
    save_to_excel(results, args.output)
    print("Simulation complete!")


if __name__ == "__main__":
    main()
