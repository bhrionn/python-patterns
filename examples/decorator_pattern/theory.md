# Decorator Pattern

## Overview

The Decorator Pattern is a structural design pattern that allows you to dynamically add new functionality to objects without altering their structure. It provides a flexible alternative to subclassing for extending functionality by wrapping objects with decorator objects that add new behaviors.

## Intent

- Attach additional responsibilities to an object dynamically
- Provide a flexible alternative to subclassing for extending functionality
- Add behavior to individual objects without affecting other objects of the same class
- Compose behaviors by stacking multiple decorators
- Follow the Open/Closed Principle (open for extension, closed for modification)

## Problem

Consider a notification system that can send messages via different channels. You might need to add features like:

- Logging when notifications are sent
- Encrypting message content
- Compressing large messages
- Adding timestamps
- Validating message format

Without the Decorator pattern, you might face several issues:

```python
# Class explosion with inheritance
class Notification:
    def send(self, message): pass

class LoggedNotification(Notification): pass
class EncryptedNotification(Notification): pass
class CompressedNotification(Notification): pass
class LoggedEncryptedNotification(Notification): pass
class LoggedCompressedNotification(Notification): pass
class EncryptedCompressedNotification(Notification): pass
class LoggedEncryptedCompressedNotification(Notification): pass
# Combinatorial explosion of classes!
```

Problems with this approach:
- **Class explosion**: Need a class for every combination
- **Inflexible**: Can't add/remove behaviors at runtime
- **Code duplication**: Similar code across many classes
- **Difficult maintenance**: Changes require modifying multiple classes

## Solution

The Decorator Pattern wraps objects with decorator objects that add new behaviors. Decorators implement the same interface as the wrapped object, so they can be stacked and composed at runtime.

### Key Components

1. **Component Interface**: Defines the interface for objects that can have responsibilities added
2. **Concrete Component**: The original object to which additional responsibilities can be attached
3. **Decorator Base Class**: Maintains a reference to a Component object and implements the Component interface
4. **Concrete Decorators**: Add specific responsibilities to the component

## Benefits

- **Single Responsibility**: Each decorator has one job
- **Open/Closed Principle**: Add new decorators without modifying existing code
- **Flexible composition**: Combine behaviors dynamically at runtime
- **Transparent to client**: Decorators and components share the same interface
- **Alternative to subclassing**: More flexible than inheritance
- **Runtime behavior modification**: Add/remove responsibilities dynamically
- **Multiple decorations**: Stack decorators for complex behavior

## When to Use

- When you need to add responsibilities to objects dynamically and transparently
- When extension by subclassing is impractical (class explosion)
- When you want to add responsibilities that can be withdrawn
- When you need to add behavior to individual objects, not entire classes
- When you need to combine multiple behaviors
- When subclassing would result in too many classes
- When you want to add cross-cutting concerns (logging, caching, validation)

## Python-Specific Considerations

Python has native decorator syntax that works differently from the classic OOP decorator pattern:

### Function Decorators
Python's `@decorator` syntax for wrapping functions:
```python
@log_calls
def process_data(data):
    return data
```

### Class Decorators
Decorators that modify or wrap entire classes:
```python
@dataclass
class User:
    name: str
```

### Classic OOP Decorators
Traditional decorator pattern with wrapper classes (what this example demonstrates)

### Key Python Features
- **functools.wraps**: Preserve metadata when decorating functions
- **First-class functions**: Functions are objects that can be passed around
- **`__call__`**: Make classes callable to act as decorators
- **Context managers**: Can combine with decorators for resource management
- **Descriptors**: Advanced decoration at the attribute level

## Implementation Approaches

### 1. Classic Object Decorator
Wrapper classes that implement the same interface as the component.

### 2. Function Decorator
Python's native `@decorator` syntax for wrapping functions.

### 3. Class Decorator
Decorators that wrap or modify entire classes.

### 4. Parameterized Decorator
Decorators that accept arguments for configuration.

