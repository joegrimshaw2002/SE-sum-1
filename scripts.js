console.log("JavaScript file loaded successfully!");

 V.3-final-product-commit
// Attach event listener to the analysis form
document.getElementById('analysis-form').addEventListener('submit', async (event) => {
    event.preventDefault();

    // Retrieve user input
    const seriesId = document.getElementById('series-id').value.trim();
    const principal = parseFloat(document.getElementById('principal').value);
    const years = parseInt(document.getElementById('years').value);

    // Validate input
    if (!seriesId || isNaN(principal) || isNaN(years) || principal <= 0 || years <= 0) {
        document.getElementById('analysis-result').textContent = 'Please enter valid inputs.';
        return;
    }

    try {
        // Display loading message
        document.getElementById('analysis-result').textContent = 'Fetching data and analysing...';

        // Fetch data from the backend
        const response = await fetch('/api/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ series_id: seriesId, principal, years })
        });

        if (response.ok) {
            const data = await response.json();

            // Render visualisation
            renderVisualisation(data.visualisation);

            // Display forecast results
            displayForecast(data.forecast);

            // Display future value calculation
            if (data.future_value) {
                document.getElementById('analysis-result').innerHTML = `
                    Future Value after ${years} years: <strong>£${data.future_value.toFixed(2)}</strong>
                `;
            } else {
                document.getElementById('analysis-result').textContent = 'Unable to calculate future value.';
            }
        } else {
            const errorData = await response.json();
            document.getElementById('analysis-result').textContent =
                `Error: ${errorData.error || 'Unable to process the request.'}`;
        }
    } catch (error) {
        document.getElementById('analysis-result').textContent =
            `Unexpected Error: ${error.message}`;
    }
});

// Render Visualisation
function renderVisualisation(visualisationJson) {
    try {
        const visualisationData = JSON.parse(visualisationJson);
        Plotly.newPlot('visualisation-container', visualisationData.data, visualisationData.layout);
    } catch (error) {
        document.getElementById('visualisation-container').textContent =
            'Error rendering visualisation. Please try again.';
    }
}

// Display Forecast Results
function displayForecast(forecast) {
    const forecastContainer = document.getElementById('forecast-result');
    forecastContainer.innerHTML = '<h3>12-Month Forecast</h3>';

    const forecastTable = document.createElement('table');
    forecastTable.innerHTML = `
        <tr>
            <th>Date</th>
            <th>Forecasted Value</th>
        </tr>
        ${forecast
            .map(row => `<tr><td>${row.date}</td><td>${row.forecast.toFixed(2)}</td></tr>`)
            .join('')}
    `;
    forecastContainer.appendChild(forecastTable);
}

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

 main
