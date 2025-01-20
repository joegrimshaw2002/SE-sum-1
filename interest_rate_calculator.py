import requests

def fetch_interest_rate(api_key, series_id):
    """
    Fetches interest rate data from the FRED API.

    Args:
        api_key (str): Your FRED API key.
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

def calculate_savings_growth(principal, annual_rate, years):
    """
    Calculates the future value of savings with compound interest.

    Args:
        principal (float): Initial savings amount.
        annual_rate (float): Annual interest rate as a percentage (e.g., 5 for 5%).
        years (int): Number of years.

    Returns:
        float: Future value of the savings.
    """
    try:
        return principal * (1 + annual_rate / 100) ** years
    except Exception as e:
        print(f"Error calculating savings growth: {e}")
        return None

if __name__ == "__main__":
    API_KEY = "f5a6985cdda556dd519bb3329e8f2f38"
    SERIES_ID = "DGS10"  # 10-year Treasury yield

    # Get interest rate from API
    interest_rate = fetch_interest_rate(API_KEY, SERIES_ID)
    if interest_rate is not None:
        print(f"Fetched interest rate: {interest_rate}%")

        # Calculate savings growth
        principal = 2000  # Initial savings in dollars
        years = 10  # Time horizon in years
        future_value = calculate_savings_growth(principal, interest_rate, years)
        print(f"Future value of savings: ${future_value:.2f}")
    else:
        print("Failed to fetch interest rate.")