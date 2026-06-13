import pandas as pd


def load_market_assumptions(file_path):
    assumptions = pd.read_csv(file_path)
    return dict(zip(assumptions["input"], assumptions["value"]))


def calculate_cost_of_equity(risk_free_rate, beta, market_risk_premium):
    return risk_free_rate + beta * market_risk_premium


def calculate_wacc(cost_of_equity, cost_of_debt, tax_rate, debt_weight):
    equity_weight = 1 - debt_weight

    after_tax_cost_of_debt = cost_of_debt * (1 - tax_rate)

    wacc = (
        equity_weight * cost_of_equity
        + debt_weight * after_tax_cost_of_debt
    )

    return wacc, after_tax_cost_of_debt, equity_weight


if __name__ == "__main__":
    assumptions = load_market_assumptions("data/market_assumptions.csv")

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

    print("WACC Calculation")
    print("----------------")
    print(f"Cost of equity: {cost_of_equity:.2%}")
    print(f"Pre-tax cost of debt: {cost_of_debt:.2%}")
    print(f"After-tax cost of debt: {after_tax_cost_of_debt:.2%}")
    print(f"Debt weight: {debt_weight:.2%}")
    print(f"Equity weight: {equity_weight:.2%}")
    print(f"WACC: {wacc:.2%}")
