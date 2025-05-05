import json
import os
from datetime import datetime
from flask import Flask, request
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv  # For loading environment variables

load_dotenv()  # Load environment variables from a .env file (if it exists)

app = Flask(__name__)
JSON_FILE_PATH = 'holidays.json'
SENDER_EMAIL = os.environ.get('SENDER_EMAIL')
RECEIVER_EMAILS = os.environ.get('RECEIVER_EMAILS', '').split(',')  # Converts comma-separated string to list


# --- Email Configuration ---
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587  # For TLS encryption

# --- Load Holidays Function (No Change Needed) ---
def load_holidays():
    """Loads holiday data from the JSON file."""
    try:
        with open(JSON_FILE_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        app.logger.error(f"Error: {JSON_FILE_PATH} not found.")
        return None
    except json.JSONDecodeError:
        app.logger.error(f"Error: Could not decode JSON from {JSON_FILE_PATH}.")
        return None
    except Exception as e:
        app.logger.error(f"An unexpected error occurred loading JSON: {e}")
        return None

# --- Send Email Function ---
def send_email(subject, body, recipients):
    """Sends an email with the given subject and body to the specified recipients."""
    sender_password = os.environ.get('GMAIL_PASSWORD')  # Get password from environment variable

    if not sender_password:
        app.logger.error("Error: GMAIL_PASSWORD environment variable not set.")
        return False

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  # Upgrade connection to secure TLS
        server.login(SENDER_EMAIL, sender_password)

        msg = MIMEText(body, 'plain', 'utf-8')
        msg['Subject'] = subject
        msg['From'] = SENDER_EMAIL
        msg['To'] = ', '.join(recipients)  # Format recipients for the header

        server.sendmail(SENDER_EMAIL, recipients, msg.as_string())
        app.logger.info(f"Email sent successfully to {', '.join(recipients)}")
        server.quit()
        return True
    except Exception as e:
        app.logger.error(f"Error sending email: {e}")
        return False

# --- Main Flask Route (Modified to Send Email) ---
@app.route('/')
def get_todays_holiday():
    """
    Endpoint to get the food holiday(s) for the current date as plain text and send an email.
    Can also accept a 'date' query parameter in 'MM-DD' format for testing.
    e.g., /?date=01-15
    """
    holidays = load_holidays()
    if holidays is None:
        error_message = "Could not load holiday data."
        send_email("Food Holiday Report Error", error_message, RECEIVER_EMAILS)
        return error_message, 500, {'Content-Type': 'text/plain; charset=utf-8'}

    test_date_str = request.args.get('date')
    today = datetime.now().date()

    if test_date_str:
        try:
            test_date = datetime.strptime(f"2024-{test_date_str}", "%Y-%m-%d").date()
            current_month_day = test_date.strftime("%B %-d")
            app.logger.info(f"Using provided date: {test_date_str} ({current_month_day})")
        except ValueError:
            error_message = "Invalid date format. Please use MM-DD."
            send_email("Food Holiday Report Error", error_message, RECEIVER_EMAILS)
            return error_message, 400, {'Content-Type': 'text/plain; charset=utf-8'}
    else:
        current_month_day = today.strftime("%B %-d")
        app.logger.info(f"Checking holidays for current date: {today} ({current_month_day})")

    todays_holidays = []
    for holiday in holidays:
        date_desc = holiday.get('date_description', '')
        parts = date_desc.split()
        if len(parts) >= 2:
            holiday_month_day = f"{parts[0]} {parts[1].rstrip(',')}"
            if holiday_month_day == current_month_day:
                todays_holidays.append(holiday.get('name', 'Unnamed Holiday'))

    app.logger.info(f"Found {len(todays_holidays)} holidays for {current_month_day}.")

    # Format the output as plain text
    today_formatted = today.strftime("%B %d, %Y")
    if todays_holidays:
        holiday_list = "\n* ".join(todays_holidays)
        output_message = f"Today's date is {today_formatted} and these are the current food holidays:\n* {holiday_list}"
        email_subject = f"Today's Food Holidays - {today_formatted}"
        email_body = output_message
    else:
        output_message = f"Today's date is {today_formatted} and there are no specific food holidays listed for today."
        email_subject = f"Today's Food Holiday Report - {today_formatted}"
        email_body = output_message

    # Send the email after generating the report
    send_email(email_subject, email_body, RECEIVER_EMAILS)

    return output_message, 200, {'Content-Type': 'text/plain; charset=utf-8'}

if __name__ == '__main__':
    # Create a dummy holidays.json file for testing if it doesn't exist
    if not os.path.exists(JSON_FILE_PATH):
        dummy_data = [
            {"name": "National Pizza Day", "date_description": "February 9"},
            {"name": "National Ice Cream Day", "date_description": "July 21"},
            {"name": "National Coffee Day", "date_description": "September 29"},
            {"name": "National Burrito Day", "date_description": "April 4"},
            {"name": "National Grilled Cheese Sandwich Day", "date_description": "April 12"},
        ]
        with open(JSON_FILE_PATH, 'w', encoding='utf-8') as f:
            json.dump(dummy_data, f, indent=4)
        print(f"Created a dummy '{JSON_FILE_PATH}' file for testing.")

    app.run(host='0.0.0.0', port=8080, debug=True)