import random
from datetime import datetime, timedelta
import os
import json
import pandas as pd
import numpy as np

# Demo user info
DEMO_USER = {
    "name": "Siddhesh Bhande",
    "age": 42,
    "gender": "Non-binary",
    "height": 175,  # cm
    "weight": 70.5,  # kg
    "email": "siddhesh.test@example.com"
}

def create_sample_health_records():
    """Generate sample health records for the demo user"""
    records = []
    
    # Generate records for the past 30 days
    end_date = datetime.now()
    for i in range(30, 0, -1):
        date = end_date - timedelta(days=i)
        
        # Generate some realistic variations in the data
        systolic = random.randint(115, 145)
        diastolic = random.randint(75, 95)
        heart_rate = random.randint(65, 85)
        blood_sugar = random.randint(90, 130) if i % 3 != 0 else random.randint(130, 180)
        weight = round(70.5 + random.uniform(-0.8, 0.5), 1)
        temperature = round(36.5 + random.uniform(-0.3, 0.7), 1)
        
        # Create more varied notes
        notes = ""
        if i == 25:
            notes = "Feeling tired today. Might be due to poor sleep last night."
        elif i == 20:
            notes = "Had a mild headache in the morning. Took ibuprofen."
        elif i == 15:
            notes = "Blood pressure seems a bit elevated. Will monitor."
        elif i == 10:
            notes = "Doctor visit today. Doctor suggested reducing salt intake and more exercise."
        elif i == 5:
            notes = "Started new exercise routine. Feeling good overall."
        
        record = {
            "record_id": 30 - i + 1,
            "date": date.strftime("%Y-%m-%d"),
            "blood_pressure": f"{systolic}/{diastolic}",
            "blood_pressure_systolic": systolic,
            "blood_pressure_diastolic": diastolic,
            "heart_rate": heart_rate,
            "blood_sugar": blood_sugar,
            "weight": weight,
            "temperature": temperature,
            "notes": notes,
            "timestamp": date.strftime("%Y-%m-%d %H:%M:%S")
        }
        records.append(record)
    
    return records

def create_sample_appointments():
    """Generate sample telehealth appointments"""
    now = datetime.now()
    
    # Create a mix of past, upcoming, and cancelled appointments
    appointments = [
        {
            "appointment_id": 1,
            "patient": DEMO_USER["name"],
            "doctor": "Dr. Smith (Cardiology)",
            "consultation_time": (now - timedelta(days=15)).isoformat(),
            "status": "Completed",
            "notes": "Reviewed blood pressure readings. Continue current medication.",
            "created_at": (now - timedelta(days=30)).isoformat()
        },
        {
            "appointment_id": 2,
            "patient": DEMO_USER["name"],
            "doctor": "Dr. Johnson (Internal Medicine)",
            "consultation_time": (now - timedelta(days=5)).isoformat(),
            "status": "Completed",
            "notes": "General checkup. Everything looks good.",
            "created_at": (now - timedelta(days=15)).isoformat()
        },
        {
            "appointment_id": 3,
            "patient": DEMO_USER["name"],
            "doctor": "Dr. Williams (Endocrinology)",
            "consultation_time": (now + timedelta(days=3)).isoformat(),
            "status": "Scheduled",
            "reason": "Discuss recent blood sugar fluctuations",
            "created_at": (now - timedelta(days=2)).isoformat()
        },
        {
            "appointment_id": 4,
            "patient": DEMO_USER["name"],
            "doctor": "Dr. Davis (Neurology)",
            "consultation_time": (now + timedelta(days=10)).isoformat(),
            "status": "Scheduled",
            "reason": "Follow-up on headaches",
            "created_at": (now - timedelta(days=1)).isoformat()
        },
        {
            "appointment_id": 5,
            "patient": DEMO_USER["name"],
            "doctor": "Dr. Smith (Cardiology)",
            "consultation_time": (now + timedelta(days=7)).isoformat(),
            "status": "Cancelled",
            "reason": "Quarterly blood pressure review",
            "created_at": (now - timedelta(days=10)).isoformat(),
            "updated_at": (now - timedelta(days=2)).isoformat()
        }
    ]
    
    return appointments

