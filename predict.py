import joblib
import pandas as pd
from feature_engineering import create_features

# Load model
model = joblib.load("model.pkl")
le = joblib.load("label_encoder.pkl")


def predict_risk(df):
    df = create_features(df)

    X = df[
        [
            "revenue_change",
            "cost_ratio",
            "delay_flag",
            "inventory_risk",
            "missing_customer_info"
        ]
    ]

    preds = model.predict(X)
    decoded = le.inverse_transform(preds)

    df["predicted_sales_risk"] = decoded

    return df



import joblib
import pandas as pd
from feature_engineering import create_features

# Load model
model = joblib.load("model.pkl")
le = joblib.load("label_encoder.pkl")


def predict_risk(df):
    df = create_features(df)

    X = df[
        [
            "revenue_change",
            "cost_ratio",
            "delay_flag",
            "inventory_risk",
            "missing_customer_info"
        ]
    ]

    preds = model.predict(X)
    decoded = le.inverse_transform(preds)

    df["predicted_sales_risk"] = decoded

    return df


if __name__ == "__main__":
    from fetch import fetch_data

    df = fetch_data()

    if df is not None:
        result = predict_risk(df)
        print(result[["PRODUCT_ID", "predicted_sales_risk"]].head())
    else:
        print("No data fetched")