# Command Pattern

## Overview

The Command Pattern is a behavioral design pattern that encapsulates a request as an object, thereby allowing you to parameterize clients with different requests, queue or log requests, and support undoable operations. It decouples the object that invokes the operation from the one that knows how to perform it.

## Intent

- Encapsulate a request as an object
- Parameterize objects with operations
- Queue operations for later execution
- Support undoable operations
- Log changes for audit trails or crash recovery
- Structure a system around high-level operations built on primitive operations
- Decouple the invoker of an operation from the object that performs it

## Problem

Consider a text editor with operations like copy, paste, undo, and redo, or a remote control that can execute different commands on various devices. Without the Command pattern, you face several issues:

```python
# Without Command - tight coupling
class TextEditor:
    def button_click(self, button_type):
        if button_type == "bold":
            self.make_bold()
        elif button_type == "italic":
            self.make_italic()
        elif button_type == "undo":
            # How do we know what to undo?
            # Need to track all previous operations
            pass
```

Problems with this approach:
- **Tight coupling**: Invoker knows too much about receivers
- **No undo/redo**: Difficult to implement without command objects
- **No queueing**: Can't delay or schedule operations
- **No logging**: Can't record operations for audit or replay
- **No macro recording**: Can't combine multiple operations
- **Inflexible**: Hard to add new operations or extend functionality

## Solution

The Command Pattern encapsulates each request as an object with all the information needed to execute it. Commands can be stored, passed around, executed at different times, and undone.

### Key Components

1. **Command**: Interface for executing operations
2. **Concrete Command**: Implements Command interface, binds receiver with action
3. **Receiver**: Knows how to perform the operation
4. **Invoker**: Asks command to execute the request
5. **Client**: Creates concrete command and sets its receiver

## Benefits

- **Decoupling**: Separates invoker from receiver
- **Single Responsibility**: Each command has one job
- **Open/Closed**: Add new commands without modifying existing code
- **Undo/Redo**: Easy to implement by storing command history
- **Macro Commands**: Combine multiple commands
- **Queueing**: Execute commands at different times
- **Logging**: Record all operations for audit or recovery
- **Transactional Behavior**: Group commands into transactions
- **Parameterization**: Pass operations as parameters

## When to Use

- When you need to parameterize objects with operations
- When you need to queue operations, schedule execution, or execute remotely
- When you need to implement undo/redo functionality
- When you need to log operations for audit trails or crash recovery
- When you want to structure a system around high-level operations
- When you need to support transactions or macro recording
- When you want to decouple the object that invokes operation from the one that performs it

## Python-Specific Considerations

Python's features enhance the Command pattern:

- **First-class Functions**: Simple commands can be functions
- **Lambdas**: Use for inline command definitions
- **Closures**: Capture state in command functions
- **Callable Objects**: Classes with `__call__` method
- **Decorators**: Wrap commands with additional behavior
- **Context Managers**: Use with commands for resource management
- **Type Hints**: Use Protocol for command interface
- **Dataclasses**: Simple command objects with `@dataclass`

## Implementation Approaches

### 1. Classic Command
Object-oriented command with execute() method.

### 2. Function-Based Command
Use functions or lambdas as commands.

### 3. Undoable Command
Commands that support undo() operation.

### 4. Macro Command
Composite command that executes multiple commands.

### 5. Transactional Command
Commands that can be committed or rolled back.

## Comparison with Other Patterns

- **Strategy**: Changes algorithm; Command encapsulates request
- **Memento**: Stores state; Command stores operation
- **Prototype**: Clones objects; Command clones operations
- **Chain of Responsibility**: Passes request; Command encapsulates it
- **Composite**: Can combine commands (Macro Command)

## Example Use Cases

- **GUI Applications**: Button clicks, menu items, keyboard shortcuts
- **Text Editors**: Edit operations with undo/redo
- **Transactions**: Database operations that can be rolled back
- **Job Queues**: Background tasks, scheduled jobs
- **Remote Control**: Control devices with different commands
- **Macro Recording**: Record and replay sequences of operations
- **Game Input**: Player actions that can be replayed or undone
- **Wizards**: Multi-step processes with back functionality
- **Network Requests**: Queue and batch API calls
- **Drawing Applications**: Drawing operations with undo

