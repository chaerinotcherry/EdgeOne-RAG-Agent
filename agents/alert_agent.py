import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

load_dotenv()

def alert_agent(analysis: str, threshold_met: bool = True) -> str:
    if not threshold_met:
        return "No alert needed."

    msg = MIMEText(analysis)
    msg["Subject"] = "⚠️ EdgeOne CDN Alert"
    msg["From"] = os.getenv("ALERT_FROM_EMAIL")
    msg["To"] = os.getenv("ALERT_TO_EMAIL")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(os.getenv("ALERT_FROM_EMAIL"), os.getenv("ALERT_PASSWORD"))
        server.send_message(msg)

    return "Alert email sent!"