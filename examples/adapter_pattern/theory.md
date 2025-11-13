# Adapter Pattern

## Overview

The Adapter Pattern is a structural design pattern that allows objects with incompatible interfaces to collaborate. It acts as a bridge between two incompatible interfaces by wrapping an existing class with a new interface, making it compatible with the client's expectations.

## Intent

- Convert the interface of a class into another interface clients expect
- Allow classes with incompatible interfaces to work together
- Wrap an existing class with a new interface
- Enable reuse of existing functionality in new contexts

## Problem

Consider a media player application that needs to play various audio and video formats. Your application has a simple interface for playing media, but you need to integrate:

- A third-party advanced media library with a completely different interface
- A legacy audio system with outdated method signatures
- Multiple external services that don't conform to your interface

Without the Adapter pattern, you would have to modify your client code or the external libraries:

```python
class MediaPlayer:
    def play(self, filename: str):
        if isinstance(self.library, AdvancedMediaLibrary):
            # Call different methods
            self.library.load_file(filename)
            self.library.start_playback()
        elif isinstance(self.library, LegacyAudioSystem):
            # Call yet different methods
            self.library.open_audio_file(filename)
            self.library.begin_audio()
        # More conditionals for each library...
```

This violates the Open/Closed Principle and creates tight coupling.

## Solution

The Adapter Pattern wraps the incompatible class (adaptee) and provides an interface that the client expects. The adapter translates calls from the target interface to the adaptee's interface.

### Key Components

1. **Target Interface**: The interface expected by the client
2. **Adaptee**: The existing class with an incompatible interface
3. **Adapter**: Wraps the adaptee and implements the target interface
4. **Client**: Works with objects through the target interface

## Benefits

- **Open/Closed Principle**: Add new adapters without modifying existing code
- **Single Responsibility**: Adapters handle interface conversion separately
- **Reusability**: Use existing classes with incompatible interfaces
- **Flexibility**: Integrate third-party libraries without modification
- **Decoupling**: Client code is independent of concrete implementations
- **Legacy Integration**: Bridge old and new systems

## When to Use

- When you want to use an existing class but its interface doesn't match what you need
- When integrating third-party libraries with incompatible interfaces
- When working with legacy code that can't be modified
- When you need to create a reusable class that cooperates with unrelated classes
- When you need multiple incompatible implementations to work with the same client
- When converting data formats or protocols between systems

## Python-Specific Considerations

Python's duck typing provides unique advantages for the Adapter pattern:

- **No strict interfaces required**: Any object with the right methods works
- **Protocol classes**: Use `typing.Protocol` for structural subtyping
- **Multiple inheritance**: Can inherit from both target and adaptee if beneficial
- **Dynamic attributes**: Can add methods dynamically if needed
- **`__getattr__`**: Delegate attribute access to adaptee automatically
- **Composition preferred**: Favor composition over inheritance for clarity

## Implementation Approaches

### 1. Object Adapter (Composition)
Uses composition to hold a reference to the adaptee. Preferred in Python.

### 2. Class Adapter (Inheritance)
Uses multiple inheritance to adapt the interface. Less common in Python.

### 3. Two-Way Adapter
Adapter that can work with both interfaces bidirectionally.

### 4. Pluggable Adapter
Generic adapter that can work with multiple adaptees through configuration.

## Comparison with Other Patterns

- **Bridge**: Separates abstraction from implementation (designed upfront)
- **Decorator**: Adds responsibilities without changing interface
- **Facade**: Simplifies a complex interface (different intent)
- **Proxy**: Same interface, controls access to object
- **Strategy**: Changes algorithm behavior, not interface

## Example Use Cases

- **API Integration**: Adapt REST API to your internal data model
- **Database Adapters**: Make different databases work with same interface (SQLite, PostgreSQL, MongoDB)
- **Media Players**: Adapt different media codecs and formats
- **Payment Gateways**: Unify different payment provider APIs
- **Authentication**: Adapt different auth mechanisms (OAuth, SAML, LDAP)
- **File Systems**: Abstract different storage backends (local, S3, FTP)
- **Protocol Conversion**: Convert between HTTP, WebSocket, gRPC
- **Unit Conversion**: Adapt between different measurement systems

## Anti-Patterns to Avoid

