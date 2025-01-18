def currency_calculator(amount, rate):
    """
    Converts an amount based on the given exchange rate.

    Parameters:
        amount (float): The amount to convert.
        rate (float): The exchange rate.

    Returns:
        float: The converted amount.
    """
    try:
        return round(amount * rate, 2)
    except Exception as e:
        print(f"Error in conversion: {e}")
        return None


if __name__ == "__main__":
    print("Welcome to the Currency Calculator!")
    try:
        amount = float(input("Enter amount in original currency: "))
        rate = float(input("Enter exchange rate: "))
        result = currency_calculator(amount, rate)
        print(f"Converted amount: {result}")
    except ValueError:
        print("Invalid input. Please enter numeric values.")
