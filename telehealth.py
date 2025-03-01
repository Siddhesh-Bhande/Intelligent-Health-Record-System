from datetime import datetime
import json
import os

# File to store appointments
APPOINTMENTS_FILE = "telehealth_appointments.json"

def initialize_appointments():
    """Create an empty appointments file if it doesn't exist."""
    if not os.path.exists(APPOINTMENTS_FILE):
        with open(APPOINTMENTS_FILE, 'w') as f:
            json.dump([], f)

def get_appointments():
    """Retrieve all appointments."""
    initialize_appointments()
    try:
        with open(APPOINTMENTS_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def save_appointments(appointments):
    """Save the updated appointments list."""
    with open(APPOINTMENTS_FILE, 'w') as f:
        json.dump(appointments, f)

def schedule_telehealth_consultation(patient_name: str, doctor_name: str, consultation_time: datetime) -> dict:
    """
    Schedule a telehealth consultation.

    Args:
        patient_name: Name of the patient.
        doctor_name: Name of the doctor.
        consultation_time: DateTime of the consultation.

    Returns:
        A dict representing the scheduled appointment.
    """
    appointments = get_appointments()
    
    # Generate a new appointment ID
    appointment_id = 1
    if appointments:
        appointment_id = max(appt.get("appointment_id", 0) for appt in appointments) + 1
    
    # Create appointment
    appointment = {
        "appointment_id": appointment_id,
        "patient": patient_name,
        "doctor": doctor_name,
        "consultation_time": consultation_time.isoformat(),
        "status": "Scheduled",
        "created_at": datetime.utcnow().isoformat()
    }
    
    # Add to list and save
    appointments.append(appointment)
    save_appointments(appointments)
    
    return appointment

def get_upcoming_consultations() -> list:
    """
    Retrieve upcoming telehealth consultations.

    Returns:
        A list of upcoming appointments.
    """
    appointments = get_appointments()
    
    # Filter for upcoming appointments
    now = datetime.utcnow().isoformat()
    upcoming = [appt for appt in appointments if appt["consultation_time"] > now]
    
    # Sort by consultation time
    upcoming.sort(key=lambda x: x["consultation_time"])
    
    return upcoming

def cancel_consultation(appointment_id: int) -> str:
    """
    Cancel a scheduled consultation.

    Args:
        appointment_id: The ID of the appointment to cancel.

    Returns:
        A message indicating success or failure.
    """
    appointments = get_appointments()
    
    for appt in appointments:
        if appt.get("appointment_id") == appointment_id:
            appt["status"] = "Cancelled"
            appt["updated_at"] = datetime.utcnow().isoformat()
            save_appointments(appointments)
            return f"Appointment {appointment_id} cancelled successfully."
    
    return "Appointment not found." 