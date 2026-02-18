import joblib
import pandas as pd


def load_model():

    model = joblib.load("models/price_model.pkl")
    feature_columns = joblib.load("models/feature_columns.pkl")

    return model, feature_columns


def predict_price(model, feature_columns, commodity, state, year, month):


    model, feature_columns = load_model()

    # Create input dataframe
    input_data = pd.DataFrame([{
        "Year": year,
        "Month": month,
        "State": state,
        "Commodity": commodity
    }])

    # Convert categorical → dummy columns
    input_data = pd.get_dummies(input_data)

    # Align columns with training columns
    input_data = input_data.reindex(columns=feature_columns, fill_value=0)

    prediction = model.predict(input_data)[0]

    return prediction