- **Over-Adaptation**: Don't adapt when you can modify the source code
- **Leaky Abstraction**: Don't expose adaptee's methods through adapter
- **God Adapter**: Keep adapters focused on single adaptee
- **Unnecessary Adapters**: Don't create adapters for already compatible interfaces
- **Complex Translation Logic**: Keep adapter simple; move complex logic elsewhere
- **Stateful Adapters**: Prefer stateless adapters when possible

## Implementation Variations

### 1. Simple Adapter
Basic wrapper that translates method calls.

### 2. Caching Adapter
Adds caching to adaptee's operations.

### 3. Logging Adapter
Adds logging to adaptee's method calls.

### 4. Error-Handling Adapter
Translates adaptee's exceptions to expected types.

### 5. Bidirectional Adapter
Works with both target and adaptee interfaces.

## Python Implementation Patterns

### Using Composition (Recommended)
```python
class Adapter:
    def __init__(self, adaptee: Adaptee):
        self._adaptee = adaptee

    def target_method(self):
        # Translate to adaptee's interface
        return self._adaptee.specific_method()
```

### Using Protocol for Duck Typing
```python
from typing import Protocol

class TargetInterface(Protocol):
    def target_method(self) -> str:
        ...

class Adapter:
    def __init__(self, adaptee):
        self._adaptee = adaptee

    def target_method(self) -> str:
        return self._adaptee.different_method()
```

### Using `__getattr__` for Delegation
```python
class Adapter:
    def __init__(self, adaptee):
        self._adaptee = adaptee

    def __getattr__(self, name):
        # Delegate unknown attributes to adaptee
        return getattr(self._adaptee, name)

    def target_method(self):
        # Only override methods that need adaptation
        return self._adaptee.specific_method()
```

## Testing Considerations

Adapter patterns are highly testable:

- **Mock Adaptees**: Easy to create test doubles for adaptees
- **Interface Testing**: Test that adapter conforms to target interface
- **Translation Testing**: Verify correct method translation
- **Isolation Testing**: Test adapter independently from adaptee
- **Integration Testing**: Test adapter with real adaptee

## Best Practices

- **Composition over Inheritance**: Prefer object adapters (composition)
- **Single Adaptee**: One adapter per adaptee class
- **Minimal Interface**: Only adapt methods that client needs
- **No Business Logic**: Keep adapters simple, no business rules
- **Clear Naming**: Name adapters descriptively (e.g., `LegacyAudioAdapter`)
- **Type Hints**: Use protocols for target interface
- **Documentation**: Document what each adapter adapts and why
- **Error Translation**: Convert adaptee exceptions to expected types

## Advanced Patterns

### Adapter + Factory
Use factory to create appropriate adapter based on configuration.

### Adapter + Strategy
Combine adapters with strategy for flexible algorithm selection.

### Adapter + Decorator
Layer decorators on top of adapters for additional functionality.

### Adapter + Proxy
Combine with proxy for remote or lazy-loaded adaptees.

## Real-World Examples

### Database Adapters
Django ORM adapts different SQL databases to unified interface.

### Web Frameworks
WSGI adapters connect different web servers to Python web applications.

### Testing Frameworks
Mock adapters provide test doubles for external services.

### Cloud Services
Cloud provider adapters unify AWS, Azure, and GCP interfaces.

## Performance Considerations

- **Minimal Overhead**: Adapters should add negligible performance cost
- **Lazy Initialization**: Create adaptee only when needed
- **Caching**: Cache expensive adaptee operations if appropriate
- **Pass-Through**: Directly delegate when no translation needed
- **Avoid Deep Nesting**: Don't chain multiple adapters unnecessarily

## Migration to Adapter Pattern

When refactoring existing code:

1. Identify incompatible interfaces in your codebase
2. Define the target interface your client expects
3. Create adapter classes for each incompatible interface
4. Inject adapters into client code
5. Remove conditional logic based on types
6. Test each adapter independently
7. Update client code to use target interface only

## Common Pitfalls

- **Forgetting to delegate**: Ensure all required methods are adapted
- **Exposing adaptee**: Don't leak adaptee's interface through adapter
- **Complex adapters**: Keep translation logic simple and focused
- **Type checking in client**: Client shouldn't know about adapters
- **Modifying adaptee**: Never modify the adaptee through adapter

## Adapter vs Wrapper

The Adapter pattern is sometimes called a "wrapper," but not all wrappers are adapters:

- **Adapter**: Changes interface to match client expectations
- **Decorator**: Same interface, adds functionality
- **Facade**: Simplifies complex subsystem
- **Proxy**: Same interface, controls access

Choose Adapter when the primary goal is interface compatibility.
