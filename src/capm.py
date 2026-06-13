import pandas as pd


def load_market_assumptions(file_path):
    assumptions = pd.read_csv(file_path)
    return dict(zip(assumptions["input"], assumptions["value"]))


def calculate_cost_of_equity(risk_free_rate, beta, market_risk_premium):
    cost_of_equity = risk_free_rate + beta * market_risk_premium
    return cost_of_equity


if __name__ == "__main__":
    assumptions = load_market_assumptions("data/market_assumptions.csv")

    risk_free_rate = float(assumptions["risk_free_rate"])
    beta = float(assumptions["beta"])
    market_risk_premium = float(assumptions["market_risk_premium"])

    cost_of_equity = calculate_cost_of_equity(
        risk_free_rate,
        beta,
        market_risk_premium
    )

    print("CAPM Cost of Equity Calculation")
    print("--------------------------------")
    print(f"Risk-free rate: {risk_free_rate:.2%}")
    print(f"Beta: {beta:.2f}")
    print(f"Market risk premium: {market_risk_premium:.2%}")
    print(f"Cost of equity: {cost_of_equity:.2%}")