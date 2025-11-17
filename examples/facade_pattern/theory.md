# Facade Pattern

## Overview

The Facade Pattern is a structural design pattern that provides a simplified, unified interface to a complex subsystem. It wraps multiple complex components with a single class that provides a cleaner, more convenient API for common tasks while still allowing direct access to subsystem components when needed.

## Intent

- Provide a simplified interface to a complex subsystem
- Reduce coupling between clients and subsystem components
- Hide complexity from clients
- Define a higher-level interface that makes the subsystem easier to use
- Organize subsystems into layers

## Problem

Consider a home theater system with many components:

```python
# Without Facade - client must manage all components
dvd_player = DVDPlayer()
projector = Projector()
screen = Screen()
amplifier = Amplifier()
lights = Lights()

# To watch a movie, client needs to:
lights.dim(10)
screen.down()
projector.on()
projector.set_input(dvd_player)
amplifier.on()
amplifier.set_dvd(dvd_player)
amplifier.set_volume(5)
dvd_player.on()
dvd_player.play(movie)
```

This approach has problems:
- Clients must understand complex subsystem interactions
- Changes to subsystem require updating all client code
- Difficult to use correctly (easy to forget steps or wrong order)
- High coupling between clients and subsystem components
- Complex initialization sequences repeated everywhere

## Solution

The Facade Pattern creates a facade class that provides simple methods encapsulating complex subsystem interactions:

```python
home_theater = HomeTheaterFacade(dvd_player, projector, screen, amplifier, lights)
home_theater.watch_movie(movie)  # Simple!
```

### Key Components

1. **Facade**: Provides simplified methods that delegate to subsystem components
2. **Subsystem Classes**: Complex components that do the actual work
3. **Client**: Uses the facade instead of subsystem components directly

## Benefits

- **Simplified Interface**: Easier to use than working with subsystem directly
- **Loose Coupling**: Clients depend on facade, not subsystem components
- **Layered Architecture**: Helps organize complex systems into layers
- **Flexibility**: Clients can still access subsystem components if needed
- **Single Responsibility**: Facade handles coordination, subsystems handle specifics
- **Maintainability**: Changes to subsystem internals don't affect clients

## When to Use

- When you want to provide a simple interface to a complex subsystem
- When there are many dependencies between clients and implementation classes
- When you want to layer your subsystem (facade for each layer)
- When you want to decouple client code from subsystem components
- When you need to wrap a poorly designed or legacy API
- When you want to provide different levels of abstraction

## Python-Specific Considerations

Python's dynamic nature makes facades particularly elegant:

- **Duck Typing**: No need for formal interfaces
- **Default Arguments**: Simplify method signatures with sensible defaults
- **Context Managers**: Use `__enter__`/`__exit__` for resource management
- **Properties**: Expose simple properties that hide complex operations
- **Decorators**: Add cross-cutting concerns to facade methods

### Context Manager Facade

```python
class DatabaseFacade:
    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

# Usage
with DatabaseFacade() as db:
    db.execute_query("SELECT * FROM users")
```

## Implementation Approaches

### 1. Basic Facade
Simple class with methods delegating to subsystem.

### 2. Configurable Facade
Facade with configuration options for customization.

### 3. Layered Facades
Multiple facades providing different abstraction levels.

### 4. Singleton Facade
Single facade instance managing shared resources.

## Comparison with Other Patterns

- **Adapter**: Changes interface of single class vs simplifying multiple classes
- **Proxy**: Same interface with additional behavior vs simplified interface
- **Mediator**: Components know about mediator vs components unaware of facade
- **Abstract Factory**: Creates objects vs provides interface to existing objects
- **Decorator**: Adds behavior dynamically vs provides simpler interface

## Example Use Cases

- **Home Automation**: Facade for controlling multiple smart devices
- **Database Access**: Simplify complex database operations
- **Compiler**: Facade for lexer, parser, code generator
- **Web Frameworks**: Request facade hiding HTTP parsing, routing, etc.
- **E-commerce Checkout**: Facade for payment, inventory, shipping systems
- **Multimedia Libraries**: Simplify audio/video encoding/decoding
- **Operating System APIs**: High-level facade over low-level system calls
- **Third-Party Libraries**: Wrap complex libraries with simpler interface

## Anti-Patterns to Avoid

