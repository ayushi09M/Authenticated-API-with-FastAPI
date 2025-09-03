
import threading
import time
import schedule
from app.storage import load_employees
from app.email_utils import send_email

def generate_report(sender_email="microverse.platform@gmail.com", sender_password="nluc vsfo vfsp japj", to_email="microverse.platform@gmail.com"):
    """
    Generates a report of employee statuses and sends via email.
    """
    employees = load_employees()
    active_count = sum(emp.status == "Active" for emp in employees)
    inactive_count = sum(emp.status == "Inactive" for emp in employees)
    missing_name = sum(not emp.name for emp in employees)
    invalid_email = sum("@" not in emp.email for emp in employees)
    unexpected_status = sum(emp.status not in ["Active", "Inactive"] for emp in employees)

    body = f"""
Employee Report:
Total: {len(employees)}
Active: {active_count}
Inactive: {inactive_count}
Missing Names: {missing_name}
Invalid Emails: {invalid_email}
Unexpected Status: {unexpected_status}
"""
    print("Sending report email...")  # For debugging
    send_email("Employee Report", body, to_email, sender_email, sender_password)

def run_report_thread(sender_email="microverse.platformgmail.com", sender_password="nluc vsfo vfsp japj", to_email="microverse.platformgmail.com"):
    """
    Runs the generate_report function in a separate thread to support concurrency.
    """
    thread = threading.Thread(target=generate_report, args=(sender_email, sender_password, to_email))
    thread.start()

def schedule_reports(sender_email="microverse.platformgmail.com", sender_password="nluc vsfo vfsp japj", to_email="microverse.platformgmail.com"):
    """
    Schedule report every 2 minutes (for testing).
    """
    schedule.every(2).minute.do(run_report_thread, sender_email, sender_password, to_email)
    print("Report scheduler started. Sending reports every 2 minutes...")
    while True:
        schedule.run_pending()
        time.sleep(1)