## Anti-Patterns to Avoid

- **Overuse**: Don't use for every operation, only when needed
- **God Commands**: Keep commands focused and simple
- **Stateful Commands**: Commands should be mostly stateless
- **Breaking Encapsulation**: Commands shouldn't expose receiver internals
- **Complex Undo Logic**: Keep undo straightforward
- **Ignoring Failures**: Handle command execution failures
- **Memory Leaks**: Clean up command history when appropriate

## Implementation Variations

### 1. Simple Command
Basic command that just executes an operation.

### 2. Parameterized Command
Command that takes parameters at execution time.

### 3. Queueable Command
Command that can be queued and executed later.

### 4. Loggable Command
Command that logs its execution.

### 5. Compensating Command
Command that can reverse its effects (for transactions).

## Python Implementation Patterns

### Classic OOP Command
```python
from abc import ABC, abstractmethod

class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

class ConcreteCommand(Command):
    def __init__(self, receiver):
        self._receiver = receiver

    def execute(self):
        self._receiver.action()
```

### Function-Based Command
```python
def create_command(receiver, method_name):
    return lambda: getattr(receiver, method_name)()

command = create_command(light, 'turn_on')
command()  # Execute
```

### Undoable Command
```python
class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        pass
```

### Callable Command
```python
class Command:
    def __init__(self, receiver, action):
        self._receiver = receiver
        self._action = action

    def __call__(self):
        return self._action(self._receiver)
```

## Testing Considerations

Command patterns are highly testable:

- **Test Execute**: Verify command executes correctly
- **Test Undo**: Verify undo reverses execution
- **Test Idempotence**: Multiple executes have expected behavior
- **Mock Receivers**: Use mocks to test command logic
- **Test Queueing**: Verify commands execute in order
- **Test Failure Handling**: Ensure failures are handled properly
- **Test State**: Verify command doesn't leak state

## Best Practices

- **Immutable Commands**: Make commands immutable when possible
- **Self-Contained**: Commands should contain all necessary information
- **Stateless**: Avoid storing mutable state in commands
- **Clear Naming**: Use action verbs (SaveCommand, DeleteCommand)
- **Type Hints**: Use for better IDE support
- **Error Handling**: Handle execution failures gracefully
- **History Management**: Limit undo history size
- **Command Validation**: Validate before execution when needed
- **Idempotence**: Consider making commands idempotent

## Advanced Patterns

### Command + Composite (Macro Command)
Combine multiple commands into a single command.

### Command + Memento
Store state with command for more complex undo.

### Command + Prototype
Clone commands for reuse or templating.

### Command + Chain of Responsibility
Commands can pass to next handler if they can't process.

### Command + Observer
Notify observers when commands execute.

## Real-World Examples

### GUI Frameworks
- Qt: QUndoCommand for undo/redo
- Tkinter: Command callbacks for widgets
- PyQt: Action system

### Task Queues
- Celery: Task encapsulation
- RQ: Job queue system
- APScheduler: Scheduled jobs

### Text Editors
- Vim: Command mode operations
- Emacs: Interactive commands
- VS Code: Command palette

### Databases
- Django ORM: Query objects
- SQLAlchemy: Query construction
- Transaction management

## Performance Considerations

- **Memory Usage**: Command history can consume memory
- **History Limits**: Set maximum undo history size
- **Command Pooling**: Reuse command objects when possible
- **Lazy Execution**: Defer expensive operations
- **Batch Processing**: Group commands for efficiency
- **Cleanup**: Remove old commands from history
- **Command Size**: Keep commands lightweight

## Migration to Command Pattern

When refactoring existing code:

1. Identify operations that need to be encapsulated
2. Define Command interface (execute, and optionally undo)
3. Create concrete command classes for each operation
4. Extract receiver logic from invoker
5. Update invoker to work with Command interface
6. Add command history for undo/redo
7. Implement undo operations
8. Add queueing or logging if needed

## Common Pitfalls

