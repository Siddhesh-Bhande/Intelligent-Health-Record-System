import numpy as np
from sklearn.linear_model import LogisticRegression
import random
from datetime import datetime

def generate_sample_training_data():
    """
    Generate simulated training data for risk prediction.
    
    Returns:
        Dictionary with features and labels.
    """
    # Generate 100 random samples
    n_samples = 100
    
    # Features: [age, systolic_bp, diastolic_bp, heart_rate, blood_sugar]
    features = []
    labels = []  # 1 for high risk, 0 for low risk
    
    for _ in range(n_samples):
        age = random.randint(25, 75)
        systolic = random.randint(100, 180)
        diastolic = random.randint(60, 110)
        heart_rate = random.randint(60, 100)
        blood_sugar = random.randint(70, 200)
        
        # Simulate risk based on these values (simple rule-based approach)
        # In reality, this would be based on medical knowledge
        risk = 1 if (systolic > 140 or diastolic > 90 or blood_sugar > 180) else 0
        
        features.append([age, systolic, diastolic, heart_rate, blood_sugar])
        labels.append(risk)
    
    return {"features": features, "labels": labels}

def train_risk_model(training_data=None) -> LogisticRegression:
    """
    Train a machine learning model to predict health risks.

    Args:
        training_data: Structured dataset with historical health data.

    Returns:
        A trained ML model.
    """
    if training_data is None:
        training_data = generate_sample_training_data()
    
    X = np.array(training_data["features"])
    y = np.array(training_data["labels"])
    
    model = LogisticRegression(random_state=42)
    model.fit(X, y)
    
    return model

def predict_risk(model, user_data: list) -> dict:
    """
    Predict health risk using the trained model.

    Args:
        model: Trained ML model.
        user_data: List of current health metric values.

    Returns:
        Risk prediction details.
    """
    risk_probability = model.predict_proba([user_data])[0][1]
    risk_level = "High" if risk_probability > 0.5 else "Low"
    
    return {
        "probability": round(risk_probability * 100, 2),
        "risk_level": risk_level,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

def send_alert(alert_message: str, risk_level: str) -> str:
    """
    Simulate sending an alert regarding potential health risks.

    Args:
        alert_message: Alert message text.
        risk_level: Level of risk (high, medium, low).

    Returns:
        A confirmation message.
    """
    # In a real application, this would integrate with an email/SMS service
    return f"Alert ({risk_level} risk) sent: {alert_message}" 