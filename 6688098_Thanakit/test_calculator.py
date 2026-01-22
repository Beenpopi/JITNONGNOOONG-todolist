"""
Unit tests for the calculator module.
"""

import pytest
from calculator import Calculator


class TestCalculator:
    """Test suite for the Calculator class."""

    def test_add(self):
        """Test addition operation."""
        assert Calculator.add(5, 3) == 8
        assert Calculator.add(-5, 3) == -2
        assert Calculator.add(0, 0) == 0
        assert Calculator.add(2.5, 1.5) == 4.0

    def test_subtract(self):
        """Test subtraction operation."""
        assert Calculator.subtract(10, 5) == 5
        assert Calculator.subtract(5, 10) == -5
        assert Calculator.subtract(0, 0) == 0
        assert Calculator.subtract(10.5, 2.5) == 8.0

    def test_multiply(self):
        """Test multiplication operation."""
        assert Calculator.multiply(5, 3) == 15
        assert Calculator.multiply(-5, 3) == -15
        assert Calculator.multiply(0, 100) == 0
        assert Calculator.multiply(2.5, 4) == 10.0

    def test_divide(self):
        """Test division operation."""
        assert Calculator.divide(10, 2) == 5
        assert Calculator.divide(15, 3) == 5
        assert Calculator.divide(7, 2) == 3.5
        assert Calculator.divide(-10, 2) == -5

    def test_divide_by_zero(self):
        """Test that division by zero raises ValueError."""
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            Calculator.divide(10, 0)

    def test_divide_zero_numerator(self):
        """Test division with zero numerator."""
        assert Calculator.divide(0, 5) == 0
