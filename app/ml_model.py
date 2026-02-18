import pandas as pd
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split


def train_price_model(df):

    df = df.copy()

    features = [
        "Year",
        "Month",
        "State",
        "Commodity"
    ]

    target = "Modal_Price"

    df_model = df[features + [target]].copy()

    df_model = pd.get_dummies(df_model)

    X = df_model.drop(target, axis=1)
    y = df_model[target]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestRegressor(
        n_estimators=200,
        random_state=42
    )

    model.fit(X_train, y_train)

    score = model.score(X_test, y_test)

    print("Model R² Score:", score)

    return model, X.columns


def save_model(model, feature_columns):

    joblib.dump(model, "models/price_model.pkl")
    joblib.dump(feature_columns, "models/feature_columns.pkl")

    print("Model Saved!")


# ✅ ADD THIS
def load_model():

    model = joblib.load("models/price_model.pkl")
    features = joblib.load("models/feature_columns.pkl")

    return model, features
