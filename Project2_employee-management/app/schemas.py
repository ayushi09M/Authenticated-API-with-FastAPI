# app/schemas.py
from pydantic import BaseModel, EmailStr, validator

# ✅ This schema ensures that incoming data is validated before saving or processing.\
# Schemas define the rules and structure of your data.
# They help validate, serialize, and document your API automatically.
class EmployeeSchema(BaseModel):
    id: int
    name: str
    email: EmailStr
    department: str
    status: str

    @validator('status')
    def status_check(cls, v):
        if v not in ["Active", "Inactive"]:
            raise ValueError("Status must be Active or Inactive")
        return v

    @validator('name')
    def name_not_empty(cls, v):
        if not v or v.isspace():
            raise ValueError("Name cannot be empty")
        return v
