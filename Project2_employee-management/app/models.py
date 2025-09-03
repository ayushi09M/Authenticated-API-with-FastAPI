from abc import ABC, abstractmethod

class Person(ABC):
    """Base class for all people in organization"""
    def __init__(self, id: int, name: str, email: str):
        self.id = id
        self.name = name
        self.email = email

    @abstractmethod
    def role(self):
        pass

class Employee(Person):
    def __init__(self, id: int, name: str, email: str, department: str, status: str):
        super().__init__(id, name, email)
        self.department = department
        self.status = status

    def role(self):
        return "Employee"

class Manager(Employee):
    def role(self):
        return "Manager"

class Department:
    def __init__(self, name: str):
        self.name = name
