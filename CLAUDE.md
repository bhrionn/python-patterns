# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository is a comprehensive collection of Python design pattern examples focused on teaching best practices in software design. Each pattern is self-contained with detailed theoretical documentation and practical, production-quality code examples that demonstrate SOLID principles and Python-specific idioms.

## Architecture and Structure

### Directory Organization

```
examples/
├── pattern_name/
│   ├── theory.md      # Comprehensive explanation of the pattern
│   └── example.py     # Working Python code demonstrating the pattern
```

Each pattern example is completely isolated in its own directory. There are no shared dependencies between pattern implementations.

### Pattern Categories

The project covers three main categories of design patterns:

1. **Creational Patterns** (object creation mechanisms)
   - Singleton, Factory Method, Abstract Factory, Builder, Prototype

2. **Structural Patterns** (object composition and relationships)
   - Adapter, Bridge, Composite, Decorator, Facade, Flyweight, Proxy

3. **Behavioral Patterns** (object collaboration and responsibility)
   - Observer, Strategy, Chain of Responsibility, Command, Iterator, Mediator, Memento, State, Template Method, Visitor

## Code Standards

All code in this repository must strictly adhere to the following principles documented in GROK.md:

### SOLID Principles (Non-Negotiable)

- **Single Responsibility**: Each class has exactly one reason to change
- **Open/Closed**: Open for extension, closed for modification
- **Liskov Substitution**: Derived classes must be substitutable for base classes
- **Interface Segregation**: Clients don't depend on unused interfaces
- **Dependency Inversion**: Depend on abstractions, not concretions

### Python Conventions

- Type hints are mandatory on all functions, methods, and class attributes
- Use Python's Protocol type for duck typing interfaces
- Follow PEP 8 (style) and PEP 257 (docstrings)
- Prefer composition over inheritance
- Use abstract base classes (ABC) for defining interfaces
- Use dataclasses for simple data containers
- Use enums for related constants

### Documentation Requirements

Every code artifact requires comprehensive documentation:

- **Module-level docstrings**: Explain the pattern, key features, and SOLID principles demonstrated
- **Class docstrings**: Include purpose, attributes, and usage examples
- **Method/function docstrings**: Document parameters (Args), return values (Returns), and exceptions (Raises) using Google-style format
- **Inline comments**: Only for explaining non-obvious design decisions

### Example Structure Pattern

Each example.py follows this template structure:

1. Module docstring with pattern overview and key features
2. Imports (standard library, third-party, local - in that order)
3. Protocol/Abstract base class definitions
4. Concrete implementations
5. Context/Client classes demonstrating pattern usage
6. `main()` function with comprehensive demonstrations
7. `if __name__ == "__main__"` guard

## Development Commands

### Running Examples

Navigate to any pattern directory and run the example directly:

```bash
cd examples/pattern_name/
python example.py
```

Each example is executable and demonstrates the pattern with output to console.

### Running a Single Pattern

From the repository root:

```bash
python examples/pattern_name/example.py
```

## Adding New Pattern Examples

When adding new patterns:

1. Create directory: `examples/new_pattern_name/`
2. Create `theory.md` with comprehensive pattern documentation including:
   - Overview and intent
   - Problem it solves
   - Solution approach
   - Key components
   - Benefits and when to use
   - Python-specific considerations
   - Example use cases
   - Anti-patterns to avoid
   - Best practices

3. Create `example.py` that:
   - Demonstrates the pattern with a realistic, non-trivial example
   - Adheres to all SOLID principles
   - Includes comprehensive type hints
   - Includes complete documentation
   - Has a working `main()` function with multiple demonstrations
   - Shows error handling where appropriate
   - Uses realistic domain models (not foo/bar examples)

4. Update `tasks.md` to track completion status

## Code Philosophy

This repository serves as a teaching resource. Code quality is paramount:

- Code should be exemplary, not minimal
- Every design decision should demonstrate best practices
- Examples should be realistic and substantial enough to show pattern value
- Avoid oversimplification that obscures the pattern's benefits
- Thread safety and error handling should be shown where relevant
- Examples should be production-quality, not just proof-of-concept

## Reference Documentation

- `PATTERNS.md`: Quick reference cheat sheet for all design patterns
- `GROK.md`: Complete Python expert instruction set with detailed SOLID principles and best practices (follow this as the authoritative guide)
- `tasks.md`: Tracking checklist for pattern implementation progress
- `README.md`: Project overview and getting started guide
