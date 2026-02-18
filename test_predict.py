from app.predict import predict_price


price = predict_price(
    year=2024,
    month=6,
    state="Madhya Pradesh",
    commodity="Wheat"
)

print("Predicted Price:", price)
