from flask import Flask, request, jsonify
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, timedelta

# =====================================================
# CONFIGURATION
# =====================================================

API_KEY = "SECRET123"  # Simple API key for request authorization
SPREADSHEET_NAME = "currency_rates"  # Google Sheet name

# =====================================================
# GOOGLE SHEETS AUTHORIZATION
# =====================================================

# Required scopes to read/write Google Sheets
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

# Load service account credentials from JSON file
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    "/home/kunitskii/currency_updater/credentials.json",
    scope
)

# Authorize gspread client
client = gspread.authorize(credentials)

# Open Google Sheet (first worksheet)
sheet = client.open(SPREADSHEET_NAME).sheet1

# =====================================================
# FLASK APPLICATION
# =====================================================

app = Flask(__name__)

# =====================================================
# HELPER FUNCTIONS
# =====================================================

def daterange(start_date, end_date):
    """
    Generator that yields dates from start_date to end_date (inclusive)
    """
    for n in range((end_date - start_date).days + 1):
        yield start_date + timedelta(days=n)


def get_usd_rate(date_obj):
    """
    Returns USD/UAH exchange rate from NBU API.
    If the rate is not available for the given date,
    the function goes backwards day by day until a rate is found.
    """

    max_attempts = 10  # How many days back we try
    attempts = 0

    while attempts < max_attempts:
        date_str = date_obj.strftime("%Y%m%d")

        url = (
            "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange"
            f"?valcode=USD&date={date_str}&json"
        )

        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            if data:
                return data[0]["rate"]

        # If no rate found, go one day back
        date_obj -= timedelta(days=1)
        attempts += 1

    raise Exception("USD exchange rate not found for the given period")

# =====================================================
# API ENDPOINT
# =====================================================

@app.route("/update", methods=["GET"])
def update_currency():
    """
    Updates USD/UAH exchange rates in Google Sheets
    for the given date range.
    """

    # -----------------------------
    # Authorization check
    # -----------------------------
    request_api_key = request.headers.get("X-API-KEY")
    if request_api_key != API_KEY:
        return jsonify({"error": "Unauthorized"}), 401

    # -----------------------------
    # Read date parameters
    # -----------------------------
    update_from = request.args.get("update_from")
    update_to = request.args.get("update_to")

    today = datetime.today().date()

    if update_from:
        start_date = datetime.strptime(update_from, "%Y-%m-%d").date()
    else:
        start_date = today

    if update_to:
        end_date = datetime.strptime(update_to, "%Y-%m-%d").date()
    else:
        end_date = today

    if start_date > end_date:
        return jsonify({"error": "update_from cannot be later than update_to"}), 400

    updated_rows = []

    # -----------------------------
    # Process each date in range
    # -----------------------------
    for current_date in daterange(start_date, end_date):

        rate = get_usd_rate(current_date)
        formatted_date = current_date.strftime("%d.%m.%Y")

        # Check if date already exists in the sheet
        cell = sheet.find(formatted_date)

        if cell:
            # Update existing row
            sheet.update_cell(cell.row, 2, rate)
        else:
            # Append new row
            sheet.append_row([formatted_date, rate])

        updated_rows.append({
            "date": formatted_date,
            "usd_uah": rate
        })

    return jsonify({
        "status": "success",
        "updated_rows": updated_rows
    })

# =====================================================
# APPLICATION ENTRY POINT
# =====================================================

if __name__ == "__main__":
    app.run(debug=True)
