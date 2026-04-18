import pandas as pd
from fetch import fetch_data
from risk_engine import create_features, generate_risks

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder


def prepare_data():
    df = fetch_data()

    df = create_features(df)
    df = generate_risks(df)

    # Features
    X = df[
        [
            "revenue_change",
            "cost_ratio",
            "delay_flag",
            "inventory_risk",
            "missing_customer_info"
        ]
    ]

    # Target (start with one risk)
    y = df["sales_risk"]

    return X, y


def train_model():
    X, y = prepare_data()

    # Encode labels
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded, test_size=0.2, random_state=42
    )

    # Model
    model = RandomForestClassifier(n_estimators=100, random_state=42)

    model.fit(X_train, y_train)

    accuracy = model.score(X_test, y_test)

    print("Model trained")
    print("Accuracy:", accuracy)

    return model, le


def predict_sample(model, le, X):
    prediction = model.predict(X)
    return le.inverse_transform(prediction)


if __name__ == "__main__":
    model, le = train_model()

    # Test prediction
    X, _ = prepare_data()
    sample = X.head(5)

    preds = predict_sample(model, le, sample)

    print("\nPredictions:")
    print(preds)