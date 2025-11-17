# Proxy Pattern

## Overview

The Proxy Pattern is a structural design pattern that provides a surrogate or placeholder object to control access to another object. The proxy has the same interface as the real object and controls access by performing additional operations before or after forwarding requests to the real object.

## Intent

- Provide a surrogate or placeholder for another object
- Control access to the real object
- Add additional behavior without modifying the real object
- Lazy initialization (create expensive objects only when needed)
- Access control (restrict access based on permissions)
- Remote proxy (represent objects in different address spaces)
- Smart reference (additional actions when object is accessed)

## Problem

Consider an image viewer application that displays high-resolution images:

```python
class Image:
    def __init__(self, filename):
        self.filename = filename
        self.load_from_disk()  # Expensive operation!

    def display(self):
        print(f"Displaying {self.filename}")

# Problem: Loading all images immediately is slow
images = [Image("photo1.jpg"), Image("photo2.jpg"), Image("photo3.jpg")]
# All images loaded even if not displayed!
```

Problems without proxy:
- Expensive operations performed immediately (even if not needed)
- No control over access to the object
- Cannot add cross-cutting concerns (logging, caching, access control) without modifying original class
- Resource-intensive objects created unnecessarily

## Solution

The Proxy Pattern creates a proxy class that controls access to the real object:

```python
class ImageProxy:
    def __init__(self, filename):
        self.filename = filename
        self._real_image = None  # Not loaded yet!

    def display(self):
        if self._real_image is None:
            self._real_image = RealImage(self.filename)  # Lazy load
        self._real_image.display()

# Images only loaded when actually displayed
images = [ImageProxy("photo1.jpg"), ImageProxy("photo2.jpg")]
```

### Key Components

1. **Subject Interface**: Common interface for RealSubject and Proxy
2. **RealSubject**: The actual object that does real work
3. **Proxy**: Controls access to RealSubject, maintains reference to it

## Types of Proxies

### 1. Virtual Proxy (Lazy Loading)
Creates expensive objects only when needed.

### 2. Protection Proxy (Access Control)
Controls access based on permissions.

### 3. Remote Proxy
Represents objects in different address spaces (network, different process).

### 4. Smart Reference
Performs additional actions (reference counting, logging, caching).

### 5. Cache Proxy
Caches results to avoid repeated expensive operations.

### 6. Logging Proxy
Adds logging to method calls.

## Benefits

- **Lazy Initialization**: Defer expensive object creation
- **Access Control**: Restrict access to sensitive operations
- **Smart Reference**: Add reference counting, locking, etc.
- **Remote Access**: Transparently access remote objects
- **Performance**: Cache results, batch operations
- **Single Responsibility**: Proxy handles cross-cutting concerns
- **Open/Closed**: Add behavior without modifying real object

## When to Use

- When you need lazy initialization of expensive objects
- When you need to control access to an object
- When you need to perform actions before/after accessing an object
- When you need to represent remote objects locally
- When you need reference counting or garbage collection
- When you need to cache expensive operation results
- When you need to log or monitor object access

## Python-Specific Considerations

Python provides several mechanisms for implementing proxies:

### `__getattr__` and `__getattribute__`
Intercept attribute access.

```python
class Proxy:
    def __getattr__(self, name):
        # Forward to real object
        return getattr(self._real_object, name)
```

### Descriptors
Control attribute access at class level.

### Decorators
Wrap functions with proxy behavior.

### Context Managers
Manage resources with `__enter__`/`__exit__`.

### Property Decorators
Create smart properties with lazy loading.

```python
class Image:
    @property
    def data(self):
        if self._data is None:
            self._data = self._load()
        return self._data
```

## Implementation Approaches

### 1. Explicit Proxy
Proxy explicitly implements interface methods.

### 2. Delegation Proxy
Proxy uses `__getattr__` for automatic delegation.

### 3. Inheritance Proxy
Proxy inherits from real class (less common, tighter coupling).

### 4. Decorator-Based Proxy
Use decorators to wrap functions.

## Comparison with Other Patterns

- **Adapter**: Changes interface vs same interface with control
- **Decorator**: Adds behavior vs controls access
- **Facade**: Simplifies interface vs same interface
- **Proxy**: Controls access, may not contain real object vs Decorator always wraps object

## Example Use Cases

- **Image Loading**: Lazy load images only when displayed (virtual proxy)
- **Database Connections**: Pool connections, add connection logic (smart reference)
- **API Rate Limiting**: Control API call frequency (protection proxy)
- **Caching**: Cache expensive computation results (cache proxy)
- **Access Control**: Restrict access based on user permissions (protection proxy)
- **Remote Objects**: RPC, web services (remote proxy)
- **Logging**: Log all method calls (logging proxy)
- **Copy-on-Write**: Share data until modification (smart reference)

## Anti-Patterns to Avoid

