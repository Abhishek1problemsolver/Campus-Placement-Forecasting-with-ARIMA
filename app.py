from flask import Flask, jsonify
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt
import seaborn as sns
import os
import json

app = Flask(__name__)
csv_file = './campus_placement_by_department.csv'  # Update with your CSV file path
forecasted_csv_dir = './forecasted_csv'  # Directory to save forecasted CSV data
plot_dir = './plots'  # Directory to save plot images

def load_data(filename):
    try:
        df = pd.read_csv(filename)
        return df
    except Exception as e:
        print(f"Error loading CSV file: {e}")
        return None

def preprocess_data(df):
    df['Year'] = pd.to_datetime(df['Year'].astype(str), format='%Y')
    df.set_index('Year', inplace=True)
    df.sort_index(inplace=True)
    return df

def build_arima_model(series):
    model = ARIMA(series, order=(5, 1, 0))  # Example ARIMA parameters, tune as needed
    model_fit = model.fit()
    return model_fit

def forecast_sales(model, steps):
    forecast = model.forecast(steps=steps)
    return forecast

def save_plot(series, forecast, department):
    sns.set(style="whitegrid")
    plt.figure(figsize=(14, 7))
    plt.plot(series.index, series.values, label='Previous Placement', color='blue', linestyle='-', linewidth=2)
    plt.plot(pd.date_range(start=series.index[-1], periods=len(forecast), freq='Y'), forecast, label='Forecasted Placement', color='red', linestyle='--', linewidth=2)
    plt.title(f'Forecasted Placement for {department}', fontsize=16)
    plt.xlabel('Year', fontsize=14)
    plt.ylabel('Forecasted Placement', fontsize=14)
    plt.legend(fontsize=12)
    plt.tight_layout()
    
    plot_filename = os.path.join(plot_dir, f'{department}_forecast_plot.png')
    plt.savefig(plot_filename)
    plt.close()
    
    return plot_filename

def save_forecast_csv(department, forecast_data):
    csv_filename = os.path.join(forecasted_csv_dir, f'{department}_forecast_data.csv')
    forecast_data.to_csv(csv_filename, index=False)
    return csv_filename

@app.route('/api/forecast/<department>', methods=['GET'])
def get_forecast(department):
    try:
        df = load_data(csv_file)
        if df is None:
            return jsonify({'error': 'Failed to load data'}), 500
        
        df = preprocess_data(df)
        
        if department not in df['Department'].unique():
            return jsonify({'error': f'Department {department} not found'}), 404
        
        department_df = df[df['Department'] == department]
        series = department_df['Placed_Students']
        
        model = build_arima_model(series)
        
        # Forecast 12 steps ahead (adjust as needed)
        forecast_steps = 12
        forecast = forecast_sales(model, steps=forecast_steps)
        
        # Save plot to file
        plot_filename = save_plot(series, forecast, department)
        
        # Save forecast data to CSV file
        forecast_data = pd.DataFrame({
            'Year': pd.date_range(start=series.index[-1], periods=len(forecast), freq='Y'),
            'Forecasted_Placement': forecast.tolist()
        })
        csv_filename = save_forecast_csv(department, forecast_data)
        
        # Return JSON response with CSV and plot URLs
        return jsonify({
            'department': department,
            'forecasted_placement': forecast.tolist(),
            'csv_url': f"http://127.0.0.1:5000/{csv_filename}",
            'plot_url': f"http://127.0.0.1:5000/{plot_filename}"
        })
        
    except Exception as e:
        return jsonify({'error': f"An error occurred: {e}"}), 500

@app.route('/', methods=['GET'])
def index():
    departments = ["Computer Science", "Mechanical Engineering", "Electrical Engineering", "Civil Engineering"]
    base_url = "http://127.0.0.1:5000/api/forecast/"
    urls = {dept: base_url + dept for dept in departments}
    return jsonify(urls)

if __name__ == '__main__':
    if not os.path.exists(forecasted_csv_dir):
        os.makedirs(forecasted_csv_dir)
    if not os.path.exists(plot_dir):
        os.makedirs(plot_dir)
    app.run(debug=True)
