# app/storage.py
import json
import os
from typing import List
from app.models import Employee

FILE_PATH = "data/employees.json"

def load_employees() -> List[Employee]:
    """
    Load employees from JSON. If file doesn't exist, create an empty JSON list.
    Returns list of Employee instances.
    """
    # Ensure directory exists
    dirpath = os.path.dirname(FILE_PATH)
    if dirpath and not os.path.exists(dirpath):
        os.makedirs(dirpath, exist_ok=True)

    # If file missing, create with empty list
    if not os.path.exists(FILE_PATH):
        with open(FILE_PATH, "w", encoding="utf-8") as f:
            json.dump([], f)

    # Read file
    with open(FILE_PATH, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
            if not isinstance(data, list):
                data = []
        except json.JSONDecodeError:
            data = []

    # Convert to Employee objects (tolerant to missing fields)
    employees = []
    for emp in data:
        # Provide defaults to avoid crashes if file contains partial data
        try:
            e = Employee(
                id=emp.get("id"),
                name=emp.get("name", ""),
                email=emp.get("email", ""),
                department=emp.get("department", ""),
                status=emp.get("status", "")
            )
            employees.append(e)
        except Exception:
            continue
    return employees

def save_employees(employees: List[Employee]):
    """
    Save list of Employee instances to JSON file.
    """
    with open(FILE_PATH, "w", encoding="utf-8") as f:
        json.dump([emp.__dict__ for emp in employees], f, indent=4)
