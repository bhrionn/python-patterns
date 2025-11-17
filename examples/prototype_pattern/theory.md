# Prototype Pattern

## Overview

The Prototype Pattern is a creational design pattern that creates new objects by copying existing instances (prototypes) rather than creating new instances from scratch. It uses cloning to produce new objects, allowing you to avoid expensive initialization and reduce the complexity of object creation.

## Intent

- Create new objects by cloning existing instances
- Avoid costly initialization when creating similar objects
- Reduce subclassing to achieve different object configurations
- Encapsulate object creation complexity
- Support adding and removing objects at runtime

## Problem

Consider a game where you have various character types (warriors, mages, archers) with complex initialization:

```python
class Character:
    def __init__(self, char_type: str):
        self.type = char_type
        # Expensive operations
        self.load_graphics()      # Load textures from disk
        self.load_animations()    # Load animation data
        self.load_sounds()        # Load sound effects
        self.calculate_stats()    # Complex stat calculations
        self.initialize_ai()      # Set up AI behavior
```

Creating new characters repeatedly performs these expensive operations every time. If you want 100 similar warriors, you perform 100 expensive initializations even though most of the data is identical.

Without the Prototype pattern, you might have:
- Repeated expensive initialization
- Complex constructors with many parameters
- Tight coupling between client code and concrete classes
- Difficulty creating variations of similar objects

## Solution

The Prototype Pattern defines a cloning interface that allows objects to create copies of themselves. Instead of creating new instances from scratch, you clone existing "prototype" instances and modify only what's different.

### Key Components

1. **Prototype Interface**: Declares the cloning interface (typically a `clone()` method)
2. **Concrete Prototype**: Implements the cloning operation
3. **Client**: Creates new objects by asking prototypes to clone themselves

## Benefits

- **Performance**: Avoid expensive initialization by cloning existing objects
- **Reduced Complexity**: Simplifies object creation when configuration is complex
- **Dynamic Configuration**: Add/remove prototypes at runtime
- **Reduced Subclassing**: Create variations without defining new subclasses
- **Encapsulation**: Hide complex object creation logic
- **Single Responsibility**: Separates object creation from business logic

## When to Use

- When object initialization is expensive (I/O, database, complex calculations)
- When you need many objects that differ only slightly
- When you want to avoid subclass explosion for different configurations
- When object creation requires accessing databases or external resources
- When the system should be independent of how objects are created
- When you want to create objects without knowing their exact classes

## Python-Specific Considerations

Python provides built-in support for cloning through the `copy` module:

- **Shallow Copy**: `copy.copy()` - Copies object but not nested objects
- **Deep Copy**: `copy.deepcopy()` - Recursively copies entire object tree
- **Custom Cloning**: Implement `__copy__()` and `__deepcopy__()` methods
- **Pickling**: Use `pickle` for serialization-based cloning

### Shallow vs Deep Copy

```python
import copy

# Shallow copy: nested objects are referenced, not copied
shallow = copy.copy(original)

# Deep copy: entire object tree is recursively copied
deep = copy.deepcopy(original)
```

### Custom Clone Behavior

```python
def __copy__(self):
    # Define custom shallow copy behavior
    return type(self)(self.data)

def __deepcopy__(self, memo):
    # Define custom deep copy behavior
    return type(self)(copy.deepcopy(self.data, memo))
```

## Implementation Approaches

### 1. Using copy module
Simplest approach using Python's built-in `copy.deepcopy()`.

### 2. Custom clone method
Implement custom `clone()` method for more control.

### 3. Prototype registry
Maintain registry of prototypes for centralized management.

### 4. Abstract base class
Define prototype interface using ABC.

## Comparison with Other Patterns

- **Factory Method**: Creates objects from scratch vs cloning
- **Abstract Factory**: Creates families of objects vs cloning prototypes
- **Builder**: Constructs complex objects step-by-step vs cloning
- **Singleton**: Ensures one instance vs creating many through cloning

## Example Use Cases

- **Game Development**: Clone game entities (characters, items, enemies)
- **Document Processing**: Clone document templates with formatting
- **GUI Applications**: Clone UI components with similar configurations
- **Database Records**: Clone records with similar data
- **Configuration Objects**: Clone configuration with minor variations
- **3D Graphics**: Clone complex 3D models
- **Testing**: Create test fixtures by cloning base objects
- **Caching**: Cache expensive-to-create objects as prototypes

