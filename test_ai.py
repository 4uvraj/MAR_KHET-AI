from app.predict import predict_price
from app.ai_explainer import get_ai_explanation


price = predict_price(
    year=2024,
    month=6,
    state="Madhya Pradesh",
    commodity="Wheat"
)

explanation = get_ai_explanation(
    predicted_price=price,
    commodity="Wheat",
    state="Madhya Pradesh",
    month=6,
    year=2024
)

print("Prediction:", price)
print("\nAI Explanation:")
print(explanation)
