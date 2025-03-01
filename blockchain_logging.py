import hashlib
import json
from datetime import datetime
import os

# Simple file to store our ledger
LEDGER_FILE = "health_ledger.json"

def initialize_ledger():
    """Create an empty ledger if it doesn't exist."""
    if not os.path.exists(LEDGER_FILE):
        with open(LEDGER_FILE, 'w') as f:
            json.dump([], f)

def get_ledger():
    """Retrieve the current ledger."""
    initialize_ledger()
    try:
        with open(LEDGER_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def save_ledger(ledger):
    """Save the updated ledger."""
    with open(LEDGER_FILE, 'w') as f:
        json.dump(ledger, f)

def log_record_update(record_id: int, changes: dict) -> dict:
    """
    Log an update to a health record using a simulated blockchain ledger.

    Args:
        record_id: Identifier of the updated record.
        changes: Dictionary containing the changes made.

    Returns:
        A ledger entry dict with the update details.
    """
    # Get the current ledger
    ledger = get_ledger()
    
    # Create a string representation of the changes, ensuring consistent order
    change_str = json.dumps(changes, sort_keys=True)
    
    # Get previous hash if the ledger is not empty
    prev_hash = "0" * 64  # Genesis block has no previous hash
    if ledger:
        prev_hash = ledger[-1]["hash"]
    
    # Generate new hash including previous hash for chain integrity
    data_to_hash = f"{prev_hash}{record_id}{change_str}{datetime.utcnow().isoformat()}"
    hash_value = hashlib.sha256(data_to_hash.encode()).hexdigest()
    
    # Create the ledger entry
    ledger_entry = {
        "record_id": record_id,
        "timestamp": datetime.utcnow().isoformat(),
        "changes": changes,
        "prev_hash": prev_hash,
        "hash": hash_value
    }
    
    # Add to ledger and save
    ledger.append(ledger_entry)
    save_ledger(ledger)
    
    return ledger_entry

def verify_ledger_integrity() -> bool:
    """
    Verify the integrity of the blockchain ledger.
    
    Returns:
        True if the ledger is valid, False otherwise.
    """
    ledger = get_ledger()
    
    if not ledger:
        return True  # Empty ledger is valid
    
    # Verify each entry
    for i in range(1, len(ledger)):
        # Check if previous hash matches
        if ledger[i]["prev_hash"] != ledger[i-1]["hash"]:
            return False
        
        # Recalculate and verify current hash
        changes_str = json.dumps(ledger[i]["changes"], sort_keys=True)
        data_to_hash = f"{ledger[i]['prev_hash']}{ledger[i]['record_id']}{changes_str}{ledger[i]['timestamp']}"
        calculated_hash = hashlib.sha256(data_to_hash.encode()).hexdigest()
        
        if calculated_hash != ledger[i]["hash"]:
            return False
    
    return True 