## Anti-Patterns to Avoid

- **Overuse**: Don't use prototype when simple construction suffices
- **Mutable Shared State**: Be careful with shallow vs deep copying
- **Circular References**: Deep copy can fail with circular references
- **Not Handling Resources**: Clone objects with file handles, database connections carefully
- **Ignoring Inheritance**: Ensure cloning works correctly in inheritance hierarchies
- **Security Issues**: Be aware of cloning sensitive data

## Implementation Variations

### 1. Simple Prototype
Basic implementation with clone method.

### 2. Prototype Registry
Central registry managing multiple prototypes.

### 3. Prototype Manager
Factory-like manager creating objects from prototypes.

### 4. Lazy Cloning
Clone only when necessary (copy-on-write).

### 5. Cached Prototypes
Cache frequently cloned prototypes.

## Python Implementation Patterns

### Using copy module

```python
import copy

class Prototype:
    def clone(self):
        return copy.deepcopy(self)
```

### Custom Clone Method

```python
class Prototype:
    def clone(self):
        # Custom cloning logic
        new_obj = type(self)()
        new_obj.__dict__.update(self.__dict__)
        return new_obj
```

### Prototype Protocol

```python
from typing import Protocol

class Cloneable(Protocol):
    def clone(self) -> 'Cloneable':
        ...
```

### Prototype Registry

```python
class PrototypeRegistry:
    def __init__(self):
        self._prototypes = {}

    def register(self, name: str, prototype):
        self._prototypes[name] = prototype

    def create(self, name: str):
        return self._prototypes[name].clone()
```

## Testing Considerations

Prototype patterns require careful testing:

- **Identity Test**: Ensure cloned object is not the same instance
- **Equality Test**: Verify cloned object has same data
- **Independence Test**: Modifications to clone don't affect original
- **Deep Copy Test**: Nested objects are properly cloned
- **Resource Handling**: File handles, connections are properly handled
- **Performance Test**: Verify cloning is actually faster than creation

## Best Practices

- **Choose Copy Type Carefully**: Decide between shallow and deep copy based on needs
- **Document Copy Semantics**: Make clear what gets copied and what's shared
- **Handle Circular References**: Use `copy.deepcopy()` which handles cycles
- **Consider Immutability**: Immutable objects can share data safely
- **Resource Management**: Handle resources (files, connections) in `__deepcopy__`
- **Test Clone Independence**: Ensure clones are truly independent
- **Use Prototype Registry**: Centralize prototype management when appropriate
- **Version Prototypes**: Track prototype versions if they evolve

## Advanced Patterns

### Prototype + Factory
Use factory to select appropriate prototype to clone.

### Prototype + Builder
Clone base object, then use builder to customize.

### Prototype + Singleton
Single prototype registry (singleton) managing all prototypes.

### Prototype + Memento
Store object states as prototypes for undo/redo.

## Real-World Examples

### Game Development
Clone enemy templates with different stats and equipment.

### Document Editors
Clone document templates (letters, invoices, reports) with standard formatting.

### Scientific Computing
Clone complex simulation configurations for parameter variations.

### UI Frameworks
Clone UI widget trees for similar layouts.

## Performance Considerations

- **Initialization Cost**: Prototyping is beneficial when initialization is expensive
- **Cloning Overhead**: Deep copying has overhead; use shallow copy when possible
- **Memory Usage**: Cloning creates new objects; monitor memory
- **Copy-on-Write**: Consider lazy cloning for large objects
- **Object Graph Complexity**: Deep cloning complex object graphs is expensive
- **Caching**: Cache prototypes to avoid repeated creation

## Shallow vs Deep Copy Trade-offs

### Shallow Copy
- **Pros**: Fast, low memory overhead
- **Cons**: Nested objects are shared (can cause unexpected behavior)
- **Use when**: Objects have primitive fields or intentionally share nested objects

### Deep Copy
- **Pros**: Complete independence, no shared state
- **Cons**: Slower, higher memory usage, potential circular reference issues
- **Use when**: Complete object independence is required

## Migration to Prototype Pattern

When refactoring existing code:

1. Identify expensive object creation operations
2. Create prototype instances with common configurations
3. Implement clone methods (using `copy.deepcopy()` or custom logic)
4. Replace object construction with prototype cloning
5. Create prototype registry if managing multiple prototypes
6. Test that clones are independent and complete
7. Measure performance improvements