- **God Object**: Don't make facade too large or handle too much
- **Breaking Encapsulation**: Don't expose subsystem internals unnecessarily
- **Tight Coupling**: Facade shouldn't know about client-specific logic
- **Bypassing Facade**: Don't let clients bypass facade and access subsystem directly (unless intentional)
- **Too Many Facades**: Don't create facades for every small subsystem
- **Leaky Abstraction**: Don't let subsystem complexity leak through facade

## Implementation Variations

### 1. Simple Facade
Basic facade with straightforward delegation.

### 2. Facade with Defaults
Provides sensible defaults to simplify common cases.

### 3. Fluent Facade
Chainable methods for fluent interface.

### 4. Facade Registry
Multiple facades registered for different subsystems.

### 5. Adaptive Facade
Facade that adapts based on configuration or runtime conditions.

## Python Implementation Patterns

### Basic Facade

```python
class Facade:
    def __init__(self):
        self._subsystem1 = Subsystem1()
        self._subsystem2 = Subsystem2()

    def operation(self):
        self._subsystem1.operation1()
        self._subsystem2.operation2()
```

### Context Manager Facade

```python
class Facade:
    def __enter__(self):
        self._setup()
        return self

    def __exit__(self, *args):
        self._teardown()
```

### Property-Based Facade

```python
class Facade:
    @property
    def status(self):
        # Hide complex status computation
        return self._compute_complex_status()
```

### Fluent Facade

```python
class Facade:
    def operation1(self):
        # Do work
        return self

    def operation2(self):
        # Do work
        return self

# Usage: facade.operation1().operation2()
```

## Testing Considerations

Facades improve testability:

- **Mock Subsystems**: Easy to mock subsystem components
- **Test Facade Interface**: Test facade without testing subsystems
- **Integration Tests**: Use facade in integration tests
- **Stub Subsystems**: Replace complex subsystems with stubs
- **Isolation**: Test clients in isolation from subsystem complexity

## Best Practices

- **Keep It Simple**: Facade should simplify, not add complexity
- **Sensible Defaults**: Provide defaults for common use cases
- **Progressive Disclosure**: Simple methods for common cases, advanced methods when needed
- **Clear Naming**: Method names should clearly indicate what they do
- **Document Subsystem Access**: If direct access allowed, document when/why
- **Error Handling**: Handle subsystem errors gracefully
- **Stateless When Possible**: Prefer stateless facades for simplicity
- **Composition Over Inheritance**: Facades should compose subsystems, not inherit

## Advanced Patterns

### Facade + Factory
Factory creates appropriate facade for different contexts.

### Facade + Singleton
Single facade instance managing shared resources (connection pools, etc.).

### Facade + Strategy
Facade uses different strategies for different operations.

### Facade + Template Method
Facade methods follow template method pattern for consistency.

## Real-World Examples

### Web Framework Request Handling
Flask/Django request objects facade over HTTP parsing, headers, cookies, etc.

### Database ORMs
SQLAlchemy facades over SQL generation, connection management, result parsing.

### Multimedia Processing
FFmpeg library facades provide simple API over complex video/audio processing.

### Cloud SDKs
AWS boto3 facades simplify complex API calls to cloud services.

## Performance Considerations

- **Lazy Initialization**: Create subsystem components only when needed
- **Caching**: Cache expensive subsystem results
- **Resource Pooling**: Pool expensive resources (connections, threads)
- **Batch Operations**: Combine multiple subsystem calls into batches
- **Async Operations**: Use async/await for I/O-bound subsystem operations

## Layering with Facades

Facades work well in layered architectures:

```
Presentation Layer
    ↓
Business Facade ← Client uses this
    ↓
Service Layer (complex subsystems)
    ↓
Data Access Layer
```

Each layer can have its own facade providing appropriate abstraction level.

## Migration to Facade Pattern

When refactoring existing code:

1. Identify complex subsystem interactions in client code
2. Create facade class
3. Move subsystem initialization to facade
4. Extract common operation sequences into facade methods
5. Update clients to use facade instead of subsystem directly
6. Optionally keep subsystem accessible for advanced use cases
7. Test that facade simplifies client code
8. Document facade API and usage examples

## Facade vs Direct Access

**Use Facade When:**
- Performing common, repetitive tasks
- You want simple, intuitive API
- You're okay with less control/flexibility

**Use Direct Subsystem Access When:**
- Need fine-grained control
- Performing unusual operations
- Optimizing specific use case
- Facade doesn't provide needed functionality
