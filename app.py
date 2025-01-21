V.3-final-product-commit
import os
from flask import Flask, render_template, request, jsonify
import sqlite3
import pandas as pd
import requests
import plotly.express as px
from statsmodels.tsa.arima.model import ARIMA

app = Flask(__name__)

# Database Connection
DATABASE = 'financial_data.db'

def get_db_connection():
    """Connect to the SQLite database."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Fetch Data from FRED API and Store in Database
def fetch_fred_data(series_id):
    """Fetch interest rate data from FRED API and store it in SQLite database."""
    try:
        api_key = 'f5a6985cdda556dd519bb3329e8f2f38' 
        url = f'https://api.stlouisfed.org/fred/series/observations?series_id={series_id}&api_key={api_key}&file_type=json'
        response = requests.get(url).json()

        observations = response.get('observations', [])
        data = pd.DataFrame(observations)

        # Clean and preprocess
        data['date'] = pd.to_datetime(data['date'], errors='coerce')
        data['value'] = pd.to_numeric(data['value'], errors='coerce')
        data.dropna(inplace=True)

        conn = get_db_connection()
        data.to_sql(series_id, conn, if_exists='replace', index=False)
        conn.close()
        print(f"Data for series ID '{series_id}' successfully fetched and stored.")
        return data
    except Exception as e:
        print(f"Error fetching data for series ID '{series_id}': {e}")
        return None

# Route to Serve the Main HTML Page
@app.route('/')
def home():
    """Render the main HTML page."""
    return render_template('index.html')

# API for Interest Rate Analysis and Prediction
@app.route('/api/analyze', methods=['POST'])
def analyze_interest_rates():
    """Analyze interest rate trends and predict future values using ARIMA."""
    try:
        data = request.json
        series_id = data.get('series_id')
        principal = data.get('principal')
        years = data.get('years')

        # Validate input
        if not series_id:
            return jsonify({'error': 'Series ID is required'}), 400

        # Fetch data from the database
        conn = get_db_connection()
        query = f'SELECT * FROM {series_id}'
        df = pd.read_sql_query(query, conn)
        conn.close()

        if df.empty:
            return jsonify({'error': f'No data found for series ID {series_id}'}), 404

        # Clean and preprocess
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df.dropna(subset=['date'], inplace=True)
        df.set_index('date', inplace=True)
        df.sort_index(inplace=True)

        # Advanced Visualisation
        fig = px.line(
            df, x=df.index, y='value',
            title=f'Interest Rate Trends ({series_id})',
            width=1000, height=600
        )
        fig.update_layout(title_font_size=20, xaxis_title='Date', yaxis_title='Interest Rate')
        fig_json = fig.to_json()

        # ARIMA Model for Forecasting
        model = ARIMA(df['value'], order=(5, 1, 0))  # Example order, adjust as needed
        model_fit = model.fit()

        # Forecast the next 12 months
        forecast = model_fit.forecast(steps=12)
        forecast_dates = pd.date_range(df.index[-1], periods=12, freq='M')
        forecast_df = pd.DataFrame({'date': forecast_dates, 'forecast': forecast})

        # Money Growth Calculation
        if principal and years:
            latest_interest_rate = df['value'].iloc[-1]
            future_value = float(principal) * (1 + latest_interest_rate / 100) ** int(years)
        else:
            future_value = None

        # Return results
        return jsonify({
            'visualisation': fig_json,
            'forecast': forecast_df.to_dict(orient='records'),
            'future_value': future_value
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Main Entry Point
if __name__ == '__main__':
    fetch_fred_data('FEDFUNDS')  # Fetch data before running the app
    app.run(debug=True)

from flask import Flask, jsonify, request, render_template
import requests

app = Flask(__name__)

def fetch_interest_rate(api_key, series_id):
    """
    Fetches interest rate data from the FRED API.

    Args:
        api_key (str):  FRED API key.
        series_id (str): The FRED series ID for the interest rate (e.g., 'DGS10' for 10-year Treasury yield).

    Returns:
        float: The latest interest rate.
    """
    try:
        url = f"https://api.stlouisfed.org/fred/series/observations?series_id={series_id}&api_key={api_key}&file_type=json"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # Get the most recent observation
        latest_observation = data['observations'][-1]
        return float(latest_observation['value'])
    except Exception as e:
        print(f"Error fetching interest rate: {e}")
        return None

@app.route('/')
def home():
    return render_template('index.html'), 200, {'Content-Type': 'text/html'}


@app.route('/api/interest-rate', methods=['GET'])
def get_interest_rate():
    """
    API endpoint to fetch the interest rate.

    Returns:
        JSON: Interest rate or error message.
    """
    API_KEY = "f5a6985cdda556dd519bb3329e8f2f38"  # Replace with  FRED API key
    SERIES_ID = "DGS10"  # 10-year Treasury yield

    interest_rate = fetch_interest_rate(API_KEY, SERIES_ID)
    if interest_rate is not None:
        return jsonify({"interest_rate": interest_rate})
    return jsonify({"error": "Failed to fetch interest rate"}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5001)
main
