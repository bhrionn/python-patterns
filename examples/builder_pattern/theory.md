# Builder Pattern

## Overview

The Builder Pattern is a creational design pattern that separates the construction of a complex object from its representation, allowing the same construction process to create different representations. It provides a step-by-step approach to building objects, making it particularly useful when dealing with objects that have many optional parameters or require complex initialization.

## Intent

- Separate object construction from representation
- Build complex objects step by step
- Allow different representations using the same construction process
- Provide fine control over the construction process
- Hide complex construction logic from client code

## Problem

Consider building complex objects like SQL queries, HTTP requests, or configuration objects. Without the Builder pattern, you might encounter several issues:

```python
# Telescoping constructor anti-pattern
class Query:
    def __init__(self, table, columns=None, where=None, join=None,
                 group_by=None, having=None, order_by=None, limit=None):
        # Too many parameters, hard to remember order
        # Many None values
        # Difficult to read and maintain
        pass

# Usage becomes confusing
query = Query("users", ["name", "email"], "age > 18", None, None, None, "name ASC", 10)
```

Problems with this approach:
- **Telescoping constructors**: Too many constructor parameters
- **Unclear intent**: Hard to understand what each parameter does
- **Inflexibility**: Difficult to add new optional parameters
- **Error-prone**: Easy to pass parameters in wrong order
- **Immutability issues**: Hard to create immutable objects with many parameters

## Solution

The Builder Pattern constructs complex objects step by step. The builder provides methods for configuring each aspect of the object, then builds and returns the final product.

### Key Components

1. **Builder**: Provides methods for constructing parts of the product
2. **Product**: The complex object being built
3. **Director** (optional): Orchestrates the building process using a builder
4. **Client**: Creates the builder and optionally a director

## Benefits

- **Fluent Interface**: Chainable methods for readable code
- **Flexible Construction**: Build objects step by step in any order
- **Single Responsibility**: Separates construction logic from representation
- **Immutability**: Easy to create immutable objects
- **Validation**: Can validate at each step or at build time
- **Multiple Representations**: Different builders can create different representations
- **Clear Code**: Intent is obvious from method names
- **Default Values**: Easy to provide sensible defaults

## When to Use

- When constructing objects with many optional parameters (more than 3-4)
- When object creation involves multiple steps
- When you need to create different representations of an object
- When construction process must allow different representations
- When you want to create immutable objects with many fields
- When telescoping constructors become unwieldy
- When you need fine control over the construction process

## Python-Specific Considerations

Python offers several approaches to implement the Builder pattern:

- **Method chaining**: Return `self` from builder methods for fluent interface
- **Keyword arguments**: Python's kwargs reduce need for builders in simple cases
- **Dataclasses**: Can combine with builders for clean data objects
- **Context managers**: Can use with `__enter__` and `__exit__` for resource management
- **Type hints**: Use for better IDE support and validation
- **Property decorators**: Can add computed properties to builders
- **`__call__`**: Make builder callable to build the object

## Implementation Approaches

### 1. Classic Builder
Separate builder class that constructs the product step by step.

### 2. Fluent Builder
Builder with method chaining for readable construction.

### 3. Telescoping Builder
Builder that inherits from product class.

### 4. Step Builder
Builder that enforces a specific order of construction.

### 5. Director-Based Builder
Separate director class that orchestrates complex builds.

## Comparison with Other Patterns

- **Factory Method**: Creates objects in one step, builder creates step by step
- **Abstract Factory**: Creates families of objects, builder focuses on single complex object
- **Prototype**: Clones existing objects, builder constructs new ones
- **Composite**: Different structure; builder constructs, composite organizes
- **Strategy**: Different behavior; builder constructs objects

## Example Use Cases

- **Query Builders**: SQL, NoSQL, or API query construction
- **Request Builders**: HTTP request configuration
- **Document Builders**: PDF, HTML, or report generation
- **Configuration Objects**: Application or service configuration
- **Test Data Builders**: Creating complex test fixtures
- **UI Builders**: Constructing complex UI components
- **Email/Message Builders**: Composing messages with attachments, formatting
- **Form Builders**: Dynamic form generation
- **Navigation/Menu Builders**: Building complex navigation structures

## Anti-Patterns to Avoid

- **Overuse**: Don't use builder for simple objects with few parameters
- **Mandatory Fields Not Enforced**: Should validate required fields at build time
- **Mutable Products**: Products should typically be immutable after building
- **Stateful Builders**: Builders should be reusable or clearly single-use
- **Too Many Builders**: Don't create builder for every class
- **Complex Builder Logic**: Keep builder simple; move complexity to product
- **Leaky Abstraction**: Don't expose product's internal structure through builder

## Implementation Variations

### 1. Immutable Product Builder
Builds immutable objects with all fields set at construction.

### 2. Incremental Builder
Allows modification of product during construction.

### 3. Generic Builder
Type-safe generic builder that works with multiple product types.

### 4. Staged Builder
Enforces construction stages with different builder interfaces.

### 5. Nested Builder
Builder nested inside the product class.

## Python Implementation Patterns

