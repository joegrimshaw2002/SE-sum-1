console.log("JavaScript file loaded successfully!");

document.getElementById('savings-form').addEventListener('submit', async (event) => {
    event.preventDefault();

    const principal = parseFloat(document.getElementById('principal').value);
    const years = parseInt(document.getElementById('years').value);

    try {
        // Fetch interest rate (replace with backend API endpoint if needed)
        const response = await fetch('/api/interest-rate');
        const data = await response.json();

        if (response.ok && data.interest_rate) {
            const interestRate = data.interest_rate;

            // Calculate savings growth
            const futureValue = principal * Math.pow(1 + interestRate / 100, years);
            document.getElementById('savings-result').textContent =
                `Future savings value: $${futureValue.toFixed(2)}`;
        } else {
            throw new Error(data.error || 'Failed to fetch interest rate');
        }
    } catch (error) {
        document.getElementById('savings-result').textContent = `Error: ${error.message}`;
    }
});

