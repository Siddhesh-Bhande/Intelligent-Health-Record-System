def generate_health_recommendations(health_data: dict) -> list:
    """
    Generate personalized health recommendations based on health data.

    Args:
        health_data: Dictionary containing aggregated health metrics.

    Returns:
        A list of recommendation strings.
    """
    recommendations = []
    
    # Extract blood pressure values (assuming format like "120/80")
    bp_str = health_data.get("blood_pressure", "")
    try:
        if "/" in bp_str:
            systolic, diastolic = map(int, bp_str.split("/"))
        else:
            systolic = health_data.get("blood_pressure_systolic", 0)
            diastolic = health_data.get("blood_pressure_diastolic", 0)
    except (ValueError, TypeError):
        systolic, diastolic = 0, 0
    
    # Get other health metrics
    sugar = health_data.get("blood_sugar", 0)
    heart_rate = health_data.get("heart_rate", 0)
    steps = health_data.get("steps", 0)
    sleep_hours = health_data.get("sleep_hours", 0)

    # Blood pressure recommendations
    if systolic > 140 or diastolic > 90:
        recommendations.append("Your blood pressure appears high. Consider reducing salt intake, increasing physical activity, and scheduling a checkup with your doctor.")
    elif systolic > 120 or diastolic > 80:
        recommendations.append("Your blood pressure is slightly elevated. Monitor it regularly and consider lifestyle changes like reducing sodium intake.")
    
    # Blood sugar recommendations
    if isinstance(sugar, (int, float)):
        if sugar > 200:
            recommendations.append("Your blood sugar is elevated. Monitor your sugar intake and consult your doctor about diabetes management.")
        elif sugar > 140:
            recommendations.append("Your blood sugar is higher than optimal. Consider reducing intake of refined carbohydrates and sugary foods.")
    
    # Heart rate recommendations
    if isinstance(heart_rate, (int, float)):
        if heart_rate > 100:
            recommendations.append("Your resting heart rate appears elevated. Consider stress reduction techniques and consult your doctor if it remains high.")
        elif heart_rate < 60:
            recommendations.append("Your heart rate is lower than average. If you're not an athlete, consider discussing this with your doctor.")
    
    # Activity recommendations
    if isinstance(steps, (int, float)):
        if steps < 5000:
            recommendations.append("You're not getting enough daily steps. Aim for at least 7,500 steps daily for better health.")
        elif steps > 10000:
            recommendations.append("Great job on your activity level! Keep up the good work with your daily steps.")
    
    # Sleep recommendations
    if isinstance(sleep_hours, (int, float)):
        if sleep_hours < 6:
            recommendations.append("You're not getting enough sleep. Adults should aim for 7-9 hours of quality sleep per night.")
        elif sleep_hours > 9:
            recommendations.append("You're sleeping more than average. While this might be normal for you, excessive sleep can sometimes indicate health issues.")
    
    # Add general recommendations if specific ones are lacking
    if not recommendations:
        recommendations.append("Maintain a balanced diet rich in fruits, vegetables, whole grains, and lean proteins.")
        recommendations.append("Aim for at least 150 minutes of moderate exercise per week.")
        recommendations.append("Stay hydrated by drinking plenty of water throughout the day.")
    
    return recommendations 