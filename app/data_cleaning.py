import pandas as pd

def clean_mandi_data(df):

    df = df.copy()

    # ---------------- DATE FIX ----------------
    df["Arrival_Date"] = pd.to_datetime(
        df["Arrival_Date"],
        dayfirst=True,
        errors="coerce"
    )

    # ---------------- PRICE FIX (VERY IMPORTANT) ----------------
    price_cols = ["Min_Price", "Max_Price", "Modal_Price"]

    for col in price_cols:

        # Remove commas if any
        df[col] = df[col].astype(str).str.replace(",", "")

        # Convert to numeric safely
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # ---------------- DROP BAD ROWS ----------------
    df = df.dropna(subset=["Modal_Price"])

    # ---------------- DATE FEATURES ----------------
    df["Year"] = df["Arrival_Date"].dt.year
    df["Month"] = df["Arrival_Date"].dt.month
    df["Day"] = df["Arrival_Date"].dt.day

    return df
