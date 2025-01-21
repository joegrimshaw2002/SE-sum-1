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
