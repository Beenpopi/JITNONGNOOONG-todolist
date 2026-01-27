"""
Simple calculator module for basic arithmetic operations.
"""


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


def calculate_velocity(distance: float, time: float) -> float:
    """
    Calculate velocity from distance and time.

    Args:
        distance: Distance traveled
        time: Time taken

    Returns:
        Velocity (distance / time)

    Raises:
        ValueError: If time is zero or negative
    """
    if time <= 0:
        raise ValueError("Time must be greater than zero")
    return distance / time


def main():
    """Main function to run the calculator interactively."""
    print("Simple Calculator")
    print("Operations: add, subtract, multiply, divide, velocity")
    print("Type 'quit' to exit")

    while True:
        operation = input("\nEnter operation (add/subtract/multiply/divide/velocity) or 'quit': ").strip().lower()

        if operation == "quit":
            print("Goodbye!")
            break

        if operation not in ["add", "subtract", "multiply", "divide", "velocity"]:
            print("Invalid operation. Please choose: add, subtract, multiply, divide, or velocity")
            continue

        try:
            if operation == "velocity":
                distance = float(input("Enter distance: "))
                time = float(input("Enter time: "))
                result = calculate_velocity(distance, time)
                print(f"Result: Velocity = {distance} / {time} = {result}")
            else:
                a = float(input("Enter first number: "))
                b = float(input("Enter second number: "))
                if operation == "add":
                    result = add(a, b)
                elif operation == "subtract":
                    result = subtract(a, b)
                elif operation == "multiply":
                    result = multiply(a, b)
                elif operation == "divide":
                    result = divide(a, b)

                print(f"Result: {a} {operation} {b} = {result}")
        except ValueError as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()