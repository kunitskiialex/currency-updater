# Sales & Performance Dashboard

## Project Overview

This project was created as a technical test assignment.
It includes:

- Power BI dashboard with sales, calls and KPI analytics
- Python API service for updating currency exchange rates
- Google Sheets as a data source for currency rates

---

## Power BI Dashboard

The dashboard includes the following metrics:

- KPI Minutes vs Actual Minutes
- KPI Leads vs Actual Leads
- Successful Calls
- Sales Amount (USD)
- Successful Events and Personal deals

### Key Features

- Dynamic date filtering
- KPI calculation based on working days (Mon–Fri)
- Currency conversion using daily USD/UAH rates
- Star schema data model

---

## Currency Update Service (Python)

A Python (Flask) API service is used to update USD/UAH exchange rates.

### API Features

- Accepts date range parameters: `update_from`, `update_to`
- Default behavior: current date
- Uses NBU public API
- Fallback logic for missing dates
- Simple API key authorization
- Writes data to Google Sheets

---

## API Usage

### Endpoint
GET /update

### Headers

X-API-KEY: SECRET123


### Query Parameters

| Parameter     | Description                     |
|--------------|---------------------------------|
| update_from  | Start date (yyyy-mm-dd)         |
| update_to    | End date (yyyy-mm-dd)           |

### Example Request



https://kunitskii.pythonanywhere.com/update?update_from=2023-01-02&update_to=2023-01-08


---

## Google Sheets

The service updates the following Google Sheet:

| Date       | USD_UAH |
|------------|---------|
| 02.01.2023 | 36.56   |

The sheet is connected to Power BI for currency conversion.

---

## Technologies Used

- Power BI
- Python (Flask)
- Google Sheets API
- NBU Exchange Rate API

---

## Notes & Assumptions

- If exchange rate for a specific date is unavailable,
  the last available rate before that date is used.
- KPI values are calculated only for working days (Mon–Fri).

---

## Author

Oleksii Kunytskyi  
Email: kunytskyi.data@gmail.com  
LinkedIn: https://www.linkedin.com/in/datapulse/
