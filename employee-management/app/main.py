# app/main.py
from fastapi import FastAPI, HTTPException, Depends
from typing import List
from fastapi.openapi.models import APIKey, APIKeyIn, SecuritySchemeType
from fastapi.openapi.utils import get_openapi

from app.models import Employee
from app.schemas import EmployeeSchema
from app.storage import load_employees, save_employees  #Functions to read/write employees from storage (JSON file or database).
from app.decorators import log_action, api_key_auth
from app.report import run_report_thread #Function to generate and send reports periodically.
from app.email_utils import send_email

app = FastAPI(title="Employee Management Service")

# In-memory employee list
employees: List[Employee] = load_employees()

# Default email config (replace with real before use)
DEFAULT_SENDER = "microverse.platform@gmail.com"
DEFAULT_SENDER_PASSWORD = "nluc vsfo vfsp japj"
DEFAULT_MANAGER_EMAIL =  "microverse.platform@gmail.com"

# --- CRUD Endpoints ---
@app.get("/employees", response_model=List[EmployeeSchema], summary="List all employees")
def get_employees(authorized: bool = Depends(api_key_auth)):
    return employees

'''
Adds a new employee.
Logs the action using @log_action.
Sends a notification email to the manager about the new hire.
'''
@app.post("/employees", response_model=EmployeeSchema, summary="Add a new employee")
@log_action
def add_employee(emp: EmployeeSchema, authorized: bool = Depends(api_key_auth)):
   # Check for duplicate
    for e in employees:
        if e.id == emp.id:
            raise HTTPException(status_code=400, detail="Employee already exists")
    # Add employee to list & save
    new_emp = Employee(**emp.dict())
    employees.append(new_emp)
    save_employees(employees)

    # Send notification email about new hire
    subject = f"New Hire: {new_emp.name}"
    body = f"New employee hired:\n\n{new_emp.__dict__}"
    try:
        send_email(subject, body, DEFAULT_MANAGER_EMAIL, DEFAULT_SENDER, DEFAULT_SENDER_PASSWORD)
    except Exception as ex:
        print(f"Failed to send new hire email: {ex}")

    return new_emp

'''
Updates employee info by ID.
Returns 404 error if employee does not exist.
'''
@app.put("/employees/{emp_id}", response_model=EmployeeSchema, summary="Update an employee")
def update_employee(emp_id: int, emp: EmployeeSchema, authorized: bool = Depends(api_key_auth)):
    for i, e in enumerate(employees):
        if e.id == emp_id:
            employees[i] = Employee(**emp.dict())
            save_employees(employees)
            return employees[i]
    raise HTTPException(status_code=404, detail="Employee not found")

@app.delete("/employees/{emp_id}", summary="Delete an employee")
def delete_employee(emp_id: int, authorized: bool = Depends(api_key_auth)):
    global employees  # Refer to the global variable
    deleted = None
    new_list = []
    for e in employees:
        if e.id == emp_id:
            deleted = e
        else:
            new_list.append(e)
    if deleted is None:
        raise HTTPException(status_code=404, detail="Employee not found")

    employees = new_list
    save_employees(employees)

    # Send termination email
    subject = f"Employee Terminated: {deleted.name}"
    body = f"Employee terminated:\n\n{deleted.__dict__}"
    try:
        send_email(subject, body, DEFAULT_MANAGER_EMAIL, DEFAULT_SENDER, DEFAULT_SENDER_PASSWORD)
    except Exception as ex:
        print(f"Failed to send termination email: {ex}")

    return {"message": "Employee deleted"}

@app.post("/trigger-report", summary="Trigger the report (send email) manually")
def trigger_report(authorized: bool = Depends(api_key_auth)):
    run_report_thread(DEFAULT_SENDER, DEFAULT_SENDER_PASSWORD, DEFAULT_MANAGER_EMAIL)
    return {"message": "Report triggered successfully!"}

@app.get("/report", summary="Get on-demand aggregated report")
def get_report(authorized: bool = Depends(api_key_auth)):
    employees_local = load_employees()
    active_count = sum(emp.status == "Active" for emp in employees_local)
    inactive_count = sum(emp.status == "Inactive" for emp in employees_local)
    missing_name = sum(not emp.name for emp in employees_local)
    invalid_email = sum("@" not in emp.email for emp in employees_local)
    unexpected_status = sum(emp.status not in ["Active", "Inactive"] for emp in employees_local)

    departments = {}
    for emp in employees_local:
        dept = emp.department or "Unknown"
        departments.setdefault(dept, 0)
        departments[dept] += 1

    return {
        "total_employees": len(employees_local),
        "active": active_count,
        "inactive": inactive_count,
        "missing_name": missing_name,
        "invalid_email": invalid_email,
        "unexpected_status": unexpected_status,
        "departments": departments
    }

# --- Swagger Customization for API Key ---
'''
Customizes Swagger UI to require API Key.

Adds x-api-key header to all endpoints in the docs.

Users can now click Authorize in Swagger to provide the API key.
'''
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version="1.0.0",
        description="Employee Management API with API Key Auth",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "APIKeyHeader": {
            "type": "apiKey",
            "in": "header",
            "name": "x-api-key"
        }
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method["security"] = [{"APIKeyHeader": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