- **Forgetting to store state for undo**: Save what's needed to reverse
- **Circular references**: Commands holding references to large objects
- **Not cleaning history**: Unbounded undo stack grows forever
- **Complex commands**: Keep commands simple and focused
- **Synchronous assumptions**: Commands might execute asynchronously
- **Ignoring failures**: Not handling when execution fails
- **Breaking encapsulation**: Exposing too much receiver detail

## Undo/Redo Implementation

### Basic Undo Stack
```python
class CommandInvoker:
    def __init__(self):
        self._history = []
        self._current = -1

    def execute(self, command):
        # Remove any redo commands
        self._history = self._history[:self._current + 1]
        command.execute()
        self._history.append(command)
        self._current += 1

    def undo(self):
        if self._current >= 0:
            self._history[self._current].undo()
            self._current -= 1

    def redo(self):
        if self._current < len(self._history) - 1:
            self._current += 1
            self._history[self._current].execute()
```

### Considerations
- Track current position in history
- Clear redo stack on new command
- Handle empty history
- Limit history size
- Clean up old commands

## Command Queueing

Commands can be queued for:
- **Delayed Execution**: Execute at specific time
- **Batch Processing**: Execute multiple commands together
- **Priority Execution**: Execute high-priority commands first
- **Asynchronous Execution**: Execute in background thread
- **Remote Execution**: Send commands over network

### Simple Queue
```python
from collections import deque

class CommandQueue:
    def __init__(self):
        self._queue = deque()

    def add(self, command):
        self._queue.append(command)

    def execute_all(self):
        while self._queue:
            command = self._queue.popleft()
            command.execute()
```

## Macro Commands (Composite)

Combine multiple commands:

```python
class MacroCommand(Command):
    def __init__(self, commands):
        self._commands = commands

    def execute(self):
        for command in self._commands:
            command.execute()

    def undo(self):
        # Undo in reverse order
        for command in reversed(self._commands):
            command.undo()
```

Benefits:
- Execute multiple operations atomically
- Undo entire sequence
- Reuse command sequences
- Build complex operations from simple ones

## Transactional Commands

Commands with commit/rollback:

```python
class TransactionalCommand(Command):
    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def commit(self):
        pass

    @abstractmethod
    def rollback(self):
        pass
```

Usage:
- Database transactions
- Multi-step operations
- All-or-nothing execution
- Error recovery

## Command Logging

Benefits of logging commands:
- **Audit Trail**: Track all operations
- **Debugging**: See what happened
- **Replay**: Recreate sequence of events
- **Crash Recovery**: Replay commands after crash
- **Analytics**: Analyze usage patterns

### Implementation
```python
class LoggingCommand(Command):
    def __init__(self, command, logger):
        self._command = command
        self._logger = logger

    def execute(self):
        self._logger.log(f"Executing: {self._command}")
        result = self._command.execute()
        self._logger.log(f"Completed: {self._command}")
        return result
```

## Command Validation

Validate before execution:
- Check preconditions
- Verify permissions
- Validate parameters
- Check system state

```python
class ValidatedCommand(Command):
    def can_execute(self):
        # Check if command can be executed
        return True

    def execute(self):
        if not self.can_execute():
            raise ValueError("Command cannot be executed")
        return self._do_execute()

    @abstractmethod
    def _do_execute(self):
        pass
```

## Asynchronous Commands

Commands that execute asynchronously:

```python
import asyncio

class AsyncCommand(ABC):
    @abstractmethod
    async def execute(self):
        pass

class AsyncInvoker:
    async def execute(self, command):
        return await command.execute()
```

Use cases:
- Network requests
- Long-running operations
- Parallel execution
- Background tasks

## Command Serialization

Serialize commands for:
- Network transmission
- Persistent storage
- Inter-process communication
- Command replay

```python
import json

class SerializableCommand(Command):
    def to_dict(self):
        return {
            'type': self.__class__.__name__,
            'params': self._params
        }

    @classmethod
    def from_dict(cls, data):
        return cls(**data['params'])
```

## Thread Safety

For concurrent command execution:

```python
import threading

class ThreadSafeInvoker:
    def __init__(self):
        self._history = []
        self._lock = threading.Lock()

    def execute(self, command):
        with self._lock:
            command.execute()
            self._history.append(command)
```

Consider:
- Lock granularity
- Command atomicity
- Race conditions
- Deadlock prevention
