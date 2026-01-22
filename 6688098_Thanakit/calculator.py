"""
Simple calculator module for basic arithmetic operations.
"""


class Calculator:
    """A simple calculator that performs basic arithmetic operations."""

    @staticmethod
    def add(a: float, b: float) -> float:
        """
        Add two numbers.
        
        Args:
            a: First number
            b: Second number
            
        Returns:
            Sum of a and b
        """
        return a + b

    @staticmethod
    def subtract(a: float, b: float) -> float:
        """
        Subtract two numbers.
        
        Args:
            a: First number
            b: Second number to subtract
            
        Returns:
            Difference of a and b
        """
        return a - b

    @staticmethod
    def multiply(a: float, b: float) -> float:
        """
        Multiply two numbers.
        
        Args:
            a: First number
            b: Second number
            
        Returns:
            Product of a and b
        """
        return a * b

    @staticmethod
    def divide(a: float, b: float) -> float:
        """
        Divide two numbers.
        
        Args:
            a: Dividend (numerator)
            b: Divisor (denominator)
            
        Returns:
            Result of a divided by b
            
        Raises:
            ValueError: If b is zero (division by zero)
        """
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b


def main():
    """Main function to demonstrate calculator usage."""
    calc = Calculator()
    
    print("=== Simple Calculator ===\n")
    
    # Examples
    a, b = 10, 5
    
    print(f"Number 1: {a}")
    print(f"Number 2: {b}\n")
    
    print(f"Addition: {a} + {b} = {calc.add(a, b)}")
    print(f"Subtraction: {a} - {b} = {calc.subtract(a, b)}")
    print(f"Multiplication: {a} * {b} = {calc.multiply(a, b)}")
    print(f"Division: {a} / {b} = {calc.divide(a, b)}\n")
    
    # Interactive mode
    print("=== Interactive Mode ===")
    while True:
        try:
            print("\nOperations: 1(+), 2(-), 3(*), 4(/), 5(exit)")
            choice = input("Select operation (1-5): ").strip()
            
            if choice == "5":
                print("Exiting calculator. Goodbye!")
                break
            
            if choice not in ["1", "2", "3", "4"]:
                print("Invalid choice. Please select 1-5.")
                continue
            
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
            
            if choice == "1":
                result = calc.add(num1, num2)
                operation = "+"
            elif choice == "2":
                result = calc.subtract(num1, num2)
                operation = "-"
            elif choice == "3":
                result = calc.multiply(num1, num2)
                operation = "*"
            else:  # choice == "4"
                result = calc.divide(num1, num2)
                operation = "/"
            
            print(f"Result: {num1} {operation} {num2} = {result}")
            
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Invalid input: {e}")


if __name__ == "__main__":
    main()
