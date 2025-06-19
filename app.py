import json
import os
from datetime import datetime
from flask import Flask, request
from flask_mail import Mail, Message # Import Mail and Message

app = Flask(__name__)

# --- Flask-Mail Configuration ---
# Use environment variables for sensitive information like email credentials
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', 'true').lower() == 'true'
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME') # Your email address (e.g., your_app_email@gmail.com)
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD') # Your email password or app-specific password
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_USERNAME') # Or a specific sender email

mail = Mail(app)

# --- End Flask-Mail Configuration ---


JSON_FILE_PATH = 'holidays.json' # Make sure this file is in the same directory

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

# --- New function to send email ---
def send_holiday_email(subject, body):
    recipient_emails_str = os.environ.get('RECIPIENT_EMAILS')
    if not recipient_emails_str:
        app.logger.error("RECIPIENT_EMAILS environment variable not set. Cannot send email.")
        return False

    recipient_emails = [email.strip() for email in recipient_emails_str.split(',')]

    try:
        msg = Message(subject, recipients=recipient_emails)
        msg.body = body
        mail.send(msg)
        app.logger.info(f"Email sent successfully to {', '.join(recipient_emails)}")
        return True
    except Exception as e:
        app.logger.error(f"Failed to send email: {e}")
        return False
# --- End new function ---

@app.route('/')
def get_todays_holiday():
    """
    Endpoint to get the food holiday(s) for the current date as plain text.
    Can also accept a 'date' query parameter in 'MM-DD' format for testing.
    e.g., /?date=01-15
    """
    holidays = load_holidays()
    if holidays is None:
        return "Could not load holiday data.", 500, {'Content-Type': 'text/plain; charset=utf-8'}

    test_date_str = request.args.get('date')
    today = datetime.now().date()

    if test_date_str:
        try:
            # Using 2024 as a placeholder year for date parsing
            test_date = datetime.strptime(f"2024-{test_date_str}", "%Y-%m-%d").date()
            current_month_day = test_date.strftime("%B %-d")
            app.logger.info(f"Using provided date: {test_date_str} ({current_month_day})")
        except ValueError:
            return "Invalid date format. Please use MM-DD.", 400, {'Content-Type': 'text/plain; charset=utf-8'}
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
    else:
        output_message = f"Today's date is {today_formatted} and there are no specific food holidays listed for today."

    # --- Send email with the holiday information ---
    email_subject = f"Daily Food Holiday Report for {today_formatted}"
    send_holiday_email(email_subject, output_message)
    # --- End email sending ---

    return output_message, 200, {'Content-Type': 'text/plain; charset=utf-8'}

if __name__ == '__main__':
    # It's recommended to set environment variables when running in production.
    # For local testing, you can set them in your terminal before running the app:
    # export MAIL_USERNAME='your_gmail_address@gmail.com'
    # export MAIL_PASSWORD='your_gmail_app_password' # Use an App Password for Gmail!
    # export RECIPIENT_EMAILS='o.a.saunders@gmail.com, jazzmine.luff@gmail.com'
    app.run(host='0.0.0.0', port=8080, debug=True)