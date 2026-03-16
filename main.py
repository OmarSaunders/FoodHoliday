import json
import os
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from dotenv import load_dotenv

#Load environnment variables from .env file
load_dotenv()

JSON_FILE_PATH = 'holidays.json' # Make sure this file is in the same directory

def load_holidays():
    """Loads holiday data from the JSON file."""
    try:
        with open(JSON_FILE_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        print(f"Error: {JSON_FILE_PATH} not found. Make sure it's in the same directory as the script.")
        return None
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {JSON_FILE_PATH}.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred loading JSON: {e}")
        return None

def send_local_email(subject, body):
    sender_email = os.environ.get('SENDER_EMAIL_ADDRESS')
    sender_password = os.environ.get('SENDER_EMAIL_PASSWORD')
    recipient_emails_str = os.environ.get('RECIPIENT_EMAILS')

    if not all([sender_email, sender_password, recipient_emails_str]):
        print("Error: Email credentials or recipients not set in environment variables. Cannot send email.")
        print(f"SENDER_EMAIL_ADDRESS: {'SET' if sender_email else 'NOT SET'}")
        print(f"SENDER_EMAIL_PASSWORD: {'SET' if sender_password else 'NOT SET'}")
        print(f"RECIPIENT_EMAILS: {'SET' if recipient_emails_str else 'NOT SET'}")
        return False

    recipient_emails = [email.strip() for email in recipient_emails_str.split(',')]

    smtp_server = 'smtp.gmail.com'
    smtp_port = 587

    try:
        msg = MIMEText(body, 'plain', 'utf-8')
        msg['From'] = Header(f"Food Holiday Bot <{sender_email}>", 'utf-8')
        msg['To'] = Header(', '.join(recipient_emails), 'utf-8')
        msg['Subject'] = Header(subject, 'utf-8')

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_emails, msg.as_string())
        print(f"Email sent successfully to {', '.join(recipient_emails)}")
        return True
    except smtplib.SMTPAuthenticationError:
        print("SMTP Authentication Error: Check your SENDER_EMAIL_ADDRESS and SENDER_EMAIL_PASSWORD (especially for App Passwords if using Gmail 2FA).")
        return False
    except smtplib.SMTPConnectError as e:
        print(f"SMTP Connection Error: Could not connect to {smtp_server}:{smtp_port}. Check network or server availability. Error: {e}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred while sending email: {e}")
        return False

if __name__ == '__main__':
    # This is the main logic that will run when the script is executed
    holidays = load_holidays()
    if holidays is None:
        print("Aborting: Could not load holiday data.")
        exit(1) # Exit with an error code

    today = datetime.now().date()
    current_month_day = today.strftime("%B %-d")
    print(f"Checking holidays for current date: {today} ({current_month_day})")

    todays_holidays = []
    for holiday in holidays:
        date_desc = holiday.get('date_description', '')
        parts = date_desc.split()
        if len(parts) >= 2:
            holiday_month_day = f"{parts[0]} {parts[1].rstrip(',')}"
            if holiday_month_day == current_month_day:
                todays_holidays.append(holiday.get('name', 'Unnamed Holiday'))

    print(f"Found {len(todays_holidays)} holidays for {current_month_day}.")

    today_formatted = today.strftime("%B %d, %Y")
    if todays_holidays:
        holiday_list = "\n* ".join(todays_holidays)
        output_message = f"Today's date is {today_formatted} and these are the current food holidays:\n* {holiday_list}"
    else:
        output_message = f"Today's date is {today_formatted} and there are no specific food holidays listed for today."

    email_subject = f"Daily Food Holiday Report for {today_formatted}"
    send_local_email(email_subject, output_message)

