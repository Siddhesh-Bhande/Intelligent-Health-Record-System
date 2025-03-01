import os
import random
from datetime import datetime, timedelta

def fetch_wearable_data() -> dict:
    """
    Simulate fetching real-time data from wearable devices.

    Returns:
        A dictionary with sensor data.
    """
    # Simulate random variations for more realistic data
    heart_rate = random.randint(65, 85)
    systolic = random.randint(110, 140)
    diastolic = random.randint(70, 90)
    steps = random.randint(2000, 10000)
    calories = random.randint(1200, 2500)
    sleep_hours = round(random.uniform(5.0, 8.5), 1)
    
    return {
        "heart_rate": heart_rate,
        "blood_pressure": f"{systolic}/{diastolic}",
        "activity": "active" if steps > 5000 else "sedentary",
        "steps": steps,
        "calories_burned": calories,
        "sleep_hours": sleep_hours,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

def upload_health_data(file_object) -> str:
    """
    Process and save an uploaded health document.

    Args:
        file_object: The uploaded file object from Streamlit.

    Returns:
        Confirmation message.
    """
    # Create uploads directory if it doesn't exist
    os.makedirs("uploads", exist_ok=True)
    
    # Save the uploaded file
    file_path = os.path.join("uploads", file_object.name)
    with open(file_path, "wb") as f:
        f.write(file_object.getbuffer())
    
    return f"File '{file_object.name}' uploaded successfully." 