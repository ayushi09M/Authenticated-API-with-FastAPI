# app/run_scheduler.py
from app.report import schedule_reports

'''
Imports the schedule_reports function from your reporting module.
This function is responsible for sending periodic employee reports via email.
'''


if __name__ == "__main__":
    # Provide valid email config here or edit defaults in report.py
    schedule_reports(sender_email="your_email@gmail.com", sender_password="your_app_password", to_email="manager@example.com")
