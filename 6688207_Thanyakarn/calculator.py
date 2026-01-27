#!/usr/bin/env python3
"""
Simple Calculator
Supports basic arithmetic operations: addition, subtraction, multiplication, and division.
Also includes velocity calculation: velocity = distance / time
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

def calculate_velocity(distance, time):
    """
    Calculate velocity given distance and time.

    Args:
        distance (float): The distance traveled.
        time (float): The time taken.

    Returns:
        float: The velocity.

    Raises:
        ValueError: If time is zero or negative.
    """
    if time <= 0:
        raise ValueError("Time must be positive and greater than zero")
    return distance / time

def main():
    """Main function to run the calculator."""
    print("Simple Calculator and Velocity Calculator")
    print("Arithmetic operations: +, -, *, / (e.g., 2 + 3)")
    print("Velocity calculation: velocity distance time (e.g., velocity 100 10)")
    print("Enter 'quit' to exit")

    while True:
        try:
            expression = input("Enter expression: ").strip()
            if expression.lower() == 'quit':
                break

            parts = expression.split()
            if len(parts) == 0:
                continue

            if parts[0].lower() == 'velocity':
                if len(parts) != 3:
                    print("Invalid format for velocity. Use: velocity distance time")
                    continue
                _, distance_str, time_str = parts
                distance = float(distance_str)
                time = float(time_str)
                result = calculate_velocity(distance, time)
                print(f"Velocity: {result} units per time unit")
            else:
                # Normal arithmetic
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