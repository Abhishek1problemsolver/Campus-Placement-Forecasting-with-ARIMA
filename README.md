# Campus Placement Forecasting with ARIMA

## Overview
This project utilizes ARIMA (AutoRegressive Integrated Moving Average) models to forecast campus placements for various departments in an educational institution. Historical placement data is analyzed to predict future trends, aiding stakeholders in making informed decisions.

## Features
- **Data Analysis:** Historical placement data from CSV files is used for trend analysis.
- **ARIMA Modeling:** Forecast future placement numbers using ARIMA models.
- **Visualization:** Generate plots to visualize historical data and forecasted trends.
- **API Integration:** Flask API provides access to forecasted data and plot images via HTTP requests.

## Project Structure
- **`app.py`:** Flask application for serving forecasts via API endpoints.
- **`campus_placement_by_department.csv`:** Sample CSV file containing historical placement data.
- **`plots/`:** Directory to save generated plot images.
- **`forecasted_csv/`:** Directory to save forecasted data in CSV format.
- **`README.md`:** This file, providing an overview of the project, setup instructions, and usage details.

## Setup Instructions
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your-username/campus-placement-forecast.git
   cd campus-placement-forecast
