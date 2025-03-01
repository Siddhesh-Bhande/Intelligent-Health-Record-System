import json
import os
from datetime import datetime

# Using a simple in-memory list to store records
health_records = []

# Path for a simple file-based storage
RECORDS_FILE = "health_records.json"

def load_records():
    """Load records from file if it exists."""
    global health_records
    if os.path.exists(RECORDS_FILE):
        try:
            with open(RECORDS_FILE, 'r') as f:
                health_records = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            health_records = []

def save_records():
    """Save records to a file."""
    with open(RECORDS_FILE, 'w') as f:
        json.dump(health_records, f)

def add_health_record(record_data: dict) -> str:
    """
    Add a new health record.

    Args:
        record_data: Dictionary with health data (e.g., vitals, notes).

    Returns:
        Success message.
    """
    load_records()
    
    # Add timestamp and record ID
    record_id = len(health_records) + 1
    record_data["record_id"] = record_id
    record_data["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    health_records.append(record_data)
    save_records()
    
    return f"Health record {record_id} added successfully."

def update_health_record(record_id: int, new_data: dict) -> str:
    """
    Update an existing health record.

    Args:
        record_id: Record identifier.
        new_data: Dictionary with updated record fields.

    Returns:
        Confirmation message.
    """
    load_records()
    
    for record in health_records:
        if record.get("record_id") == record_id:
            record.update(new_data)
            record["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            save_records()
            return f"Health record {record_id} updated successfully."
    
    return "Record not found."

def get_health_record(record_id: int) -> dict:
    """
    Retrieve a single health record.

    Args:
        record_id: Record identifier.

    Returns:
        A dictionary containing record details.
    """
    load_records()
    
    for record in health_records:
        if record.get("record_id") == record_id:
            return record
    
    return {"error": "Record not found."}

def get_all_records() -> list:
    """
    Retrieve all health records.

    Returns:
        A list of all records.
    """
    load_records()
    return health_records

def delete_health_record(record_id: int) -> str:
    """
    Delete a health record.

    Args:
        record_id: Record identifier.

    Returns:
        Confirmation message.
    """
    load_records()
    
    for i, record in enumerate(health_records):
        if record.get("record_id") == record_id:
            del health_records[i]
            save_records()
            return f"Health record {record_id} deleted successfully."
    
    return "Record not found." 