### 5. Decorator with State
Decorators that maintain state between calls.

## Comparison with Other Patterns

- **Adapter**: Changes interface; decorator keeps same interface
- **Proxy**: Controls access; decorator adds responsibilities
- **Composite**: Aggregates objects; decorator wraps single object
- **Strategy**: Changes algorithm; decorator adds behavior
- **Chain of Responsibility**: Passes request along chain; decorator wraps object

## Example Use Cases

- **Logging**: Add logging to method calls
- **Caching/Memoization**: Cache function results
- **Authentication/Authorization**: Add security checks
- **Validation**: Validate inputs before processing
- **Performance Monitoring**: Measure execution time
- **Error Handling**: Add try-catch wrappers
- **Transaction Management**: Add database transaction support
- **Encryption/Compression**: Transform data
- **Rate Limiting**: Throttle requests
- **Retry Logic**: Automatically retry failed operations
- **UI Components**: Add scrollbars, borders, shadows to widgets

## Anti-Patterns to Avoid

- **Over-decoration**: Too many decorator layers become hard to debug
- **Breaking interface**: Decorators must maintain the component's interface
- **Order dependency**: Decorator order shouldn't matter (when possible)
- **Stateful decorators**: Can lead to unexpected behavior
- **Hidden dependencies**: Decorators should be independent
- **Performance overhead**: Too many layers can impact performance
- **Decorator confusion**: Mixing Python function decorators with OOP decorators

## Implementation Variations

### 1. Transparent Decorator
Decorator that's completely invisible to clients.

### 2. Semi-Transparent Decorator
Adds methods beyond the component interface.

### 3. Decorator with Multiple Components
Decorator that wraps multiple objects.

### 4. Chained Decorators
Multiple decorators stacked together.

### 5. Conditional Decorator
Decorator that conditionally applies behavior.

## Python Implementation Patterns

### Classic OOP Decorator
```python
class Component(ABC):
    @abstractmethod
    def operation(self): pass

class ConcreteComponent(Component):
    def operation(self):
        return "Base"

class Decorator(Component):
    def __init__(self, component: Component):
        self._component = component

    def operation(self):
        return self._component.operation()

class ConcreteDecorator(Decorator):
    def operation(self):
        return f"Decorated({self._component.operation()})"
```

### Function Decorator
```python
def log_calls(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

@log_calls
def process(data):
    return data
```

### Parameterized Decorator
```python
def retry(max_attempts=3):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    if attempt == max_attempts - 1:
                        raise
        return wrapper
    return decorator

@retry(max_attempts=5)
def unreliable_operation():
    pass
```

### Class-Based Decorator
```python
class Memoize:
    def __init__(self, func):
        self.func = func
        self.cache = {}

    def __call__(self, *args):
        if args not in self.cache:
            self.cache[args] = self.func(*args)
        return self.cache[args]

@Memoize
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
```

## Testing Considerations

Decorator patterns are highly testable:

- **Test Component Alone**: Verify base functionality works
- **Test Each Decorator**: Test decorators with mock components
- **Test Combinations**: Verify multiple decorators work together
- **Test Order Independence**: Ensure decorator order doesn't break functionality
- **Test Edge Cases**: Empty decorators, null components, etc.
- **Mock Decorators**: Replace decorators in tests when needed

## Best Practices

- **Same Interface**: Decorators must implement the component's interface
- **Composability**: Design decorators to work together
- **Independence**: Each decorator should be self-contained
- **Transparency**: Decorators shouldn't be visible to clients
- **Single Responsibility**: Each decorator adds one feature
- **Immutability Consideration**: Consider whether to modify or create new objects
- **Documentation**: Clearly document what each decorator adds
- **Performance**: Be aware of decorator stacking overhead
- **functools.wraps**: Always use when decorating functions

## Advanced Patterns

### Decorator + Factory
Use factory to create decorated objects based on configuration.

