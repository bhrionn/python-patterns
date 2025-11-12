# Strategy Pattern

## Overview

The Strategy Pattern is a behavioral design pattern that defines a family of algorithms, encapsulates each one, and makes them interchangeable. It lets the algorithm vary independently from clients that use it, enabling runtime selection of different behaviors.

## Intent

- Define a family of algorithms
- Encapsulate each algorithm
- Make algorithms interchangeable
- Allow clients to choose algorithm implementation at runtime

## Problem

Consider a navigation application that can calculate routes using different methods:

- Fastest route (prioritizing speed)
- Shortest route (prioritizing distance)
- Scenic route (prioritizing attractions)

Without the Strategy pattern, you might have conditional logic scattered throughout the code:

```python
class Navigator:
    def __init__(self, route_type: str):
        self.route_type = route_type

    def calculate_route(self, start, end):
        if self.route_type == "fastest":
            # Complex fastest route logic
            return fastest_route(start, end)
        elif self.route_type == "shortest":
            # Complex shortest route logic
            return shortest_route(start, end)
        elif self.route_type == "scenic":
            # Complex scenic route logic
            return scenic_route(start, end)
```

This violates Open/Closed Principle - adding new route types requires modifying existing code.

## Solution

The Strategy Pattern defines a common interface for all algorithms and encapsulates each algorithm in a separate class. The context (Navigator) maintains a reference to a strategy object and delegates work to it.

### Key Components

1. **Strategy Interface**: Defines the common interface for all concrete strategies
2. **Concrete Strategies**: Implement the algorithm defined by the Strategy interface
3. **Context**: Maintains a reference to a Strategy object and delegates algorithm execution

## Benefits

- **Open/Closed Principle**: New strategies can be added without modifying existing code
- **Single Responsibility**: Each strategy has one job
- **Runtime Flexibility**: Strategies can be swapped at runtime
- **Testability**: Each strategy can be tested independently
- **Composition over Inheritance**: Behavior defined through composition

## When to Use

- When you have multiple ways to do the same thing
- When you need to switch between algorithms at runtime
- When you want to isolate algorithm implementation from client code
- When you have conditional logic that selects different behaviors
- When you want to make algorithm selection configurable

## Python-Specific Considerations

Python's duck typing makes Strategy Pattern particularly elegant:

- **No need for abstract base classes**: Any object with the right methods works
- **Functions as strategies**: Use functions directly as strategies
- **Callable objects**: Classes with `__call__` method can be strategies
- **Lambda functions**: Simple strategies can be lambdas
- **Method references**: Bind methods as strategies

## Implementation Approaches

### 1. Interface-Based Strategy
Using abstract base classes or protocols.

### 2. Function-Based Strategy
Using functions directly as strategies.

### 3. Callable Class Strategy
Using classes with `__call__` method.

### 4. Method Strategy
Using bound methods as strategies.

## Comparison with Other Patterns

- **Template Method**: Defines skeleton of algorithm, subclasses override steps
- **State**: Changes behavior based on internal state
- **Command**: Encapsulates requests as objects
- **Factory**: Creates objects, doesn't define behavior
- **Decorator**: Adds behavior dynamically

## Example Use Cases

- **Sorting Algorithms**: Different sorting strategies (quick, merge, bubble)
- **Payment Processing**: Different payment methods (credit card, PayPal, crypto)
- **Compression**: Different compression algorithms (gzip, zip, rar)
- **Image Processing**: Different filters (blur, sharpen, contrast)
- **Validation**: Different validation strategies (strict, lenient, custom)
- **Caching**: Different cache strategies (LRU, LFU, FIFO)

## Anti-Patterns to Avoid

- **Over-Engineering**: Don't use Strategy for simple conditionals
- **Too Many Strategies**: Keep strategy count manageable
- **Strategy Bloat**: Each strategy should be substantial enough to justify separation
- **Tight Coupling**: Strategies should not depend on context internals
- **Shared State**: Strategies should be stateless or manage their own state

## Implementation Variations

### 1. Simple Strategy
Basic interface-based implementation.

### 2. Strategy with Context Data
Strategies receive context data for decision making.

### 3. Chain of Strategies
Strategies can be chained together.

### 4. Strategy Factory
Factory for creating appropriate strategies.

### 5. Parameterized Strategy
Strategies accept parameters for customization.

## Python Implementation Patterns

### Using ABC
```python
from abc import ABC, abstractmethod

class Strategy(ABC):
    @abstractmethod
    def execute(self, data):
        pass

class ConcreteStrategy(Strategy):
    def execute(self, data):
        # Implementation
        pass
```

### Using Protocols (Python 3.8+)
```python
from typing import Protocol

class Strategy(Protocol):
    def execute(self, data) -> Any:
        ...
```

### Function-Based
```python
def strategy_function(data):
    # Implementation
    return result

# Usage
context = Context(strategy_function)
```

### Callable Classes
```python
class Strategy:
    def __init__(self, param):
        self.param = param

    def __call__(self, data):
        # Implementation using self.param
        return result
```

## Testing Considerations

Strategy patterns are highly testable:

- **Unit Test Strategies**: Test each strategy independently
- **Mock Strategies**: Easy to mock for testing context
- **Strategy Injection**: Inject test strategies for isolation
- **Parameter Variation**: Test strategies with different parameters

## Best Practices

- **Strategy Interface**: Keep it simple and focused
- **Strategy Naming**: Use descriptive names (SortByName, SortByDate)
- **Strategy Scope**: Each strategy should have clear responsibility
- **Context Simplicity**: Context should only orchestrate, not implement logic
- **Dependency Injection**: Inject strategies rather than hardcoding
- **Immutability**: Prefer stateless strategies when possible
- **Error Handling**: Strategies should handle their own errors appropriately

## Advanced Patterns

### Strategy + Factory
Combine with Factory to create strategies based on configuration.

### Strategy + Template Method
Use Template Method within strategies for common algorithm structure.

### Strategy + Decorator
Decorate strategies to add cross-cutting concerns.

### Strategy + State
Strategies can change based on state.

## Real-World Examples

### Web Framework Middleware
Different authentication strategies (JWT, OAuth, Basic Auth).

### E-commerce Pricing
Different pricing strategies (fixed, percentage discount, buy-one-get-one).

### Logging
Different logging strategies (console, file, remote service).

### Data Validation
Different validation strategies (email, phone, credit card).

## Performance Considerations

- **Strategy Selection**: Minimize overhead of choosing strategies
- **Strategy Caching**: Cache expensive strategy objects if appropriate
- **Lazy Loading**: Load strategies only when needed
- **Memory Usage**: Consider memory implications of multiple strategy objects

## Migration to Strategy Pattern

When refactoring existing code:

1. Identify conditional logic selecting algorithms
2. Extract algorithms into separate strategy classes
3. Define common interface for strategies
4. Create context class to use strategies
5. Replace conditional with strategy injection
6. Test each strategy independently