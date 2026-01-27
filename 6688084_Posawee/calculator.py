"""Simple calculator with basic arithmetic operations."""


def add(a, b):
    """Add two numbers and return the result."""
    return a + b


def subtract(a, b):
    """Subtract b from a and return the result."""
    return a - b


def multiply(a, b):
    """Multiply two numbers and return the result."""
    return a * b


def divide(a, b):
    """Divide a by b and return the result.
    
    Raises:
        ValueError: If attempting to divide by zero.
    """
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


def main():
    """Interactive calculator loop."""
    print("Simple Calculator")
    print("-" * 40)
    print("Operations: add, subtract, multiply, divide")
    print("Type 'quit' to exit")
    print("-" * 40)
    
    while True:
        operation = input("\nEnter operation (add/subtract/multiply/divide) or 'quit': ").strip().lower()
        
        if operation == "quit":
            print("Goodbye!")
            break
        
        if operation not in ["add", "subtract", "multiply", "divide"]:
            print("Invalid operation. Please choose: add, subtract, multiply, or divide")
            continue
        
        try:
            a = float(input("Enter first number: "))
            b = float(input("Enter second number: "))
        except ValueError:
            print("Invalid input. Please enter valid numbers.")
            continue
        
        try:
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

def calculate_velocity(distance: float, time: float) -> float:
    if time <= 0:
        raise ValueError("Time must be greater than zero")
    return distance / time

if __name__ == "__main__":
    main()