def create_sample_wearable_data_history():
    """Create a 7-day history of wearable data for visualizations"""
    end_date = datetime.now()
    dates = [(end_date - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7, 0, -1)]
    
    # Create realistic patterns - gradually improving health metrics
    systolic = [random.randint(125, 145) for _ in range(4)] + [random.randint(118, 130) for _ in range(3)]
    diastolic = [random.randint(82, 94) for _ in range(4)] + [random.randint(75, 85) for _ in range(3)]
    heart_rate = [random.randint(72, 86) for _ in range(4)] + [random.randint(68, 76) for _ in range(3)]
    blood_sugar = [random.randint(130, 160) for _ in range(3)] + [random.randint(100, 125) for _ in range(4)]
    steps = [random.randint(4000, 6000) for _ in range(3)] + [random.randint(7500, 12000) for _ in range(4)]
    sleep_hours = [random.uniform(5.5, 6.5) for _ in range(3)] + [random.uniform(7.0, 8.5) for _ in range(4)]
    calories_burned = [steps[i] * 0.05 for i in range(7)]
    
    return {
        "dates": dates,
        "blood_pressure_systolic": systolic,
        "blood_pressure_diastolic": diastolic,
        "heart_rate": heart_rate,
        "blood_sugar": blood_sugar,
        "steps": steps,
        "sleep_hours": [round(h, 1) for h in sleep_hours],
        "calories_burned": [round(c) for c in calories_burned]
    }

def initialize_demo_data():
    """Initialize all demo data files if they don't exist"""
    # Create directories if they don't exist
    os.makedirs("uploads", exist_ok=True)
    
    # Create health records
    if not os.path.exists("health_records.json"):
        records = create_sample_health_records()
        with open("health_records.json", "w") as f:
            json.dump(records, f)
    
    # Create telehealth appointments
    if not os.path.exists("telehealth_appointments.json"):
        appointments = create_sample_appointments()
        with open("telehealth_appointments.json", "w") as f:
            json.dump(appointments, f)
    
    # Create sample documents in uploads folder
    sample_docs = [
        "blood_test_results.csv",
        "cholesterol_screening.pdf",
        "doctor_visit_summary.pdf"
    ]
    
    for doc in sample_docs:
        doc_path = os.path.join("uploads", doc)
        if not os.path.exists(doc_path):
            # Just create empty files as placeholders
            with open(doc_path, "w") as f:
                f.write(f"Sample {doc} file - placeholder")
    
    # Create sample CSV templates in uploads folder
    create_sample_templates()

def create_sample_templates():
    """Create downloadable template files"""
    # Blood test results template
    blood_test_template = pd.DataFrame({
        'Date': ['YYYY-MM-DD'],
        'Test': ['Complete Blood Count'],
        'Result': ['Value'],
        'Unit': ['Unit'],
        'Reference Range': ['Min-Max'],
        'Notes': ['Additional notes']
    })
    
    # Health tracking template
    health_tracking_template = pd.DataFrame({
        'Date': ['YYYY-MM-DD'],
        'Systolic BP': [120],
        'Diastolic BP': [80],
        'Heart Rate': [72],
        'Blood Sugar': [100],
        'Weight (kg)': [70.0],
        'Temperature (°C)': [36.6],
        'Steps': [10000],
        'Sleep Hours': [8],
        'Notes': ['How you felt today']
    })
    
    # Save templates
    os.makedirs("templates", exist_ok=True)
    blood_test_template.to_csv("templates/blood_test_template.csv", index=False)
    health_tracking_template.to_csv("templates/health_tracking_template.csv", index=False)

def get_demo_user():
    """Return the demo user information"""
    return DEMO_USER

def get_latest_wearable_data():
    """Get the most recent simulated wearable data"""
    history = create_sample_wearable_data_history()
    
    # Return the last day's data
    return {
        "heart_rate": history["heart_rate"][-1],
        "blood_pressure": f"{history['blood_pressure_systolic'][-1]}/{history['blood_pressure_diastolic'][-1]}",
        "blood_pressure_systolic": history["blood_pressure_systolic"][-1],
        "blood_pressure_diastolic": history["blood_pressure_diastolic"][-1],
        "steps": history["steps"][-1],
        "calories_burned": history["calories_burned"][-1],
        "sleep_hours": history["sleep_hours"][-1],
        "activity": "active" if history["steps"][-1] > 7500 else "sedentary",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    } 