- **Over-Proxying**: Too many proxy layers causing complexity
- **Leaky Abstraction**: Proxy exposing implementation details
- **Tight Coupling**: Proxy too tightly coupled to real object internals
- **Identity Issues**: Proxy not handling identity (`is`, `==`) correctly
- **Performance Overhead**: Proxy overhead exceeding benefits
- **Breaking Liskov Substitution**: Proxy not properly substitutable

## Implementation Variations

### 1. Virtual Proxy
Lazy initialization of expensive objects.

### 2. Protection Proxy
Access control based on user permissions.

### 3. Remote Proxy
Represents remote objects (RPC, REST).

### 4. Cache Proxy
Caches results to avoid repeated computation.

### 5. Smart Reference Proxy
Reference counting, copy-on-write, locking.

### 6. Logging Proxy
Transparently logs all method calls.

## Python Implementation Patterns

### Using `__getattr__`

```python
class Proxy:
    def __init__(self, real_object):
        self._real = real_object

    def __getattr__(self, name):
        # Delegate to real object
        return getattr(self._real, name)
```

### Using Property Decorator

```python
class LazyProperty:
    @property
    def expensive_data(self):
        if not hasattr(self, '_data'):
            self._data = self._compute()
        return self._data
```

### Using Descriptor

```python
class LazyDescriptor:
    def __get__(self, obj, objtype=None):
        if obj._value is None:
            obj._value = obj._compute()
        return obj._value
```

### Using Protocol

```python
from typing import Protocol

class Subject(Protocol):
    def request(self) -> str:
        ...
```

## Testing Considerations

Proxies affect testing:

- **Mock Real Object**: Easy to mock real object when testing proxy
- **Test Proxy Behavior**: Test that proxy correctly delegates
- **Test Additional Behavior**: Test logging, caching, access control
- **Integration Tests**: Test proxy with real object
- **Performance Tests**: Verify proxy improves performance

## Best Practices

- **Same Interface**: Proxy should have same interface as real object
- **Transparent**: Client shouldn't need to know it's using proxy
- **Lazy Initialization**: Don't create real object in proxy constructor
- **Exception Handling**: Proxy should handle exceptions from real object
- **Thread Safety**: Consider thread safety for shared proxies
- **Resource Management**: Properly clean up resources
- **Documentation**: Document what additional behavior proxy adds
- **Identity Semantics**: Handle `==`, `is`, `hash()` appropriately

## Advanced Patterns

### Proxy + Factory
Factory creates appropriate proxy for different scenarios.

### Proxy + Singleton
Singleton proxy controlling access to singleton real object.

### Proxy + Decorator
Chain proxies to add multiple cross-cutting concerns.

### Proxy + Strategy
Proxy uses different strategies for different operations.

## Real-World Examples

### ORMs (SQLAlchemy, Django ORM)
Lazy loading of related objects (virtual proxy).

### Caching Libraries
Cache proxies (Redis, Memcached clients).

### Network Libraries
Remote proxies (RPC frameworks, gRPC).

### Security Frameworks
Protection proxies (authentication, authorization).

### Image Processing
Virtual proxies for lazy image loading.

## Performance Considerations

- **Lazy Loading**: Balance between lazy loading overhead and memory savings
- **Caching**: Cache expensive operations but manage cache size
- **Network Proxies**: Minimize network round trips
- **Thread Safety**: Locking overhead in multi-threaded scenarios
- **Proxy Overhead**: Ensure proxy overhead is less than benefit gained

## Lazy Loading Strategies

### Lazy Initialization
Load on first access.

### Lazy Collection Loading
Load collections only when accessed.

### Ghost Objects
Minimal object loaded, full object loaded on first property access.

### Eager Loading
Sometimes load eagerly to avoid N+1 problem.

## Copy-on-Write with Proxy

Proxy can implement copy-on-write optimization:

```python
class CopyOnWriteProxy:
    def __init__(self, data):
        self._data = data
        self._copy = None

    def read(self):
        return self._copy if self._copy else self._data

    def write(self, value):
        if self._copy is None:
            self._copy = self._data.copy()
        self._copy[key] = value
```

## Security Considerations

Protection proxies should:
- Validate all inputs
- Check permissions before delegating
- Log security-relevant operations
- Handle authentication/authorization errors
- Not expose implementation details in error messages

## Migration to Proxy Pattern

When refactoring existing code:

1. Identify expensive operations or access control needs
2. Create subject interface (if not already abstract)
3. Rename existing class to RealSubject
4. Create Proxy class implementing subject interface
5. Add proxy behavior (lazy loading, caching, etc.)
6. Update clients to use proxy instead of real object
7. Test that proxy correctly delegates to real object
8. Measure performance improvements

## Proxy vs Decorator

**Proxy:**
- Controls access to object
- May not create real object immediately
- Same interface
- Usually one proxy per real object

**Decorator:**
- Adds behavior to object
- Always wraps existing object
- May extend interface
- Can stack multiple decorators
