import random
import argparse
import pandas as pd
from statistics import mean, mode


def drop_marbles(num_drops, edge_length=1):
    """
    Simulate random marble drops on a rectangular table.
    Count marbles that fall into the circular and square trays.
    """
    circular_count = 0
    square_count = 0

    for _ in range(num_drops):
        # Generate random point within the table
        x, y = random.uniform(-edge_length, edge_length), random.uniform(
            -edge_length, edge_length
        )

        # Check if the point falls inside the circular tray (radius = edge_length)
        if x**2 + y**2 <= edge_length**2:
            circular_count += 1

        # Check if the point falls inside the square tray (side length = edge_length)
        if abs(x) <= edge_length / 2 and abs(y) <= edge_length / 2:  # Centered square
            square_count += 1

    return circular_count, square_count


def run_simulation(trials, num_drops_list):
    """
    Run the simulation for different values of N and repeat each experiment.
    """
    results = []

    for num_drops in num_drops_list:
        estimates = []

        for trial in range(1, trials + 1):
            circular_count, square_count = drop_marbles(num_drops)

            # Estimate pi based on the ratio of counts
            if square_count > 0:
                pi_estimate = circular_count / square_count
            else:
                pi_estimate = 0

            print(
                f"N={num_drops}, Trial={trial}, Circular={circular_count}, Square={square_count}, π={pi_estimate:.5f}"
            )
            estimates.append(pi_estimate)

        # Compute mean and mode
        mean_pi = mean(estimates)
        try:
            mode_pi = mode(estimates)
        except:
            mode_pi = "No mode"

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
        description="Monte Carlo Simulation for Estimating π with Separate Trays"
    )
    parser.add_argument(
        "--trials", type=int, default=10, help="Number of trials per simulation"
    )
    parser.add_argument(
        "--drops",
        type=int,
        nargs="+",
        default=[1000, 10000, 100000, 1000000],
        help="List of marble drop counts (space-separated)",
    )
    parser.add_argument(
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
