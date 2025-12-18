# Sales & Performance Dashboard

## Project Overview

This project was developed as a technical test assignment and demonstrates a complete analytics solution including:

- Power BI dashboard with sales, calls, and KPI analytics
- Python-based API service for updating currency exchange rates
- Google Sheets used as an external data source for currency rates
- Integration between Python service, Google Sheets, and Power BI

---

## Power BI Dashboard

The Power BI report provides performance analytics by manager with the following key metrics:

- KPI Minutes vs Actual Call Minutes
- KPI Leads vs Actual Leads
- Successful Calls
- Sales Amount converted to USD
- Successful Events and Personal deals

### Key Features

- Dynamic date filtering using a calendar slicer
- KPI calculation based on working days (Monday–Friday)
- Currency conversion using daily USD/UAH exchange rates
- Star schema data model (fact and dimension tables)
- Clear comparison of KPI vs actual performance

---

## Currency Update Service (Python)

A Python API service built with Flask is used to update USD/UAH exchange rates.

### API Features

- Accepts date range parameters: `update_from` and `update_to`
- Date format: `yyyy-mm-dd`
- Default behavior: both dates equal the current date
- Uses the National Bank of Ukraine (NBU) public API
- Fallback logic: if a rate for a specific date is unavailable, the service uses the last available rate before that date
- Simple API key authorization
- Writes and updates currency data in Google Sheets

---

## API Usage

### Endpoint

GET /update

sql
Копировать код

### Headers

| Header       | Value     |
|--------------|-----------|
| X-API-KEY    | SECRET123 |

### Query Parameters

| Parameter    | Description                         |
|--------------|-------------------------------------|
| update_from | Start date (yyyy-mm-dd)             |
| update_to   | End date (yyyy-mm-dd)               |

### Example Request

https://kunitskii.pythonanywhere.com/update?update_from=2023-01-02&update_to=2023-01-08

yaml
Копировать код

---

## Google Sheets

The service updates the following Google Sheet structure:

| Date       | USD_UAH |
|------------|---------|
| 02.01.2023 | 36.56   |

The Google Sheet is connected to Power BI and used for currency conversion in sales calculations.

Access to the Google Sheet is provided for verification.

---

## Technologies Used

- Power BI
- Python (Flask)
- Google Sheets API
- National Bank of Ukraine Exchange Rate API

---

## Notes & Assumptions

- If the exchange rate for a specific date is unavailable, the last available rate before that date is used
- KPI values are calculated only for working days (Monday–Friday)
- Currency rates are updated on demand via API call

---

## Author

**Oleksii Kunytskyi**  
📧 Email: kunytskyi.data@gmail.com  
💼 LinkedIn: https://www.linkedin.com/in/datapulse/
