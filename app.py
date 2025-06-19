import json
import os
from datetime import datetime
from flask import Flask, request

app = Flask(__name__)

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

    return output_message, 200, {'Content-Type': 'text/plain; charset=utf-8'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
