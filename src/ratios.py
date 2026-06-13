import pandas as pd
def interpret_roa(roa):
    if pd.isna(roa):
        return "N/A"
    if roa >= 0.10:
        return "Strong"
    if roa >= 0.05:
        return "Moderate"
    return "Weak"


def interpret_roe(roe):
    if pd.isna(roe):
        return "N/A"
    if roe >= 0.15:
        return "Strong"
    if roe >= 0.08:
        return "Moderate"
    return "Weak"


def interpret_debt_ratio(debt_ratio):
    if pd.isna(debt_ratio):
        return "N/A"
    if debt_ratio <= 0.30:
        return "Conservative leverage"
    if debt_ratio <= 0.60:
        return "Moderate leverage"
    return "High leverage"


def interpret_interest_coverage(interest_coverage):
    if interest_coverage == "N/A":
        return "No meaningful interest expense"
    if interest_coverage >= 5:
        return "Strong interest coverage"
    if interest_coverage >= 2:
        return "Moderate interest coverage"
    return "Weak interest coverage"

def calculate_ratios(financials):
    financials = financials.sort_values("year").reset_index(drop=True)

    financials["average_assets"] = financials["total_assets"].rolling(2).mean()
    financials["average_equity"] = financials["total_equity"].rolling(2).mean()

    financials["roa"] = financials["net_income"] / financials["average_assets"]
    financials["roe"] = financials["net_income"] / financials["average_equity"]
    financials["debt_ratio"] = financials["total_liabilities"] / financials["total_assets"]

    financials["interest_coverage"] = financials.apply(
        lambda row: "N/A" if row["interest_expense"] == 0 else row["operating_income"] / row["interest_expense"],
        axis=1
    )

    financials["roa_pct"] = financials["roa"].apply(
        lambda value: "N/A" if pd.isna(value) else f"{value:.2%}"
    )
    financials["roe_pct"] = financials["roe"].apply(
        lambda value: "N/A" if pd.isna(value) else f"{value:.2%}"
    )
    financials["debt_ratio_pct"] = financials["debt_ratio"].apply(
        lambda value: "N/A" if pd.isna(value) else f"{value:.2%}"
    )

    financials["roa_interpretation"] = financials["roa"].apply(interpret_roa)
    financials["roe_interpretation"] = financials["roe"].apply(interpret_roe)
    financials["leverage_interpretation"] = financials["debt_ratio"].apply(interpret_debt_ratio)
    financials["interest_coverage_interpretation"] = financials["interest_coverage"].apply(
        interpret_interest_coverage
    )

    return financials[
        [
            "year",
            "roa_pct",
            "roa_interpretation",
            "roe_pct",
            "roe_interpretation",
            "debt_ratio_pct",
            "leverage_interpretation",
            "interest_coverage",
            "interest_coverage_interpretation"
        ]
    ]

if __name__ == "__main__":
    financials = pd.read_csv("data/garmin_financials_template.csv")
    ratios = calculate_ratios(financials)
    print(ratios.to_string(index=False))