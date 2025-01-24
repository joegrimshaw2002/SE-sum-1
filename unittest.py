import unittest
from app import calculate_savings 

class TestSavingsCalculator(unittest.TestCase):

    def setUp(self):
        """Set up to capture output to a file."""
        self.output_file = "unittest_output.txt"

    def tearDown(self):
        """Clean up resources after tests."""
        with open(self.output_file, "a") as f:
            f.write("\nAll tests completed.\n")

    def write_output(self, message):
        """Helper function to write output to file."""
        with open(self.output_file, "a") as f:
            f.write(message + "\n")

    def test_calculate_savings_simple(self):
        """Test simple case of savings calculation."""
        principal = 1000
        years = 5
        rate = 0.05  # Assume 5% annual interest
        expected_result = 1000 * ((1 + rate) ** years)
        result = calculate_savings(principal, years, rate)
        self.assertAlmostEqual(result, expected_result, places=2)
        self.write_output("test_calculate_savings_simple passed.")

    def test_calculate_savings_zero_principal(self):
        """Test savings calculation with zero initial principal."""
        result = calculate_savings(0, 10, 0.05)
        self.assertEqual(result, 0)
        self.write_output("test_calculate_savings_zero_principal passed.")

    def test_calculate_savings_negative_principal(self):
        """Test savings calculation with negative principal, should raise ValueError."""
        try:
            calculate_savings(-1000, 5, 0.05)
        except ValueError as e:
            self.write_output(f"test_calculate_savings_negative_principal passed: {str(e)}")
            return
        self.write_output("test_calculate_savings_negative_principal failed: ValueError not raised.")
        self.fail("ValueError not raised for negative principal.")

    def test_calculate_savings_zero_years(self):
        """Test calculation with zero years, should return initial principal."""
        result = calculate_savings(1000, 0, 0.05)
        self.assertEqual(result, 1000)
        self.write_output("test_calculate_savings_zero_years passed.")

    def test_calculate_savings_high_interest_rate(self):
        """Test calculation with a very high interest rate."""
        principal = 1000
        years = 3
        rate = 1.0  # 100% annual interest
        expected_result = 1000 * ((1 + rate) ** years)
        result = calculate_savings(principal, years, rate)
        self.assertAlmostEqual(result, expected_result, places=2)
        self.write_output("test_calculate_savings_high_interest_rate passed.")

if __name__ == "__main__":
    with open("unittest_output.txt", "w") as f:
        f.write("Running Tests:\n\n")
    unittest.main()
