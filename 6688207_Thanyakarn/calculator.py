#!/usr/bin/env python3
"""
Simple Calculator
Supports basic arithmetic operations: addition, subtraction, multiplication, and division.
"""

def add(a, b):
    """Return the sum of a and b."""
    return a + b

def subtract(a, b):
    """Return the difference of a and b."""
    return a - b

def multiply(a, b):
    """Return the product of a and b."""
    return a * b

def divide(a, b):
    """Return the quotient of a and b. Raises ValueError if b is zero."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

def main():
    """Main function to run the calculator."""
    print("Simple Calculator")
    print("Operations: +, -, *, /")
    print("Enter 'quit' to exit")

    while True:
        try:
            expression = input("Enter expression (e.g., 2 + 3): ").strip()
            if expression.lower() == 'quit':
                break

            # Parse the expression
            parts = expression.split()
            if len(parts) != 3:
                print("Invalid format. Use: number operator number")
                continue

            a_str, op, b_str = parts
            a = float(a_str)
            b = float(b_str)

            if op == '+':
                result = add(a, b)
            elif op == '-':
                result = subtract(a, b)
            elif op == '*':
                result = multiply(a, b)
            elif op == '/':
                result = divide(a, b)
            else:
                print("Invalid operator. Use +, -, *, /")
                continue

            print(f"Result: {result}")

        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()