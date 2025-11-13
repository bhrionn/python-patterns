# Template Method Pattern

## Overview

The Template Method Pattern is a behavioral design pattern that defines the skeleton of an algorithm in a base class, allowing subclasses to override specific steps of the algorithm without changing its overall structure. It uses inheritance to achieve code reuse and enforces a consistent algorithm structure across variations.

## Intent

- Define the skeleton of an algorithm in a base class
- Let subclasses override specific steps without changing structure
- Enforce consistent algorithm structure across variations
- Eliminate code duplication through inheritance
- Provide hooks for subclass customization
- Implement the "Hollywood Principle" (Don't call us, we'll call you)

## Problem

Consider a data processing application that processes different file types:

```python
class CSVProcessor:
    def process(self, filename):
        data = self.read_csv_file(filename)
        self.validate_csv_data(data)
        result = self.transform_csv_data(data)
        self.write_csv_file(result)

class JSONProcessor:
    def process(self, filename):
        data = self.read_json_file(filename)
        self.validate_json_data(data)
        result = self.transform_json_data(data)
        self.write_json_file(result)
```

Problems without Template Method:
- Duplicated algorithm structure (read, validate, transform, write)
- Difficult to enforce consistent processing steps
- Hard to add new processing steps to all processors
- Violates DRY (Don't Repeat Yourself) principle
- No guarantee subclasses follow same process

## Solution

The Template Method Pattern defines the algorithm structure in base class:

```python
class DataProcessor(ABC):
    def process(self, filename):  # Template method
        data = self.read_file(filename)
        self.validate_data(data)
        result = self.transform_data(data)
        self.write_file(result)

    @abstractmethod
    def read_file(self, filename): pass

    @abstractmethod
    def validate_data(self, data): pass

    # Subclasses only override specific steps
```

### Key Components

1. **Abstract Class**: Defines template method and abstract operations
2. **Template Method**: Defines algorithm skeleton (usually final/not overridable)
3. **Abstract Operations**: Steps that must be implemented by subclasses
4. **Hook Operations**: Optional steps with default implementation
5. **Concrete Classes**: Implement abstract operations

## Benefits

- **Code Reuse**: Common algorithm structure defined once
- **Consistency**: All subclasses follow same algorithm structure
- **Open/Closed**: New variations added without modifying base class
- **Inversion of Control**: Base class controls flow, subclasses provide details
- **Reduces Duplication**: Common code in base class
- **Enforces Process**: Template method ensures steps are executed in order

## When to Use

- When you have multiple classes with similar algorithms but different implementations
- When you want to control the algorithm structure while allowing customization
- When you want to avoid code duplication across similar classes
- When you need to enforce a specific sequence of steps
- When you want to provide hooks for subclass customization
- When you have invariant parts of algorithm that should not change

## Python-Specific Considerations

Python allows template method with several approaches:

- **ABC and abstractmethod**: Enforce implementation of required methods
- **Hook Methods**: Provide default implementations that can be overridden
- **Multiple Inheritance**: Combine template methods through mixins
- **`super()`**: Chain template method variations
- **NotImplementedError**: Alternative to abstractmethod

### Using ABC

```python
from abc import ABC, abstractmethod

class Template(ABC):
    def template_method(self):
        self.step1()
        self.step2()

    @abstractmethod
    def step1(self): pass

    def step2(self):  # Hook with default
        pass
```

## Implementation Approaches

### 1. Classic Template Method
Abstract base class with template method.

### 2. Template Method with Hooks
Provide optional hook methods with default behavior.

### 3. Multi-Stage Template
Multiple template methods for different phases.

### 4. Parameterized Template
Template method accepts parameters for customization.

## Comparison with Other Patterns

- **Strategy**: Encapsulates entire algorithm vs defines skeleton
- **Factory Method**: Creates objects vs defines algorithm structure
- **State**: Changes behavior based on state vs structure of algorithm
- **Decorator**: Adds behavior vs defines algorithm skeleton

## Example Use Cases

- **Data Processing**: Read, validate, transform, write pipeline
- **Web Scraping**: Fetch, parse, extract, store pipeline
- **Game Development**: Initialize, update, render game loop
- **Testing Frameworks**: Setup, execute, teardown test lifecycle
- **Build Systems**: Configure, compile, link, package build process
- **Report Generation**: Gather data, format, apply styles, output
- **Authentication**: Validate credentials, check permissions, grant access
- **HTTP Request Handling**: Parse request, authenticate, process, send response

## Anti-Patterns to Avoid

- **Too Many Steps**: Keep template method focused
- **Too Deep Hierarchy**: Avoid deep inheritance chains
- **Rigid Template**: Provide hooks for flexibility
- **Leaking Abstractions**: Don't expose implementation details
- **Override Template**: Template method should not be overridable
- **Too Generic**: Keep template method specific to domain

## Implementation Variations

### 1. Simple Template
Basic template method with abstract steps.

### 2. Template with Hooks
Include optional hook methods.

### 3. Multi-Level Template
Template methods at multiple inheritance levels.

### 4. Template with Callbacks
Use callbacks instead of inheritance.

### 5. Template with Context
Pass context object through steps.

## Python Implementation Patterns

### Using ABC

```python
from abc import ABC, abstractmethod

class Template(ABC):
    def template_method(self):
        self.required_step()
        self.optional_hook()

    @abstractmethod
    def required_step(self):
        pass

    def optional_hook(self):
        # Default implementation
        pass
```

### Using NotImplementedError

```python
class Template:
    def template_method(self):
        self.step1()
        self.step2()

    def step1(self):
        raise NotImplementedError("Must implement step1")

    def step2(self):
        pass  # Optional hook
```

### Final Template Method (Python 3.11+)

```python
from typing import final

class Template:
    @final
    def template_method(self):
        # Cannot be overridden
        self.step1()
        self.step2()
```

## Testing Considerations

Template method pattern is testable:

- **Test Template Flow**: Verify template method calls steps in order
- **Test Subclasses**: Test each concrete implementation
- **Mock Steps**: Mock individual steps to test template logic
- **Test Hooks**: Verify hooks are called at right time
- **Template Invariants**: Test that template structure is maintained

## Best Practices

- **Don't Override Template**: Template method should be final
- **Minimize Required Steps**: Only make necessary steps abstract
- **Provide Hooks**: Allow optional customization through hooks
- **Clear Naming**: Use descriptive names for steps
- **Document Process**: Document algorithm flow clearly
- **Keep Steps Focused**: Each step should have single responsibility
- **Use Final**: Mark template method as final (Python 3.11+)
- **Composition Alternative**: Consider strategy pattern for more flexibility

## Advanced Patterns

### Template Method + Factory
Factory creates objects with template methods.

### Template Method + Strategy
Template steps use strategies for variation.

### Template Method + Hook
Extensive use of hooks for customization.

### Template Method + Observer
Notify observers at each template step.

## Real-World Examples

### Testing Frameworks (pytest, unittest)
`setUp()`, test execution, `tearDown()` template.

### Django Class-Based Views
`dispatch()`, `get()`, `post()` template for request handling.

### Web Frameworks
Request handling pipeline (parse, authenticate, process, respond).

### Build Tools
Build process template (configure, compile, link, package).

## Performance Considerations

- **Virtual Method Calls**: Slight overhead from dynamic dispatch
- **Deep Hierarchies**: Avoid deep inheritance for performance
- **Step Granularity**: Balance between fine-grained and coarse steps
- **Caching**: Cache expensive step results when appropriate
- **Lazy Evaluation**: Defer expensive steps until needed

## Hook Methods

Hooks provide extension points without requiring override:

```python
class Template:
    def template_method(self):
        self.before_processing()  # Hook
        self.process()
        self.after_processing()   # Hook

    def before_processing(self):
        pass  # Optional hook

    def after_processing(self):
        pass  # Optional hook

    @abstractmethod
    def process(self):
        pass  # Required step
```

## Hollywood Principle

Template Method implements "Don't call us, we'll call you":

- **Framework calls application**: Base class calls subclass methods
- **Inversion of Control**: Parent class controls flow
- **Subclass Plugs In**: Subclass provides implementations

## When to Use Inheritance vs Composition

**Use Template Method (Inheritance) When:**
- Algorithm structure is stable and unlikely to change
- Variations share substantial common code
- Strong "is-a" relationship exists
- You want to enforce process consistency

**Use Strategy (Composition) When:**
- Need runtime algorithm switching
- Multiple orthogonal variations exist
- Prefer composition over inheritance
- Algorithm structure may change

## Migration to Template Method Pattern

When refactoring existing code:

1. Identify similar algorithms in multiple classes
2. Extract common algorithm structure
3. Create abstract base class with template method
4. Move common code to base class
5. Identify varying steps
6. Make varying steps abstract or hook methods
7. Create concrete subclasses implementing steps
8. Test that all variations work correctly
9. Remove duplicated code from original classes

## Template Method vs Strategy

**Template Method:**
- Uses inheritance
- Algorithm structure in base class
- Subclasses override steps
- Static at runtime (set at object creation)
- More rigid structure
- Better for stable algorithm with variations

**Strategy:**
- Uses composition
- Algorithm encapsulated in strategy objects
- Can switch strategies at runtime
- More flexible
- Looser coupling
- Better for interchangeable algorithms

## Primitive Operations vs Hooks

**Primitive Operations (Abstract):**
- Must be implemented by subclasses
- Core algorithm steps
- Use `@abstractmethod`

**Hooks (Concrete with default):**
- Optional customization points
- Have default implementation (often empty)
- Subclasses can override if needed

## Final Methods in Python

Python 3.11+ supports `@final` decorator:

```python
from typing import final

class Template:
    @final
    def template_method(self):
        # Cannot be overridden in subclasses
        self.step1()
        self.step2()
```

Before Python 3.11, document that method should not be overridden.
