import pandas as pd
import matplotlib.pyplot as plt


def calculate_enterprise_value(base_fcf, growth_rate, discount_rate, terminal_growth_rate):
    projected_fcfs = []

    for year in range(1, 6):
        projected_fcf = base_fcf * ((1 + growth_rate) ** year)
        projected_fcfs.append(projected_fcf)

    discounted_fcfs = []

    for year, fcf in enumerate(projected_fcfs, start=1):
        discounted_fcf = fcf / ((1 + discount_rate) ** year)
        discounted_fcfs.append(discounted_fcf)

    final_year_fcf = projected_fcfs[-1]

    terminal_value = final_year_fcf * (1 + terminal_growth_rate) / (
        discount_rate - terminal_growth_rate
    )

    discounted_terminal_value = terminal_value / ((1 + discount_rate) ** 5)

    enterprise_value = sum(discounted_fcfs) + discounted_terminal_value

    return enterprise_value


def create_scenario_chart():
    scenario_results = pd.read_csv("outputs/scenario_analysis_results.csv")

    colors = ["#C44E52", "#4C72B0", "#55A868"]

    plt.figure(figsize=(9, 5.5))
    bars = plt.bar(
        scenario_results["scenario"],
        scenario_results["enterprise_value"] / 1_000_000,
        color=colors
    )

    plt.title("Garmin DCF Enterprise Value by Scenario", fontsize=14, fontweight="bold")
    plt.xlabel("Scenario")
    plt.ylabel("Enterprise Value ($ billions)")
    plt.grid(axis="y", linestyle="--", alpha=0.4)

    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            height,
            f"${height:.1f}B",
            ha="center",
            va="bottom",
            fontsize=10
        )

    plt.tight_layout()
    plt.savefig("outputs/scenario_chart.png", dpi=300)
    plt.close()


def create_sensitivity_analysis():
    base_fcf = 1594000
    terminal_growth_rate = 0.025

    discount_rates = [0.075, 0.08, 0.085, 0.09, 0.095]
    growth_rates = [0.02, 0.03, 0.04, 0.05, 0.06]

    results = []

    for growth_rate in growth_rates:
        for discount_rate in discount_rates:
            enterprise_value = calculate_enterprise_value(
                base_fcf,
                growth_rate,
                discount_rate,
                terminal_growth_rate
            )

            results.append(
                {
                    "growth_rate": growth_rate,
                    "discount_rate": discount_rate,
                    "enterprise_value": enterprise_value
                }
            )

    sensitivity_df = pd.DataFrame(results)
    sensitivity_df.to_csv("outputs/sensitivity_analysis.csv", index=False)

    return sensitivity_df


def create_sensitivity_chart(sensitivity_df):
    plt.figure(figsize=(10, 6))

    colors = {
        0.02: "#C44E52",
        0.03: "#DD8452",
        0.04: "#4C72B0",
        0.05: "#8172B3",
        0.06: "#55A868"
    }

    for growth_rate in sorted(sensitivity_df["growth_rate"].unique()):
        filtered_data = sensitivity_df[sensitivity_df["growth_rate"] == growth_rate]

        plt.plot(
            filtered_data["discount_rate"],
            filtered_data["enterprise_value"] / 1_000_000,
            marker="o",
            linewidth=2,
            color=colors[growth_rate],
            label=f"FCF Growth {growth_rate:.0%}"
        )

    plt.title("Garmin Valuation Sensitivity to WACC and FCF Growth", fontsize=14, fontweight="bold")
    plt.xlabel("Discount Rate / WACC")
    plt.ylabel("Enterprise Value ($ billions)")
    plt.grid(True, linestyle="--", alpha=0.4)
    plt.legend(title="Scenario Assumption")
    plt.tight_layout()

    plt.savefig("outputs/sensitivity_chart.png", dpi=300)
    plt.close()


if __name__ == "__main__":
    create_scenario_chart()

    sensitivity_df = create_sensitivity_analysis()
    create_sensitivity_chart(sensitivity_df)

    print("Scenario chart saved to outputs/scenario_chart.png")
    print("Sensitivity analysis saved to outputs/sensitivity_analysis.csv")
    print("Sensitivity chart saved to outputs/sensitivity_chart.png")