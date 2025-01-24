// Assuming the relevant functions in scripts.js are modular and exportable.
import { calculateSavings, updateSavingsResult } from './scripts';

// Using Jest as the testing framework
describe('Savings Calculator', () => {

    test('calculateSavings - Basic Calculation', () => {
        const principal = 1000;
        const years = 5;
        const rate = 0.05; // 5% annual interest
        const expected = 1000 * Math.pow((1 + rate), years);
        expect(calculateSavings(principal, years, rate)).toBeCloseTo(expected, 2);
    });

    test('calculateSavings - Zero Principal', () => {
        const principal = 0;
        const years = 10;
        const rate = 0.05;
        expect(calculateSavings(principal, years, rate)).toBe(0);
    });

    test('calculateSavings - Negative Principal', () => {
        const principal = -1000;
        const years = 5;
        const rate = 0.05;
        expect(() => calculateSavings(principal, years, rate)).toThrow('Principal amount cannot be negative');
    });

    test('updateSavingsResult - Correct DOM Update', () => {
        // Set up DOM
        document.body.innerHTML = '<div id="savings-result"></div>';
        
        const resultContainer = document.getElementById('savings-result');
        const resultValue = '$1,276.45';

        updateSavingsResult(resultValue);

        expect(resultContainer.textContent).toBe(`Savings after the specified period: ${resultValue}`);
    });

    test('calculateSavings - High Interest Rate', () => {
        const principal = 1000;
        const years = 2;
        const rate = 1.0; // 100% annual interest
        const expected = 1000 * Math.pow((1 + rate), years);
        expect(calculateSavings(principal, years, rate)).toBeCloseTo(expected, 2);
    });
});
