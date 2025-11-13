# Composite Pattern

## Overview

The Composite Pattern is a structural design pattern that allows you to compose objects into tree structures to represent part-whole hierarchies. It lets clients treat individual objects and compositions of objects uniformly, enabling recursive composition and simplifying client code that works with complex tree structures.

## Intent

- Compose objects into tree structures to represent part-whole hierarchies
- Allow clients to treat individual objects and compositions uniformly
- Create recursive tree structures where nodes can be either leaves or containers
- Simplify client code by eliminating the need to distinguish between simple and complex elements
- Enable adding new kinds of components easily

## Problem

Consider a file system with files and folders, or a graphics system with shapes and groups. Without the Composite pattern, you face several issues:

```python
# Without Composite - need to distinguish between types
def calculate_size(item):
    if isinstance(item, File):
        return item.size
    elif isinstance(item, Folder):
        total = 0
        for child in item.children:
            if isinstance(child, File):
                total += child.size
            elif isinstance(child, Folder):
                # Need to recurse, duplicate logic
                total += calculate_size(child)
        return total
```

Problems with this approach:
- **Type checking everywhere**: Client must distinguish between leaf and composite
- **Code duplication**: Similar operations repeated for different types
- **Fragile code**: Adding new component types breaks existing code
- **Complex client logic**: Clients handle tree traversal manually
- **Violates Open/Closed**: Can't add new components without modifying client code

## Solution

The Composite Pattern defines a common interface for both simple (leaf) and complex (composite) objects. Composite objects contain children and delegate operations to them, creating a recursive structure.

### Key Components

1. **Component**: Interface for all objects in the composition (both leaf and composite)
2. **Leaf**: Primitive object with no children, implements Component interface
3. **Composite**: Object that has children, implements Component interface and delegates to children
4. **Client**: Works with objects through the Component interface

## Benefits

- **Uniform Treatment**: Clients treat leaves and composites identically
- **Recursive Composition**: Easy to create complex tree structures
- **Open/Closed Principle**: Easy to add new component types
- **Simplified Client Code**: No need for type checking or special cases
- **Flexible Structure**: Can nest components arbitrarily deep
- **Single Responsibility**: Each component handles its own operations
- **Easy Traversal**: Tree traversal is built into the structure

## When to Use

- When you need to represent part-whole hierarchies
- When you want clients to treat simple and complex objects uniformly
- When you have tree-like structures (file systems, UI components, org charts)
- When you need recursive composition of objects
- When the structure can be represented as a tree
- When you want to simplify client code by removing type checks
- When you need to perform operations on all elements of a complex structure

## Python-Specific Considerations

Python's features enhance the Composite pattern:

- **Duck Typing**: No need for explicit interfaces in simple cases
- **Protocol Classes**: Use `typing.Protocol` for structural subtyping
- **ABC Module**: Use abstract base classes for strict interfaces
- **List/Set Operations**: Python's collections work naturally with composites
- **Iteration**: Implement `__iter__` for natural iteration
- **`__len__`**: Implement for counting elements
- **Generators**: Use `yield` for memory-efficient tree traversal
- **Multiple Inheritance**: Can combine behaviors if needed

## Implementation Approaches

### 1. Classic Composite
Strict interface with separate Leaf and Composite classes.

### 2. Transparent Composite
All components have child management methods (even leaves).

### 3. Safe Composite
Only composites have child management methods (type-safe).

### 4. Cached Composite
Composite caches results of operations for performance.

### 5. Lazy Composite
Composite loads children on demand.

## Comparison with Other Patterns

- **Decorator**: Adds responsibilities; Composite aggregates children
- **Iterator**: Traverses collection; Composite defines structure
- **Chain of Responsibility**: Passes requests; Composite delegates operations
- **Visitor**: Separates operations from structure; works well with Composite
- **Flyweight**: Shares objects for efficiency; Composite creates structure

## Example Use Cases

