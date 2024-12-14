import argparse
import random
import statistics
import pandas as pd
import matplotlib.pyplot as plt
import math


def estimate_circle_pi(N):
    """Estimate π using Monte Carlo simulation and also compute probabilities for circular and rectangular trays."""
    inside_circle = 0
    inside_rectangle = 0

    # Define rectangular tray coordinates
    # For demonstration: a 0.5x0.5 square in the bottom-left corner of the bounding square
    rect_x_min, rect_x_max = -1.0, -0.5
    rect_y_min, rect_y_max = -1.0, -0.5

    for _ in range(N):
        x = random.uniform(-1, 1)
        y = random.uniform(-1, 1)

        # Check inside circle (center=0,0; radius=1)
        if x * x + y * y <= 1:
            inside_circle += 1

        # Check inside rectangle
        if rect_x_min <= x <= rect_x_max and rect_y_min <= y <= rect_y_max:
            inside_rectangle += 1

    pi_estimate = 4 * (inside_circle / N)
    prob_circle = inside_circle / N
    prob_rectangle = inside_rectangle / N
    return pi_estimate, prob_circle, prob_rectangle


def compute_mode(values):
    """Compute mode of a list of float values.
    If all are unique, we can return None or handle by rounding."""
    rounded_vals = [round(v, 5) for v in values]
    try:
        return statistics.mode(rounded_vals)
    except statistics.StatisticsError:
        # If no unique mode, return None or pick the first
        return None


def run_simulation(N_values, save_to_excel):
    results = []

    for N in N_values:
        pi_estimates = []
        circle_probs = []
        rect_probs = []

        # Run 10 experiments
        for _ in range(10):
            pi_val, p_circle, p_rect = estimate_circle_pi(N)
            pi_estimates.append(pi_val)
            circle_probs.append(p_circle)
            rect_probs.append(p_rect)

        mean_pi = statistics.mean(pi_estimates)
        mode_pi = compute_mode(pi_estimates)
        mean_circle_prob = statistics.mean(circle_probs)
        mean_rect_prob = statistics.mean(rect_probs)

        result_record = {
            "N": N,
            "Pi_Estimates": pi_estimates,
            "Mean_Pi": mean_pi,
            "Mode_Pi": mode_pi,
            "Circle_Probabilities": circle_probs,
            "Mean_Circle_Prob": mean_circle_prob,
            "Rect_Probabilities": rect_probs,
            "Mean_Rect_Prob": mean_rect_prob,
        }
        results.append(result_record)

        # Print results for quick check
        print(f"For N={N}:")
        print(f" Pi Estimates: {pi_estimates}")
        print(f" Mean Pi: {mean_pi}, Mode Pi: {mode_pi}")
        print(f" Mean Circle Probability: {mean_circle_prob}")
        print(f" Mean Rect Probability: {mean_rect_prob}")
        print("-" * 50)

    if save_to_excel:
        data_rows = []
        for r in results:
            row = {
                "N": r["N"],
                "Mean_Pi": r["Mean_Pi"],
                "Mode_Pi": r["Mode_Pi"],
                "Mean_Circle_Prob": r["Mean_Circle_Prob"],
                "Mean_Rect_Prob": r["Mean_Rect_Prob"],
            }
            for i, (pi_val, c_val, rect_val) in enumerate(
                zip(
                    r["Pi_Estimates"],
                    r["Circle_Probabilities"],
                    r["Rect_Probabilities"],
                ),
                start=1,
            ):
                row[f"Pi_Run_{i}"] = pi_val
                row[f"Circle_Prob_Run_{i}"] = c_val
                row[f"Rect_Prob_Run_{i}"] = rect_val
            data_rows.append(row)

        df = pd.DataFrame(data_rows)
        df.to_excel("monte_carlo_pi_results_with_rectangle.xlsx", index=False)
        print("Results saved to monte_carlo_pi_results_with_rectangle.xlsx")

    # Plot the convergence of Pi (using mean values)
    plt.figure(figsize=(10, 6))
    Ns = [r["N"] for r in results]
    mean_pis = [r["Mean_Pi"] for r in results]

    plt.plot(Ns, mean_pis, marker="o", label="Mean of Pi Estimates")
    plt.axhline(y=math.pi, color="r", linestyle="--", label="Actual π")
    plt.xscale("log")
    plt.xlabel("Number of Samples (N)")
    plt.ylabel("Estimated π")
    plt.title("Monte Carlo π Estimation Convergence")
    plt.legend()
    plt.savefig("pi_convergence_plot_with_rectangle.png")
    print("Plot saved as pi_convergence_plot_with_rectangle.png")


def main():
    parser = argparse.ArgumentParser(
        description="Monte Carlo Simulation to Estimate Pi and Tray Probabilities"
    )
    parser.add_argument(
        "-n",
        "--values",
        nargs="+",
        type=int,
        default=[1000, 10000, 100000, 1000000],
        help="List of N values to run simulations for (e.g. --values 1000 10000)",
    )
    parser.add_argument(
        "-e","--excel", action="store_true", help="Save results to an Excel file."
    )
    args = parser.parse_args()

    run_simulation(args.values, args.excel)


if __name__ == "__main__":
    main()
