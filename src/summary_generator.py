import pandas as pd


def generate_analyst_summary(
    ratio_results,
    valuation_summary,
    scenario_results
):
    latest_year_data = ratio_results.sort_values("year").iloc[-1]

    cost_of_equity = valuation_summary[
        valuation_summary["metric"] == "Cost of Equity"
    ]["formatted_value"].iloc[0]

    wacc = valuation_summary[
        valuation_summary["metric"] == "WACC"
    ]["formatted_value"].iloc[0]

    enterprise_value = valuation_summary[
        valuation_summary["metric"] == "DCF Enterprise Value"
    ]["formatted_value"].iloc[0]

    base_scenario = scenario_results[
        scenario_results["scenario"] == "Base"
    ]["enterprise_value"].iloc[0]

    pessimistic_scenario = scenario_results[
        scenario_results["scenario"] == "Pessimistic"
    ]["enterprise_value"].iloc[0]

    optimistic_scenario = scenario_results[
        scenario_results["scenario"] == "Optimistic"
    ]["enterprise_value"].iloc[0]

    summary = f"""
Garmin Financial Analysis Summary

Garmin demonstrates strong profitability based on the latest available ratio analysis. In {latest_year_data["year"]}, the company reported ROA of {latest_year_data["roa_pct"]} and ROE of {latest_year_data["roe_pct"]}, both classified as {latest_year_data["roe_interpretation"].lower()} under the toolkit's interpretation framework.

The company also maintains a conservative leverage profile, with a debt ratio of {latest_year_data["debt_ratio_pct"]}. Interest coverage is marked as {latest_year_data["interest_coverage"]} because Garmin has no meaningful interest expense in the input data.

Using the CAPM approach, Garmin's estimated cost of equity is {cost_of_equity}. After incorporating the assumed cost of debt, tax rate, and target capital structure, the estimated WACC is {wacc}. This WACC is used as the discount rate in the base-case DCF model.

Under the base-case DCF scenario, Garmin's enterprise value is estimated at approximately {enterprise_value}. The scenario analysis shows a valuation range from approximately ${pessimistic_scenario / 1_000_000:.1f} billion in the pessimistic case to approximately ${optimistic_scenario / 1_000_000:.1f} billion in the optimistic case.

Overall, the toolkit suggests that Garmin combines strong profitability, conservative leverage, and meaningful valuation sensitivity to growth and discount rate assumptions. This analysis is intended as a simplified financial modelling exercise rather than a full investment recommendation.
"""

    return summary.strip()


if __name__ == "__main__":
    ratio_results = pd.read_csv("outputs/ratio_analysis_results.csv")
    valuation_summary = pd.read_csv("outputs/valuation_summary.csv")
    scenario_results = pd.read_csv("outputs/scenario_analysis_results.csv")

    summary = generate_analyst_summary(
        ratio_results,
        valuation_summary,
        scenario_results
    )

    print(summary)

    with open("outputs/analyst_summary.txt", "w") as file:
        file.write(summary)
