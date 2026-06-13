import os
import pandas as pd
from src.summary_generator import generate_analyst_summary
from src.ratios import calculate_ratios
from src.capm import load_market_assumptions, calculate_cost_of_equity
from src.wacc import calculate_wacc
from src.dcf import calculate_dcf_valuation
from src.scenario_analysis import calculate_enterprise_value
from src.sensitivity_analysis import (
    create_scenario_chart,
    create_sensitivity_analysis,
    create_sensitivity_chart
)


def run_financial_analysis():
    os.makedirs("outputs", exist_ok=True)

    financials = pd.read_csv("data/garmin_financials_template.csv")
    assumptions = load_market_assumptions("data/market_assumptions.csv")

    ratios = calculate_ratios(financials)
    ratios.to_csv("outputs/ratio_analysis_results.csv", index=False)

    risk_free_rate = float(assumptions["risk_free_rate"])
    beta = float(assumptions["beta"])
    market_risk_premium = float(assumptions["market_risk_premium"])
    tax_rate = float(assumptions["tax_rate"])
    cost_of_debt = float(assumptions["cost_of_debt"])
    debt_weight = float(assumptions["debt_weight"])

    cost_of_equity = calculate_cost_of_equity(
        risk_free_rate,
        beta,
        market_risk_premium
    )

    wacc, after_tax_cost_of_debt, equity_weight = calculate_wacc(
        cost_of_equity,
        cost_of_debt,
        tax_rate,
        debt_weight
    )

    base_fcf = float(assumptions["base_free_cash_flow"])
    growth_rate = float(assumptions["fcf_growth_rate"])
    terminal_growth_rate = float(assumptions["terminal_growth_rate"])

    projected_fcfs, discounted_fcfs, terminal_value, discounted_terminal_value, enterprise_value = calculate_dcf_valuation(
        base_fcf,
        growth_rate,
        wacc,
        terminal_growth_rate
    )

    summary_results = pd.DataFrame(
    [
        {
            "metric": "Cost of Equity",
            "value": cost_of_equity,
            "formatted_value": f"{cost_of_equity:.2%}",
            "interpretation": "Estimated using CAPM based on risk-free rate, beta, and market risk premium"
        },
        {
            "metric": "After-tax Cost of Debt",
            "value": after_tax_cost_of_debt,
            "formatted_value": f"{after_tax_cost_of_debt:.2%}",
            "interpretation": "Reflects tax shield benefit on debt financing"
        },
        {
            "metric": "Debt Weight",
            "value": debt_weight,
            "formatted_value": f"{debt_weight:.2%}",
            "interpretation": "Assumed debt share in the target capital structure"
        },
        {
            "metric": "Equity Weight",
            "value": equity_weight,
            "formatted_value": f"{equity_weight:.2%}",
            "interpretation": "Implied equity share in the target capital structure"
        },
        {
            "metric": "WACC",
            "value": wacc,
            "formatted_value": f"{wacc:.2%}",
            "interpretation": "Weighted average cost of capital used as the DCF discount rate"
        },
        {
            "metric": "DCF Enterprise Value",
            "value": enterprise_value,
            "formatted_value": f"${enterprise_value / 1_000_000:.2f} billion",
            "interpretation": "Estimated enterprise value from simplified DCF valuation"
        }
    ]
)

    summary_results.to_csv("outputs/valuation_summary.csv", index=False)

    scenarios = {
        "Pessimistic": {
            "growth_rate": 0.02,
            "discount_rate": 0.095,
            "terminal_growth_rate": 0.015
        },
        "Base": {
            "growth_rate": growth_rate,
            "discount_rate": wacc,
            "terminal_growth_rate": terminal_growth_rate
        },
        "Optimistic": {
            "growth_rate": 0.06,
            "discount_rate": 0.075,
            "terminal_growth_rate": 0.03
        }
    }

    scenario_results = []

    for scenario_name, scenario_assumptions in scenarios.items():
        scenario_enterprise_value = calculate_enterprise_value(
            base_fcf,
            scenario_assumptions["growth_rate"],
            scenario_assumptions["discount_rate"],
            scenario_assumptions["terminal_growth_rate"]
        )

        scenario_results.append(
            {
                "scenario": scenario_name,
                "growth_rate": scenario_assumptions["growth_rate"],
                "discount_rate": scenario_assumptions["discount_rate"],
                "terminal_growth_rate": scenario_assumptions["terminal_growth_rate"],
                "enterprise_value": scenario_enterprise_value
            }
        )

    scenario_results_df = pd.DataFrame(scenario_results)
    scenario_results_df.to_csv("outputs/scenario_analysis_results.csv", index=False)
    analyst_summary = generate_analyst_summary(
        ratios,
        summary_results,
        scenario_results_df
    )

    with open("outputs/analyst_summary.txt", "w") as file:
        file.write(analyst_summary)

    create_scenario_chart()

    sensitivity_df = create_sensitivity_analysis()
    create_sensitivity_chart(sensitivity_df)

    print("Automated Financial Analysis Toolkit")
    print("------------------------------------")
    print("Ratio analysis saved to outputs/ratio_analysis_results.csv")
    print("Valuation summary saved to outputs/valuation_summary.csv")
    print("Scenario analysis saved to outputs/scenario_analysis_results.csv")
    print("Analyst summary saved to outputs/analyst_summary.txt")
    print("Scenario chart saved to outputs/scenario_chart.png")
    print("Sensitivity analysis saved to outputs/sensitivity_analysis.csv")
    print("Sensitivity chart saved to outputs/sensitivity_chart.png")
    print()
    print(f"Cost of equity: {cost_of_equity:.2%}")
    print(f"WACC: {wacc:.2%}")
    print(f"DCF enterprise value: ${enterprise_value / 1_000_000:.2f} billion")


if __name__ == "__main__":
    run_financial_analysis()