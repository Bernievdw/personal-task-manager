import pandas as pd
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_task_email(sender_email, receiver_email, password):
    tasks = pd.read_csv("tasks.csv")
    tasks['deadline'] = pd.to_datetime(tasks['deadline'])
    today = datetime.today()

    overdue = tasks[(tasks['deadline'] < today) & (tasks['status'] == 'Incomplete')]
    high_priority = overdue[overdue['priority']=="High"]

    html = f"""
    <html>
    <body>
        <h2>Daily Task Summary</h2>
        <p>Today: {today.date()}</p>
        <h3>Overdue Tasks:</h3>
        {overdue.to_html(index=False) if not overdue.empty else "<p>No overdue tasks! ✅</p>"}
        <h3>High Priority Overdue Tasks:</h3>
        {high_priority.to_html(index=False) if not high_priority.empty else "<p>None 🎉</p>"}
    </body>
    </html>
    """

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = "Daily Task Summary"
    msg.attach(MIMEText(html, 'html'))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, password)
        server.send_message(msg)
    print("Email sent successfully!")

if __name__ == "__main__":
    sender = "youremail@gmail.com"
    receiver = "receiver@gmail.com"
    app_password = "your_app_password"
    send_task_email(sender, receiver, app_password)