- **File Systems**: Files and folders
- **GUI Components**: Widgets, containers, panels
- **Graphics**: Shapes, groups of shapes, drawings
- **Organizational Charts**: Employees, departments, divisions
- **Menu Systems**: Menu items, submenus, menu bars
- **Expression Trees**: Numbers, operators, complex expressions
- **Document Structure**: Paragraphs, sections, chapters, books
- **Task Lists**: Tasks, subtasks, projects
- **Product Catalogs**: Products, categories, subcategories
- **Network Topology**: Devices, networks, subnets

## Anti-Patterns to Avoid

- **Over-Generalization**: Don't use Composite for simple flat structures
- **Improper Leaf Methods**: Leaves shouldn't have child management methods (in safe variant)
- **Violation of Uniformity**: Breaking the uniform interface defeats the purpose
- **Deep Nesting**: Excessively deep trees can impact performance
- **Circular References**: Parent-child cycles cause infinite loops
- **Missing Null Checks**: Not handling empty composites
- **Ignoring Performance**: Not caching results when appropriate

## Implementation Variations

### 1. Parent References
Components maintain references to their parent for upward traversal.

### 2. Child Ordering
Composites maintain ordered children (list) vs unordered (set).

### 3. Shared Ownership
Children can belong to multiple parents (requires careful design).

### 4. Caching
Cache operation results to avoid repeated traversal.

### 5. Lazy Loading
Load children only when accessed.

## Python Implementation Patterns

### Basic Composite with ABC
```python
from abc import ABC, abstractmethod

class Component(ABC):
    @abstractmethod
    def operation(self):
        pass

class Leaf(Component):
    def operation(self):
        return "Leaf"

class Composite(Component):
    def __init__(self):
        self._children = []

    def add(self, component):
        self._children.append(component)

    def operation(self):
        results = [child.operation() for child in self._children]
        return f"Composite({', '.join(results)})"
```

### Composite with Protocol
```python
from typing import Protocol, List

class Component(Protocol):
    def operation(self) -> str: ...

class Composite:
    def __init__(self):
        self._children: List[Component] = []

    def add(self, component: Component):
        self._children.append(component)

    def operation(self) -> str:
        return "".join(c.operation() for c in self._children)
```

### Iterable Composite
```python
class Composite(Component):
    def __init__(self):
        self._children = []

    def add(self, component):
        self._children.append(component)

    def __iter__(self):
        return iter(self._children)

    def __len__(self):
        return len(self._children)
```

### Recursive Generator
```python
class Composite(Component):
    def all_components(self):
        """Recursively yield all components in tree."""
        yield self
        for child in self._children:
            if hasattr(child, 'all_components'):
                yield from child.all_components()
            else:
                yield child
```

## Testing Considerations

Composite patterns are highly testable:

- **Test Leaves Independently**: Verify leaf behavior
- **Test Empty Composites**: Handle composites with no children
- **Test Single Child**: Composite with one child
- **Test Multiple Children**: Composite with multiple children
- **Test Deep Nesting**: Multi-level hierarchies
- **Test Traversal**: Verify all nodes are visited
- **Test Add/Remove**: Child management operations
- **Mock Children**: Use mocks for testing composite logic

## Best Practices

- **Consistent Interface**: All components implement same operations
- **Immutability Consideration**: Decide if tree structure is mutable
- **Parent References**: Add if upward traversal is needed
- **Error Handling**: Handle missing children gracefully
- **Type Hints**: Use for better IDE support and documentation
- **Clear Naming**: Name classes clearly (e.g., FileSystemItem, Folder, File)
- **Null Object**: Consider using null object pattern for missing children
- **Thread Safety**: Add locking if tree is modified concurrently
- **Avoid Cycles**: Prevent parent-child cycles

## Advanced Patterns

### Composite + Visitor
Use Visitor to add operations without modifying component classes.

### Composite + Iterator
Implement custom iterators for different traversal strategies (depth-first, breadth-first).

### Composite + Factory
Use factory to create appropriate components based on input.

### Composite + Decorator
Decorate composite operations for logging, caching, etc.

### Composite + Command
Store commands in composite structure for undo/redo.

## Real-World Examples

### GUI Frameworks
- Tkinter: Frame contains widgets
- PyQt: QWidget hierarchy
- HTML DOM: Elements contain child elements

### File Systems
- pathlib: Path objects represent files and directories
- os.walk: Traverses directory trees

