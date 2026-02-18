from app.data_pipeline import get_dataframe
from app.data_cleaning import clean_mandi_data
from app.feature_engineering import create_time_features
from app.ml_model import train_price_model, save_model


df = get_dataframe(limit=1000)

df = clean_mandi_data(df)

df = create_time_features(df)

print("Training Model...")

model, features = train_price_model(df)

save_model(model, features)
