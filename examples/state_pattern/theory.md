# State Pattern

## Overview

The State Pattern is a behavioral design pattern that allows an object to alter its behavior when its internal state changes. The object will appear to change its class by delegating state-specific behavior to separate state objects, making state transitions explicit and manageable.

## Intent

- Allow an object to alter its behavior when its internal state changes
- Encapsulate state-specific behavior in separate classes
- Make state transitions explicit
- Eliminate complex conditional statements based on state
- Make it easy to add new states without changing existing code

## Problem

Consider a document editor with different editing modes (view, edit, review):

```python
class Document:
    def __init__(self):
        self.mode = "view"  # view, edit, review

    def click(self):
        if self.mode == "view":
            print("Opening document")
        elif self.mode == "edit":
            print("Selecting text")
        elif self.mode == "review":
            print("Adding comment")

    def type(self, text):
        if self.mode == "view":
            print("Cannot type in view mode")
        elif self.mode == "edit":
            print(f"Typing: {text}")
        elif self.mode == "review":
            print("Cannot type in review mode")
```

Problems without State pattern:
- Complex conditional logic scattered throughout methods
- Adding new states requires modifying multiple methods
- State transitions are implicit and hard to track
- Violates Open/Closed Principle
- Difficult to maintain and test
- State-specific behavior is not encapsulated

## Solution

The State Pattern encapsulates state-specific behavior in separate state classes:

```python
class DocumentState(ABC):
    @abstractmethod
    def click(self, document): pass

    @abstractmethod
    def type(self, document, text): pass

class ViewState(DocumentState):
    def click(self, document):
        print("Opening document")
        document.set_state(EditState())

    def type(self, document, text):
        print("Cannot type in view mode")

class Document:
    def __init__(self):
        self.state = ViewState()

    def click(self):
        self.state.click(self)

    def type(self, text):
        self.state.type(self, text)
```

### Key Components

1. **Context**: Maintains current state and delegates state-specific requests
2. **State Interface**: Defines interface for state-specific behavior
3. **Concrete States**: Implement behavior for specific states

## Benefits

- **Open/Closed Principle**: New states can be added without modifying existing code
- **Single Responsibility**: Each state class handles one state's behavior
- **Explicit State Transitions**: State changes are clear and trackable
- **Eliminates Conditionals**: No complex if/else or switch statements
- **Encapsulation**: State-specific behavior is encapsulated
- **Testability**: Each state can be tested independently

## When to Use

- When object behavior depends on its state
- When you have large conditional statements based on object state
- When state transitions follow complex rules
- When you need to add new states frequently
- When different states have substantially different behaviors
- When you want to make state transitions explicit

## Python-Specific Considerations

Python's dynamic typing simplifies state pattern implementation:

- **Duck Typing**: No need for formal state interface
- **Dynamic Method Assignment**: Can replace methods dynamically
- **Enums**: Use Enum for state identifiers
- **Context Managers**: States can use `__enter__`/`__exit__`
- **Decorators**: Decorate methods to add state validation

### Using Enums for State Identity

```python
from enum import Enum, auto

class DocumentMode(Enum):
    VIEW = auto()
    EDIT = auto()
    REVIEW = auto()
```

## Implementation Approaches

### 1. Classic State Pattern
Separate state classes implementing state interface.

### 2. State Enum
Use enum values with conditional logic (simpler but less flexible).

### 3. State Dictionary
Map states to behavior dictionaries.

### 4. State Machine
Formal state machine with transition rules.

## Comparison with Other Patterns

- **Strategy**: Algorithms are interchangeable vs states change object behavior
- **Command**: Encapsulates request vs encapsulates state behavior
- **State Machine**: State pattern is implementation of state machine
- **Chain of Responsibility**: Request passes through chain vs state handles request

## Example Use Cases

- **Document Editor**: View, edit, review modes
- **TCP Connection**: Established, listening, closed states
- **Vending Machine**: Ready, has money, dispensing states
- **Order Processing**: New, paid, shipped, delivered states
- **Media Player**: Playing, paused, stopped states
- **Game Character**: Idle, running, jumping, attacking states
- **Authentication**: Unauthenticated, authenticated, locked states
- **Traffic Light**: Red, yellow, green states

## Anti-Patterns to Avoid

- **Too Many States**: Keep state count manageable
- **God State**: States that know too much about context internals
- **State Proliferation**: Don't create state for every minor variation
- **Circular Dependencies**: States shouldn't depend on each other
- **Shared State**: State objects should be stateless or manage only state-specific data
- **Missing Transitions**: Ensure all valid transitions are implemented

## Implementation Variations

### 1. Classic State Objects
Each state is an object instance.

