import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
import io
import base64

def generate_health_trends() -> dict:
    """
    Analyze (simulated) health records to compute trends.

    Returns:
        Time-series data for various health metrics.
    """
    # Generate dates for the past 7 days
    end_date = datetime.now()
    dates = [(end_date - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7, 0, -1)]
    
    # Generate random health metrics
    blood_pressure_systolic = [np.random.randint(110, 140) for _ in range(7)]
    blood_pressure_diastolic = [np.random.randint(70, 90) for _ in range(7)]
    heart_rate = [np.random.randint(65, 85) for _ in range(7)]
    blood_sugar = [np.random.randint(90, 180) for _ in range(7)]
    steps = [np.random.randint(3000, 12000) for _ in range(7)]
    
    return {
        "dates": dates,
        "blood_pressure_systolic": blood_pressure_systolic,
        "blood_pressure_diastolic": blood_pressure_diastolic,
        "heart_rate": heart_rate,
        "blood_sugar": blood_sugar,
        "steps": steps
    }

def plot_metric(dates: list, values: list, title: str, ylabel: str = "Value"):
    """
    Plot a health metric using matplotlib.

    Args:
        dates: List of dates.
        values: List of corresponding metric values.
        title: Title of the plot.
        ylabel: Label for the y-axis.
    """
    plt.figure(figsize=(10, 6))
    plt.plot(dates, values, marker='o', linestyle='-', linewidth=2)
    plt.title(title, fontsize=16)
    plt.xlabel("Date", fontsize=12)
    plt.ylabel(ylabel, fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()

def get_plot_as_base64():
    """Convert the current matplotlib plot to a base64 encoded string."""
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    img_str = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()
    return img_str 