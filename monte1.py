import random
import pandas as pd
import matplotlib.pyplot as plt
from statistics import mean, mode
import argparse


def monte_carlo_pi_simulation(num_drops):
    """Simulate the process of estimating Pi using random points."""
    inside_circle = 0
    for _ in range(num_drops):
        x, y = random.uniform(-1, 1), random.uniform(-1, 1)
        if x**2 + y**2 <= 1:
            inside_circle += 1
    return 4 * inside_circle / num_drops


def run_simulation(trials, output_excel):
    """Run Monte Carlo simulation for specified trials."""
    results = []

    for N in trials:
        estimates = [monte_carlo_pi_simulation(N) for _ in range(10)]
        avg = mean(estimates)
        mod = mode(estimates)
        results.append({"N": N, "Mean Pi": avg, "Mode Pi": mod, "Estimates": estimates})

        # Print results to terminal
        print(f"Results for N={N}:")
        print(f"  Mean Pi: {avg}")
        print(f"  Mode Pi: {mod}")
        print(f"  Estimates: {estimates}")
        print("-" * 50)

    if output_excel:
        # Save to Excel
        df = pd.DataFrame(results)
        df.to_excel("monte_carlo_pi_results.xlsx", index=False)
        print("Results saved to monte_carlo_pi_results.xlsx")

    # Plotting
    plt.figure(figsize=(10, 6))
    for res in results:
        plt.scatter([res["N"]] * 10, res["Estimates"], label=f"N={res['N']}", alpha=0.6)
    plt.plot(
        trials,
        [r["Mean Pi"] for r in results],
        label="Mean Pi",
        color="red",
        marker="o",
    )
    plt.axhline(y=3.14159, color="blue", linestyle="--", label="Actual Pi")
    plt.xlabel("Number of Drops (N)")
    plt.ylabel("Estimated Pi")
    plt.title("Monte Carlo Simulation of Pi by Group R")
    plt.legend()
    plt.savefig("monte_carlo_pi_plot.png")
    print("Graph saved to monte_carlo_pi_plot.png")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Monte Carlo Simulation to Estimate Pi"
    )
    parser.add_argument(
        "-n",
        "--trials",
        type=int,
        nargs="+",
        default=[1000, 10000, 100000, 1000000],
        help="Number of trials to run (space-separated for multiple).",
    )
    parser.add_argument(
        "-e", "--excel", action="store_true", help="Save results to an Excel file."
    )

    args = parser.parse_args()
    run_simulation(args.trials, args.excel)
