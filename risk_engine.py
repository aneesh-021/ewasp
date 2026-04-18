import pandas as pd
from fetch import fetch_data
from feature_engineering import create_features


def generate_risks(df):
    df = df.copy()

    # --- SALES RISK ---
    def sales_risk_logic(x):
        if pd.isna(x):
            return "LOW"
        elif x < -200:
            return "HIGH"
        elif x < -50:
            return "MEDIUM"
        else:
            return "LOW"

    df["sales_risk"] = df["revenue_change"].apply(sales_risk_logic)

    # --- COST RISK ---
    def cost_risk_logic(x):
        if pd.isna(x):
            return "LOW"
        elif x > 0.7:
            return "HIGH"
        elif x > 0.5:
            return "MEDIUM"
        else:
            return "LOW"

    df["cost_ratio"] = df.apply(
    lambda row: row["COST"] / row["REVENUE"]
    if pd.notna(row["COST"]) and pd.notna(row["REVENUE"]) and row["REVENUE"] != 0
    else 0,
    axis=1
)

    # --- VENDOR RISK ---
    def vendor_risk_logic(x):
        if x == 1:
            return "HIGH"
        else:
            return "LOW"

    df["vendor_risk"] = df["delay_flag"].apply(vendor_risk_logic)

    print("Risk generation complete")
    return df


if __name__ == "__main__":
    df = fetch_data()

    if df is not None:
        df = create_features(df)
        df = generate_risks(df)

        print(df[[
            "DATE", "PRODUCT_ID",
            "revenue_change", "cost_ratio", "delay_flag",
            "sales_risk", "cost_risk", "vendor_risk"
        ]].head())

    else:
        print("No data available")