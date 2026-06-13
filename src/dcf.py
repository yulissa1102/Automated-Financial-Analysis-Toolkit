import pandas as pd


def load_market_assumptions(file_path):
    assumptions = pd.read_csv(file_path)
    return dict(zip(assumptions["input"], assumptions["value"]))


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


def calculate_dcf_valuation(base_fcf, growth_rate, discount_rate, terminal_growth_rate):
    projected_fcfs = project_free_cash_flows(base_fcf, growth_rate)
    discounted_fcfs = discount_cash_flows(projected_fcfs, discount_rate)

    terminal_value = calculate_terminal_value(
        projected_fcfs[-1],
        discount_rate,
        terminal_growth_rate
    )

    discounted_terminal_value = terminal_value / ((1 + discount_rate) ** 5)

    enterprise_value = sum(discounted_fcfs) + discounted_terminal_value

    return projected_fcfs, discounted_fcfs, terminal_value, discounted_terminal_value, enterprise_value


if __name__ == "__main__":
    assumptions = load_market_assumptions("data/market_assumptions.csv")

    base_fcf = float(assumptions["base_free_cash_flow"])
    growth_rate = float(assumptions["fcf_growth_rate"])
    terminal_growth_rate = float(assumptions["terminal_growth_rate"])

    # Use the WACC calculated in Day 4 as a simplified discount rate.
    discount_rate = 0.0826

    projected_fcfs, discounted_fcfs, terminal_value, discounted_terminal_value, enterprise_value = calculate_dcf_valuation(
        base_fcf,
        growth_rate,
        discount_rate,
        terminal_growth_rate
    )

    print("DCF Valuation")
    print("-------------")

    for year, (fcf, discounted_fcf) in enumerate(zip(projected_fcfs, discounted_fcfs), start=1):
        print(f"Year {year}: Projected FCF = {fcf:,.0f}, Discounted FCF = {discounted_fcf:,.0f}")

    print(f"Terminal value: {terminal_value:,.0f}")
    print(f"Discounted terminal value: {discounted_terminal_value:,.0f}")
    print(f"Enterprise value: {enterprise_value:,.0f}")
