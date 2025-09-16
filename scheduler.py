# scheduler.py
import schedule
import time
from task_email import send_task_email

SENDER = "youremail@gmail.com"
RECEIVER = "receiver@gmail.com"
APP_PASSWORD = "your_app_password"

def job():
    print("Running daily task email...")
    send_task_email(SENDER, RECEIVER, APP_PASSWORD)

schedule.every().day.at("08:00").do(job)

print("Scheduler started. Press Ctrl+C to stop.")
while True:
    schedule.run_pending()
    time.sleep(60)
