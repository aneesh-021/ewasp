import pandas as pd
from fetch import fetch_data


def create_features(df):
    df = df.copy()

    # Convert DATE
    df["DATE"] = pd.to_datetime(df["DATE"])

    # Sort
    df = df.sort_values(by=["PRODUCT_ID", "DATE"])

    # 📉 Revenue Change
    df["revenue_change"] = df.groupby("PRODUCT_ID")["REVENUE"].diff()

    # 📈 Cost Ratio
    df["cost_ratio"] = df["COST"] / df["REVENUE"]

    # 🚚 Delay Flag
    df["delay_flag"] = df["LEAD_TIME_DAYS"].apply(
        lambda x: 1 if pd.notna(x) and x > 2 else 0
    )

    # 📦 Inventory Risk
    df["inventory_risk"] = df["INVENTORY_LEVEL"].apply(
        lambda x: 1 if pd.notna(x) and x < 10 else 0
    )

    # 👥 Missing Customer Info
    df["missing_customer_info"] = df["CUSTOMER_SEGMENT"].isna().astype(int)

    print("✅ Features created")
    return df


if __name__ == "__main__":
    df = fetch_data()

    if df is not None:
        print("Columns:", df.columns)  # ✅ HERE (correct place)

        df = create_features(df)
        print(df.head())
    else:
        print("❌ No data available")