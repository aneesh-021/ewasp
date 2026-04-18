import pandas as pd
from fetch import fetch_data


def create_features(df):
    df = df.copy()

    # Convert DATE
    df["DATE"] = pd.to_datetime(df["DATE"])

    # Sort data
    df = df.sort_values(by=["PRODUCT_ID", "DATE"])

    # Revenue change
    df["revenue_change"] = df.groupby("PRODUCT_ID")["REVENUE"].diff()
    df["revenue_change"] = df["revenue_change"].fillna(0)

    # Safe cost ratio
    df["cost_ratio"] = df.apply(
        lambda row: row["COST"] / row["REVENUE"]
        if pd.notna(row["COST"]) and pd.notna(row["REVENUE"]) and row["REVENUE"] != 0
        else 0,
        axis=1
    )

    # Delay flag (using LEAD_TIME_DAYS)
    df["delay_flag"] = df["LEAD_TIME_DAYS"].apply(
        lambda x: 1 if pd.notna(x) and x > 2 else 0
    )

    # Inventory risk
    df["inventory_risk"] = df["INVENTORY_LEVEL"].apply(
        lambda x: 1 if pd.notna(x) and x < 10 else 0
    )

    # Missing customer info
    df["missing_customer_info"] = df["CUSTOMER_SEGMENT"].isna().astype(int)

    return df


def generate_risks(df):
    df = df.copy()

    # SALES RISK
    df["sales_risk"] = df["revenue_change"].apply(
        lambda x: "HIGH" if x < -200 else ("MEDIUM" if x < -50 else "LOW")
    )

    # COST RISK
    df["cost_risk"] = df["cost_ratio"].apply(
        lambda x: "HIGH" if x > 0.7 else ("MEDIUM" if x > 0.5 else "LOW")
    )

    # VENDOR RISK
    df["vendor_risk"] = df["delay_flag"].apply(
        lambda x: "HIGH" if x == 1 else "LOW"
    )

    return df


if __name__ == "__main__":
    df = fetch_data()

    if df is not None:
        df = create_features(df)
        df = generate_risks(df)

        print("Final Columns:", df.columns)

        print(df[
            [
                "DATE",
                "PRODUCT_ID",
                "revenue_change",
                "cost_ratio",
                "delay_flag",
                "sales_risk",
                "cost_risk",
                "vendor_risk"
            ]
        ].head())

    else:
        print("No data fetched")