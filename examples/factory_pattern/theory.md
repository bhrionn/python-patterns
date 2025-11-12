# Factory Pattern

## Overview

The Factory Pattern is a creational design pattern that provides an interface for creating objects in a superclass, but allows subclasses to alter the type of objects that will be created. It encapsulates object creation logic, making the code more flexible and easier to extend.

## Intent

- Define an interface for creating an object, but let subclasses decide which class to instantiate.
- Factory Method lets a class defer instantiation to subclasses.

## Problem

Imagine you're building a logistics management application that needs to handle different types of transportation: trucks, ships, and planes. The initial code might look like this:

```python
class LogisticsApp:
    def __init__(self, transport_type: str):
        self.transport_type = transport_type

    def plan_delivery(self):
        if self.transport_type == "truck":
            transport = Truck()
        elif self.transport_type == "ship":
            transport = Ship()
        elif self.transport_type == "plane":
            transport = Plane()
        else:
            raise ValueError("Unknown transport type")
        # Use transport...
```

This approach violates the Open/Closed Principle. If you need to add a new transport type, you have to modify the existing code.

## Solution

The Factory Pattern solves this by introducing a separate method for object creation. Instead of calling the constructor directly, you call a factory method that returns the appropriate object.

### Key Components

1. **Product Interface**: Defines the interface for objects the factory method creates.
2. **Concrete Products**: Implement the Product interface.
3. **Creator**: Declares the factory method that returns objects of Product type.
4. **Concrete Creators**: Override the factory method to return instances of Concrete Products.

## Benefits

- **Loose Coupling**: Client code doesn't need to know the specifics of object creation.
- **Extensibility**: Easy to add new product types without modifying existing code.
- **Centralized Creation Logic**: Object creation is handled in one place.
- **Adherence to SOLID**: Follows Open/Closed Principle and Single Responsibility Principle.

## When to Use

- When object creation logic is complex or likely to change
- When you want to centralize object creation
- When you need to support multiple similar objects with different creation logic
- When you want to decouple client code from concrete classes

## Python-Specific Considerations

In Python, the Factory Pattern can be implemented using:

- Functions as factories
- Classes with factory methods
- Abstract base classes
- Type hints and protocols

Python's dynamic nature makes factories particularly elegant, as you can return different types based on runtime conditions.

## Comparison with Other Patterns

- **Abstract Factory**: Creates families of related objects
- **Builder**: Constructs complex objects step by step
- **Prototype**: Creates objects by cloning existing instances
- **Singleton**: Ensures only one instance exists

## Example Use Cases

- UI component factories in GUI frameworks
- Database connection factories
- Logger factories
- Payment processor factories
- Shape factories in graphics libraries

## Anti-Patterns to Avoid

- Overusing factories for simple object creation
- Creating "God Factories" that handle too many different types
- Mixing factory logic with business logic

## Implementation Variations

1. **Simple Factory**: A function or class with a static method
2. **Factory Method**: Uses inheritance to decide object type
3. **Abstract Factory**: Creates families of related objects

## Testing Considerations

Factory patterns are highly testable because:
- You can mock the factory method
- Concrete products can be easily substituted
- Creation logic can be tested in isolation