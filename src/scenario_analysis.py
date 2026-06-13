import pandas as pd


def project_free_cash_flows(base_fcf, growth_rate, years=5):
    projected_fcfs = []

    for year in range(1, years + 1):
        projected_fcf = base_fcf * ((1 + growth_rate) ** year)
        projected_fcfs.append(projected_fcf)

    return projected_fcfs


def discount_cash_flows(projected_fcfs, discount_rate):
    discounted_fcfs = []

    for year, fcf in enumerate(projected_fcfs, start=1):
        discounted_fcf = fcf / ((1 + discount_rate) ** year)
        discounted_fcfs.append(discounted_fcf)

    return discounted_fcfs


def calculate_terminal_value(final_year_fcf, discount_rate, terminal_growth_rate):
    terminal_value = final_year_fcf * (1 + terminal_growth_rate) / (
        discount_rate - terminal_growth_rate
    )
    return terminal_value


def calculate_enterprise_value(base_fcf, growth_rate, discount_rate, terminal_growth_rate):
    projected_fcfs = project_free_cash_flows(base_fcf, growth_rate)
    discounted_fcfs = discount_cash_flows(projected_fcfs, discount_rate)

    terminal_value = calculate_terminal_value(
        projected_fcfs[-1],
        discount_rate,
        terminal_growth_rate
    )

    discounted_terminal_value = terminal_value / ((1 + discount_rate) ** 5)
    enterprise_value = sum(discounted_fcfs) + discounted_terminal_value

    return enterprise_value


if __name__ == "__main__":
    base_fcf = 1594000

    scenarios = {
        "Pessimistic": {
            "growth_rate": 0.02,
            "discount_rate": 0.095,
            "terminal_growth_rate": 0.015
        },
        "Base": {
            "growth_rate": 0.04,
            "discount_rate": 0.0826,
            "terminal_growth_rate": 0.025
        },
        "Optimistic": {
            "growth_rate": 0.06,
            "discount_rate": 0.075,
            "terminal_growth_rate": 0.03
        }
    }

    results = []

    for scenario_name, assumptions in scenarios.items():
        enterprise_value = calculate_enterprise_value(
            base_fcf,
            assumptions["growth_rate"],
            assumptions["discount_rate"],
            assumptions["terminal_growth_rate"]
        )

        results.append(
            {
                "scenario": scenario_name,
                "growth_rate": assumptions["growth_rate"],
                "discount_rate": assumptions["discount_rate"],
                "terminal_growth_rate": assumptions["terminal_growth_rate"],
                "enterprise_value": enterprise_value
            }
        )

    results_df = pd.DataFrame(results)

    print("Scenario Analysis")
    print("-----------------")
    print(results_df)

    results_df.to_csv("outputs/scenario_analysis_results.csv", index=False)
    print("Scenario analysis results saved to outputs/scenario_analysis_results.csv")