### Abstract Syntax Trees
- Python ast module: Represents code as tree
- Expression evaluators: Parse and evaluate expressions

### Document Structures
- Markdown/HTML parsers: Documents as tree of elements
- PDF generators: Pages contain sections contain paragraphs

## Performance Considerations

- **Traversal Cost**: Deep trees require many recursive calls
- **Caching**: Cache results of expensive operations
- **Lazy Loading**: Load children only when needed
- **Iteration Strategy**: Choose depth-first vs breadth-first based on needs
- **Memory Usage**: Large trees consume significant memory
- **Reference Management**: Be aware of reference cycles
- **Batch Operations**: Process multiple operations together when possible

## Migration to Composite Pattern

When refactoring existing code:

1. Identify hierarchical structures in your code
2. Define common Component interface
3. Create Leaf classes for primitive objects
4. Create Composite classes for containers
5. Replace type checks with polymorphic calls
6. Update client code to use uniform interface
7. Add child management methods to composites
8. Test tree construction and traversal
9. Handle edge cases (empty composites, deep nesting)

## Common Pitfalls

- **Forgetting to iterate children**: Composite must delegate to all children
- **Not handling empty composites**: Check for zero children
- **Breaking uniformity**: All components must implement same interface
- **Circular references**: Child becomes its own ancestor
- **Ignoring leaf operations**: Leaves must implement all Component methods
- **Deep recursion**: Very deep trees can cause stack overflow
- **Shared children**: Same child in multiple parents can cause issues
- **Not considering thread safety**: Concurrent modifications need locking

## Safe vs Transparent Composite

### Safe Composite
- Child management methods only in Composite class
- Type-safe: can't add children to leaves
- Requires type checking or separate interfaces
- Better type safety

```python
class Leaf(Component):
    def operation(self): pass
    # No add/remove methods

class Composite(Component):
    def operation(self): pass
    def add(self, child): pass  # Only in Composite
```

### Transparent Composite
- Child management methods in Component interface
- All components have same interface
- Leaf implementations may throw exceptions or ignore
- More uniform but less type-safe

```python
class Component(ABC):
    def operation(self): pass
    def add(self, child): pass  # In base interface
    def remove(self, child): pass

class Leaf(Component):
    def add(self, child):
        raise NotImplementedError("Cannot add to leaf")
```

**Recommendation**: Use Safe Composite for type safety, Transparent for uniformity.

## Tree Traversal Strategies

### Depth-First Traversal
```python
def traverse_depth_first(component):
    yield component
    if hasattr(component, '_children'):
        for child in component._children:
            yield from traverse_depth_first(child)
```

### Breadth-First Traversal
```python
from collections import deque

def traverse_breadth_first(root):
    queue = deque([root])
    while queue:
        component = queue.popleft()
        yield component
        if hasattr(component, '_children'):
            queue.extend(component._children)
```

### Pre-order, In-order, Post-order
For binary trees or specific traversal needs.

## Parent-Child Relationships

### With Parent References
```python
class Component:
    def __init__(self):
        self._parent = None

    def get_parent(self):
        return self._parent

class Composite(Component):
    def add(self, child):
        self._children.append(child)
        child._parent = self  # Set parent reference
```

**Benefits**: Can traverse upward, find root, get path
**Drawbacks**: More complex, potential for inconsistency

## Composite with Operations

Different operations on composite structures:

- **Aggregation**: Sum, count, average across tree
- **Search**: Find components matching criteria
- **Transformation**: Map operations across tree
- **Filtering**: Select subset of tree
- **Validation**: Check tree invariants
- **Serialization**: Convert tree to/from external format

## Thread Safety in Composites

When composites are modified concurrently:

```python
import threading

class ThreadSafeComposite(Component):
    def __init__(self):
        self._children = []
        self._lock = threading.Lock()

    def add(self, child):
        with self._lock:
            self._children.append(child)

    def operation(self):
        with self._lock:
            return "".join(c.operation() for c in self._children)
```

Consider:
- Lock granularity (fine vs coarse)
- Read-write locks for better performance
- Immutable trees to avoid locking
- Copy-on-write for concurrent access