### Basic Fluent Builder
```python
class QueryBuilder:
    def __init__(self):
        self._query = Query()

    def select(self, columns):
        self._query.columns = columns
        return self  # Enable chaining

    def where(self, condition):
        self._query.condition = condition
        return self

    def build(self):
        return self._query
```

### Builder with Validation
```python
class QueryBuilder:
    def build(self):
        if not self._table:
            raise ValueError("Table is required")
        return Query(self._table, self._columns, self._where)
```

### Nested Builder Pattern
```python
class Query:
    class Builder:
        def __init__(self):
            self._table = None

        def table(self, name):
            self._table = name
            return self

        def build(self):
            return Query(self._table)
```

### Director-Based Builder
```python
class QueryDirector:
    def __init__(self, builder):
        self._builder = builder

    def construct_user_query(self):
        return (self._builder
                .select(["id", "name"])
                .from_table("users")
                .where("active = 1")
                .build())
```

## Testing Considerations

Builder patterns are highly testable:

- **Test Each Step**: Verify each builder method works correctly
- **Test Validation**: Ensure build() validates required fields
- **Test Immutability**: Verify products are immutable if intended
- **Test Defaults**: Check default values are applied correctly
- **Test Chaining**: Ensure method chaining works properly
- **Test Reusability**: Verify builders can be reused if designed to be

## Best Practices

- **Fluent Interface**: Use method chaining for readability
- **Immutable Products**: Make built objects immutable
- **Validate on Build**: Check required fields in build() method
- **Clear Method Names**: Use descriptive builder method names
- **Return Types**: Type hint return types for better IDE support
- **Reusable Builders**: Make builders reusable or create new instance each time
- **Sensible Defaults**: Provide reasonable default values
- **Documentation**: Document required vs optional fields
- **Copy Don't Mutate**: Builder methods should not mutate previous state if reusable

## Advanced Patterns

### Builder + Factory
Use factory to create appropriate builder based on type.

### Builder + Prototype
Clone builder state for similar objects.

### Builder + Strategy
Use different strategies within builder for variations.

### Builder + Template Method
Define skeleton of building process, let subclasses customize steps.

## Real-World Examples

### SQLAlchemy Query Builder
Builds SQL queries programmatically with fluent interface.

### Django QuerySet
Chains query operations to build database queries.

### Requests Library
Builds HTTP requests with session configuration.

### StringBuilder/StringBuffer
Java's string builder for efficient string construction.

### pytest Fixtures
Building complex test data and configurations.

## Performance Considerations

- **Object Creation Overhead**: Builders add slight overhead; acceptable for complex objects
- **Memory Usage**: Builder holds intermediate state; release after build()
- **Validation Cost**: Validate once at build time, not at each step
- **Reusability**: Reusing builders can improve performance
- **Lazy Evaluation**: Defer expensive operations until build()

## Migration to Builder Pattern

When refactoring existing code:

1. Identify classes with telescoping constructors
2. Create builder class for the target class
3. Move construction logic to builder methods
4. Add fluent interface (return self)
5. Add validation in build() method
6. Update client code to use builder
7. Consider making product immutable
8. Remove old constructors or mark as deprecated

## Common Pitfalls

- **Not validating required fields**: Always validate in build()
- **Mutable products**: Can lead to unexpected behavior
- **Stateful builders**: Makes reuse difficult and error-prone
- **Too much in builder**: Builder should construct, not contain business logic
- **Forgetting to call build()**: Builder is not the product
- **Not returning self**: Breaks method chaining
- **Complex validation**: Keep validation simple; move complex logic to product

## Builder vs Named Parameters

Python's keyword arguments reduce the need for builders in simple cases:

**Use kwargs when:**
- Object is simple with few parameters
- All parameters are independent
- No complex validation needed
- No step-by-step construction required

**Use Builder when:**
- Many optional parameters (>4-5)
- Complex validation or interdependencies
- Multiple representations needed
- Step-by-step construction adds clarity
- Want to enforce immutability
- Construction process is complex

## Method Chaining Best Practices

When implementing fluent interfaces:

```python
def method(self, value):
    """
    Set a value.

    Args:
        value: The value to set

    Returns:
        Self for method chaining
    """
    self._value = value
    return self  # Critical for chaining
```

- Always return `self` from builder methods
- Type hint return type as builder class
- Document that method returns self
- Keep methods focused on single concern
- Order doesn't matter (unless using staged builder)

## Validation Strategies

### Fail-Fast Validation
```python
def where(self, condition):
    if not condition:
        raise ValueError("Condition cannot be empty")
    self._where = condition
    return self
```

### Deferred Validation
```python
def build(self):
    if not self._table:
        raise ValueError("Table is required")
    if self._limit and self._limit < 0:
        raise ValueError("Limit must be positive")
    return Query(...)
```

### Progressive Validation
Validate incrementally as you build, and final validation at build time.

Choose based on:
- **Fail-fast**: Better error messages, catches errors early
- **Deferred**: More flexible, allows any construction order
- **Progressive**: Balance of both, good for complex objects