### 2. Singleton States
States are singletons (stateless states).

### 3. State Factory
Factory creates appropriate state objects.

### 4. Hierarchical States
States can have substates.

### 5. State with Transition Rules
Explicit transition validation.

## Python Implementation Patterns

### Using ABC

```python
from abc import ABC, abstractmethod

class State(ABC):
    @abstractmethod
    def handle(self, context):
        pass
```

### Using Protocol

```python
from typing import Protocol

class State(Protocol):
    def handle(self, context) -> None:
        ...
```

### Using Enum

```python
from enum import Enum, auto

class State(Enum):
    IDLE = auto()
    RUNNING = auto()
    STOPPED = auto()
```

### State Transition Validation

```python
class State(ABC):
    allowed_transitions: List[Type['State']] = []

    def can_transition_to(self, state_class):
        return state_class in self.allowed_transitions
```

## Testing Considerations

State patterns are highly testable:

- **Test Each State**: Test state behavior independently
- **Test Transitions**: Verify valid and invalid transitions
- **Mock Context**: Mock context for testing states
- **State Coverage**: Ensure all states are tested
- **Transition Coverage**: Test all state transitions

## Best Practices

- **Stateless States**: Prefer stateless state objects (singletons)
- **Clear Transitions**: Make state transitions explicit and clear
- **Transition Validation**: Validate state transitions
- **State Interface**: Keep state interface focused and cohesive
- **Context API**: Context should provide clean API to states
- **Immutable Transitions**: Consider making state transitions immutable
- **Document State Machine**: Document valid states and transitions
- **Error Handling**: Handle invalid state transitions gracefully

## Advanced Patterns

### State + Factory
Factory creates appropriate initial state.

### State + Strategy
States use different strategies for their behavior.

### State + Command
Commands trigger state transitions.

### Hierarchical State Machines
States can have nested substates.

## Real-World Examples

### TCP Connection States
Linux kernel TCP stack uses state pattern.

### Game Engines
Game character AI and animation states.

### Workflow Engines
Order processing, approval workflows.

### UI Frameworks
Component states (enabled, disabled, hover, focus).

## Performance Considerations

- **State Object Creation**: Use singletons for stateless states
- **Transition Overhead**: Minimize state transition overhead
- **State Caching**: Cache frequently used states
- **Memory**: Consider memory impact of many state objects
- **Transition Validation**: Balance validation thoroughness with performance

## State Machine Diagram

State patterns implement state machines:

```
     +-------+
     | Start |
     +-------+
         |
         v
    +---------+     event1    +---------+
    | State A | ------------> | State B |
    +---------+               +---------+
         ^                         |
         |                         | event2
         +-------------------------+
```

## Transition Guards

Add conditions to transitions:

```python
class State(ABC):
    def can_transition(self, context, next_state):
        # Check if transition is allowed
        return True

    def transition(self, context, next_state):
        if self.can_transition(context, next_state):
            context.set_state(next_state)
        else:
            raise InvalidTransitionError()
```

## Entry and Exit Actions

States can perform actions on entry/exit:

```python
class State(ABC):
    def on_enter(self, context):
        """Called when entering this state."""
        pass

    def on_exit(self, context):
        """Called when exiting this state."""
        pass
```

## Hierarchical States

States can have substates:

```python
class ParentState(State):
    def __init__(self):
        self.substate = None

    def handle(self, context):
        if self.substate:
            self.substate.handle(context)
        else:
            # Handle at parent level
            pass
```

## State History

Remember previous states for back/undo:

```python
class Context:
    def __init__(self):
        self.state = InitialState()
        self.state_history = []

    def set_state(self, state):
        self.state_history.append(self.state)
        self.state = state

    def revert_state(self):
        if self.state_history:
            self.state = self.state_history.pop()
```

## Concurrent States

Object can be in multiple states simultaneously:

```python
class Context:
    def __init__(self):
        self.states = {
            'connection': DisconnectedState(),
            'authentication': UnauthenticatedState(),
            'activity': IdleState()
        }
```

## Migration to State Pattern

When refactoring existing code:

1. Identify state-dependent behavior
2. Extract states as enum or constants
3. Create state interface
4. Create concrete state classes
5. Move state-specific behavior to state classes
6. Replace conditionals with state delegation
7. Implement state transitions
8. Test all states and transitions
9. Document state machine

## State vs Strategy

**State:**
- Changes behavior based on internal state
- State changes during object lifetime
- States aware of each other (for transitions)
- Context delegates to current state

**Strategy:**
- Encapsulates algorithms
- Strategy typically set once
- Strategies independent of each other
- Context chooses strategy explicitly