### Decorator + Strategy
Combine decorators with strategy for flexible behavior.

### Decorator + Template Method
Use template method within decorators for common structure.

### Decorator + Composite
Decorate composite objects for tree-wide behavior.

### Decorator + Proxy
Combine decoration with access control.

## Real-World Examples

### Python Built-in Decorators
- `@property`: Add getter/setter behavior
- `@staticmethod`: Modify method binding
- `@classmethod`: Change method type
- `@functools.lru_cache`: Add memoization
- `@dataclass`: Add boilerplate methods

### Web Frameworks
- Flask/FastAPI route decorators: `@app.route('/')`
- Authentication decorators: `@login_required`
- Permission decorators: `@permission_required`

### Testing Frameworks
- `@pytest.fixture`: Create test fixtures
- `@pytest.mark.parametrize`: Parameterize tests
- `@unittest.mock.patch`: Mock objects

### Django
- `@csrf_exempt`: Disable CSRF protection
- `@require_http_methods`: Restrict HTTP methods
- `@cache_page`: Cache view results

## Performance Considerations

- **Call Overhead**: Each decorator adds a function call
- **Memory Overhead**: Decorators create wrapper objects
- **Stacking Limit**: Too many decorators can impact performance
- **Caching**: Cache decorated results when appropriate
- **Lazy Decoration**: Delay decoration until needed
- **Profile First**: Measure before optimizing decorator overhead

## Migration to Decorator Pattern

When refactoring existing code:

1. Identify cross-cutting concerns (logging, validation, caching)
2. Define component interface
3. Extract core functionality to concrete component
4. Create decorator base class
5. Implement concrete decorators for each concern
6. Replace conditional logic with decorator composition
7. Test each decorator independently
8. Compose decorators at runtime as needed

## Common Pitfalls

- **Forgetting to call wrapped method**: Always delegate to component
- **Breaking the interface**: Decorators must maintain interface
- **Decorator order matters**: Be explicit about order requirements
- **Not using functools.wraps**: Loses function metadata
- **Too many decorators**: Makes debugging difficult
- **Tight coupling**: Decorators depending on other decorators
- **Mutating wrapped object**: Can cause unexpected side effects

## Decorator vs Inheritance

**Use Inheritance when:**
- Relationship is truly "is-a"
- Behavior is permanent and fundamental
- Limited number of variations
- Compile-time binding is needed

**Use Decorator when:**
- Behavior can be added/removed dynamically
- Multiple optional behaviors need to be combined
- Avoiding class explosion
- Runtime binding is needed
- Behavior is cross-cutting concern

## Function Decorators Best Practices

When writing Python function decorators:

```python
import functools

def my_decorator(func):
    """
    Decorator that does something useful.

    Args:
        func: Function to decorate

    Returns:
        Decorated function
    """
    @functools.wraps(func)  # Preserves metadata
    def wrapper(*args, **kwargs):
        # Pre-processing
        result = func(*args, **kwargs)
        # Post-processing
        return result
    return wrapper
```

- Always use `@functools.wraps`
- Document what the decorator does
- Support `*args` and `**kwargs` for flexibility
- Consider making decorators parameterizable
- Handle exceptions appropriately
- Preserve function signature when possible

## Stacking Decorators

When using multiple decorators:

```python
@decorator1
@decorator2
@decorator3
def function():
    pass

# Equivalent to:
# function = decorator1(decorator2(decorator3(function)))
```

- Innermost decorator is applied first
- Order can matter for some decorators
- Document required ordering
- Consider decorator independence
- Test different orderings

## Decorator with Context

Decorators can maintain context:

```python
class CountCalls:
    def __init__(self, func):
        self.func = func
        self.count = 0

    def __call__(self, *args, **kwargs):
        self.count += 1
        print(f"Call {self.count}")
        return self.func(*args, **kwargs)
```

- Useful for stateful decorators
- Can track metrics, rate limiting
- Be aware of thread safety
- Consider when state should reset
