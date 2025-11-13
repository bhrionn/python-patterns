"""
Command Pattern Example: Text Editor with Undo/Redo

This example demonstrates the Command Pattern using a text editor that supports
various editing operations with full undo/redo functionality. The pattern
encapsulates operations as command objects, enabling history tracking,
macro recording, and transactional editing.

Key features:
- Abstract Command interface with execute and undo
- Multiple concrete commands (insert, delete, replace, format)
- Command history with undo/redo stack
- Macro commands (composite commands)
- Command logging and statistics
- Type hints and comprehensive documentation
- Adherence to Single Responsibility and Open/Closed Principles
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
from enum import Enum, auto


# ============================================================================
# Receiver (The object that performs actual operations)
# ============================================================================


class TextDocument:
    """
    Receiver class that performs actual text editing operations.

    This class knows how to perform the operations but doesn't know
    when or why they're called. Commands will invoke these methods.
    """

    def __init__(self, initial_content: str = ""):
        """
        Initialize a text document.

        Args:
            initial_content: Initial text content
        """
        self._content = initial_content

    def insert(self, position: int, text: str) -> None:
        """
        Insert text at specified position.

        Args:
            position: Position to insert at
            text: Text to insert

        Raises:
            ValueError: If position is invalid
        """
        if position < 0 or position > len(self._content):
            raise ValueError(f"Invalid position: {position}")

        self._content = self._content[:position] + text + self._content[position:]

    def delete(self, position: int, length: int) -> str:
        """
        Delete text at specified position.

        Args:
            position: Starting position
            length: Number of characters to delete

        Returns:
            Deleted text

        Raises:
            ValueError: If position or length is invalid
        """
        if length == 0:
            return ""  # No deletion needed
        if position < 0 or position >= len(self._content):
            raise ValueError(f"Invalid position: {position}")
        if length < 0 or position + length > len(self._content):
            raise ValueError(f"Invalid length: {length}")

        deleted_text = self._content[position:position + length]
        self._content = self._content[:position] + self._content[position + length:]
        return deleted_text

    def replace(self, position: int, length: int, text: str) -> str:
        """
        Replace text at specified position.

        Args:
            position: Starting position
            length: Number of characters to replace
            text: Replacement text

        Returns:
            Replaced text

        Raises:
            ValueError: If position or length is invalid
        """
        old_text = self.delete(position, length)
        self.insert(position, text)
        return old_text

    def get_content(self) -> str:
        """
        Get current document content.

        Returns:
            Current text content
        """
        return self._content

    def get_length(self) -> int:
        """
        Get length of document.

        Returns:
            Number of characters
        """
        return len(self._content)

    def clear(self) -> str:
        """
        Clear all content.

        Returns:
            Previous content
        """
        old_content = self._content
        self._content = ""
        return old_content

    def __str__(self) -> str:
        """String representation of document."""
        return self._content

    def __repr__(self) -> str:
        """Detailed representation of document."""
        return f"TextDocument({len(self._content)} chars)"


# ============================================================================
# Command Interface
# ============================================================================


class Command(ABC):
    """
    Abstract base class for all commands.

    Commands encapsulate an operation along with all the information
    needed to execute and undo it. This is the core of the Command pattern.
    """

    @abstractmethod
    def execute(self) -> None:
        """
        Execute the command.

        This method performs the operation. It should be idempotent
        or handle multiple executions appropriately.
        """
        pass

    @abstractmethod
    def undo(self) -> None:
        """
        Undo the command.

        This method reverses the operation performed by execute().
        It should restore the state to before execute() was called.
        """
        pass

    def get_description(self) -> str:
        """
        Get human-readable description of the command.

        Returns:
            Description string
        """
        return self.__class__.__name__


# ============================================================================
# Concrete Commands
# ============================================================================


class InsertCommand(Command):
    """
    Command to insert text at a specific position.

    This command demonstrates a basic operation with undo functionality.
    """

    def __init__(self, document: TextDocument, position: int, text: str):
        """
        Initialize insert command.

        Args:
            document: Document to operate on
            position: Position to insert at
            text: Text to insert
        """
        self._document = document
        self._position = position
        self._text = text
        self._executed = False

    def execute(self) -> None:
        """Execute the insert operation."""
        self._document.insert(self._position, self._text)
        self._executed = True

    def undo(self) -> None:
        """Undo the insert operation by deleting inserted text."""
        if self._executed:
            self._document.delete(self._position, len(self._text))
            self._executed = False

    def get_description(self) -> str:
        """Get description of this command."""
        preview = self._text[:20] + "..." if len(self._text) > 20 else self._text
        return f"Insert '{preview}' at position {self._position}"


class DeleteCommand(Command):
    """
    Command to delete text at a specific position.

    This command stores the deleted text so it can be restored during undo.
    """

    def __init__(self, document: TextDocument, position: int, length: int):
        """
        Initialize delete command.

        Args:
            document: Document to operate on
            position: Starting position
            length: Number of characters to delete
        """
        self._document = document
        self._position = position
        self._length = length
        self._deleted_text: Optional[str] = None

    def execute(self) -> None:
        """Execute the delete operation and store deleted text."""
        self._deleted_text = self._document.delete(self._position, self._length)

    def undo(self) -> None:
        """Undo the delete operation by reinserting deleted text."""
        if self._deleted_text is not None:
            self._document.insert(self._position, self._deleted_text)

    def get_description(self) -> str:
        """Get description of this command."""
        return f"Delete {self._length} chars at position {self._position}"


class ReplaceCommand(Command):
    """
    Command to replace text at a specific position.

    This command combines delete and insert operations.
    """

    def __init__(self, document: TextDocument, position: int, length: int, text: str):
        """
        Initialize replace command.

        Args:
            document: Document to operate on
            position: Starting position
            length: Number of characters to replace
            text: Replacement text
        """
        self._document = document
        self._position = position
        self._length = length
        self._text = text
        self._old_text: Optional[str] = None

    def execute(self) -> None:
        """Execute the replace operation and store old text."""
        self._old_text = self._document.replace(self._position, self._length, self._text)

    def undo(self) -> None:
        """Undo the replace operation by restoring old text."""
        if self._old_text is not None:
            self._document.replace(self._position, len(self._text), self._old_text)

    def get_description(self) -> str:
        """Get description of this command."""
        preview = self._text[:20] + "..." if len(self._text) > 20 else self._text
        return f"Replace {self._length} chars with '{preview}' at position {self._position}"


class AppendCommand(Command):
    """
    Command to append text to the end of document.

    Convenience command that always inserts at the end.
    """

    def __init__(self, document: TextDocument, text: str):
        """
        Initialize append command.

        Args:
            document: Document to operate on
            text: Text to append
        """
        self._document = document
        self._text = text
        self._position: Optional[int] = None

    def execute(self) -> None:
        """Execute the append operation."""
        self._position = self._document.get_length()
        self._document.insert(self._position, self._text)

    def undo(self) -> None:
        """Undo the append operation."""
        if self._position is not None:
            self._document.delete(self._position, len(self._text))

    def get_description(self) -> str:
        """Get description of this command."""
        preview = self._text[:20] + "..." if len(self._text) > 20 else self._text
        return f"Append '{preview}'"


class ClearCommand(Command):
    """
    Command to clear all document content.

    This command stores the entire content for undo.
    """

    def __init__(self, document: TextDocument):
        """
        Initialize clear command.

        Args:
            document: Document to operate on
        """
        self._document = document
        self._old_content: Optional[str] = None

    def execute(self) -> None:
        """Execute the clear operation and store old content."""
        self._old_content = self._document.clear()

    def undo(self) -> None:
        """Undo the clear operation by restoring old content."""
        if self._old_content is not None:
            self._document.insert(0, self._old_content)

    def get_description(self) -> str:
        """Get description of this command."""
        return "Clear document"


# ============================================================================
# Macro Command (Composite)
# ============================================================================


class MacroCommand(Command):
    """
    Composite command that executes multiple commands as one operation.

    This demonstrates the Composite pattern combined with Command pattern.
    All sub-commands are executed/undone together atomically.
    """

    def __init__(self, commands: List[Command], description: str = "Macro"):
        """
        Initialize macro command.

        Args:
            commands: List of commands to execute
            description: Description of the macro
        """
        self._commands = commands
        self._description = description
        self._executed_commands: List[Command] = []

    def execute(self) -> None:
        """Execute all commands in order."""
        self._executed_commands = []
        for command in self._commands:
            command.execute()
            self._executed_commands.append(command)

    def undo(self) -> None:
        """Undo all executed commands in reverse order."""
        for command in reversed(self._executed_commands):
            command.undo()
        self._executed_commands = []

    def get_description(self) -> str:
        """Get description of this macro."""
        return f"{self._description} ({len(self._commands)} operations)"


# ============================================================================
# Command Invoker (Manages execution and history)
# ============================================================================


class CommandInvoker:
    """
    Invoker that executes commands and manages undo/redo history.

    This class maintains a history of executed commands and provides
    undo/redo functionality by managing the history stack.
    """

    def __init__(self, max_history: int = 100):
        """
        Initialize command invoker.

        Args:
            max_history: Maximum number of commands to keep in history
        """
        self._history: List[Command] = []
        self._current_index = -1
        self._max_history = max_history

    def execute(self, command: Command) -> None:
        """
        Execute a command and add it to history.

        Any redo commands are removed when a new command is executed.

        Args:
            command: Command to execute
        """
        # Execute the command
        command.execute()

        # Remove any redo commands (everything after current index)
        self._history = self._history[:self._current_index + 1]

        # Add to history
        self._history.append(command)
        self._current_index += 1

        # Trim history if needed
        if len(self._history) > self._max_history:
            self._history.pop(0)
            self._current_index -= 1

    def undo(self) -> bool:
        """
        Undo the last command.

        Returns:
            True if undo was performed, False if nothing to undo
        """
        if not self.can_undo():
            return False

        command = self._history[self._current_index]
        command.undo()
        self._current_index -= 1
        return True

    def redo(self) -> bool:
        """
        Redo the next command.

        Returns:
            True if redo was performed, False if nothing to redo
        """
        if not self.can_redo():
            return False

        self._current_index += 1
        command = self._history[self._current_index]
        command.execute()
        return True

    def can_undo(self) -> bool:
        """
        Check if undo is available.

        Returns:
            True if there are commands to undo
        """
        return self._current_index >= 0

    def can_redo(self) -> bool:
        """
        Check if redo is available.

        Returns:
            True if there are commands to redo
        """
        return self._current_index < len(self._history) - 1

    def get_history(self) -> List[str]:
        """
        Get list of command descriptions in history.

        Returns:
            List of command descriptions
        """
        return [cmd.get_description() for cmd in self._history]

    def get_current_position(self) -> int:
        """
        Get current position in history.

        Returns:
            Current index in history
        """
        return self._current_index

    def clear_history(self) -> None:
        """Clear all command history."""
        self._history = []
        self._current_index = -1


# ============================================================================
# Text Editor (Client)
# ============================================================================


class TextEditor:
    """
    Text editor client that uses commands for all operations.

    This class demonstrates how the client uses the Command pattern
    to provide high-level editing functionality with undo/redo.
    """

    def __init__(self):
        """Initialize text editor."""
        self._document = TextDocument()
        self._invoker = CommandInvoker(max_history=50)

    def insert(self, position: int, text: str) -> None:
        """
        Insert text at position.

        Args:
            position: Position to insert at
            text: Text to insert
        """
        command = InsertCommand(self._document, position, text)
        self._invoker.execute(command)

    def delete(self, position: int, length: int) -> None:
        """
        Delete text at position.

        Args:
            position: Starting position
            length: Number of characters to delete
        """
        command = DeleteCommand(self._document, position, length)
        self._invoker.execute(command)

    def replace(self, position: int, length: int, text: str) -> None:
        """
        Replace text at position.

        Args:
            position: Starting position
            length: Number of characters to replace
            text: Replacement text
        """
        command = ReplaceCommand(self._document, position, length, text)
        self._invoker.execute(command)

    def append(self, text: str) -> None:
        """
        Append text to end of document.

        Args:
            text: Text to append
        """
        command = AppendCommand(self._document, text)
        self._invoker.execute(command)

    def clear(self) -> None:
        """Clear all document content."""
        command = ClearCommand(self._document)
        self._invoker.execute(command)

    def execute_macro(self, commands: List[Command], description: str = "Macro") -> None:
        """
        Execute multiple commands as a single operation.

        Args:
            commands: List of commands to execute
            description: Description of the macro
        """
        macro = MacroCommand(commands, description)
        self._invoker.execute(macro)

    def undo(self) -> bool:
        """
        Undo last operation.

        Returns:
            True if undo was performed
        """
        return self._invoker.undo()

    def redo(self) -> bool:
        """
        Redo next operation.

        Returns:
            True if redo was performed
        """
        return self._invoker.redo()

    def can_undo(self) -> bool:
        """Check if undo is available."""
        return self._invoker.can_undo()

    def can_redo(self) -> bool:
        """Check if redo is available."""
        return self._invoker.can_redo()

    def get_content(self) -> str:
        """Get current document content."""
        return self._document.get_content()

    def get_history(self) -> List[str]:
        """Get command history."""
        return self._invoker.get_history()

    def get_statistics(self) -> dict:
        """
        Get editor statistics.

        Returns:
            Dictionary with statistics
        """
        return {
            'content_length': self._document.get_length(),
            'history_size': len(self._invoker.get_history()),
            'can_undo': self.can_undo(),
            'can_redo': self.can_redo(),
            'current_position': self._invoker.get_current_position()
        }


# ============================================================================
# Demonstration Functions
# ============================================================================


def demonstrate_basic_commands():
    """Demonstrate basic command execution."""
    print("=== Basic Command Execution ===")

    editor = TextEditor()

    # Insert text
    editor.insert(0, "Hello")
    print(f"After insert: '{editor.get_content()}'")

    # Append text
    editor.append(" World")
    print(f"After append: '{editor.get_content()}'")

    # Insert in middle
    editor.insert(5, ",")
    print(f"After insert comma: '{editor.get_content()}'")

    print()


def demonstrate_undo_redo():
    """Demonstrate undo/redo functionality."""
    print("=== Undo/Redo Functionality ===")

    editor = TextEditor()

    # Perform operations
    editor.append("First")
    editor.append(" Second")
    editor.append(" Third")
    print(f"After operations: '{editor.get_content()}'")

    # Undo
    print("\nUndoing operations...")
    editor.undo()
    print(f"After 1 undo: '{editor.get_content()}'")

    editor.undo()
    print(f"After 2 undos: '{editor.get_content()}'")

    # Redo
    print("\nRedoing operations...")
    editor.redo()
    print(f"After 1 redo: '{editor.get_content()}'")

    editor.redo()
    print(f"After 2 redos: '{editor.get_content()}'")

    print()


def demonstrate_replace_and_delete():
    """Demonstrate replace and delete commands."""
    print("=== Replace and Delete Commands ===")

    editor = TextEditor()

    editor.append("The quick brown fox")
    print(f"Original: '{editor.get_content()}'")

    # Replace word
    editor.replace(4, 5, "slow")
    print(f"After replace 'quick' with 'slow': '{editor.get_content()}'")

    # Delete word
    editor.delete(10, 6)
    print(f"After delete 'brown ': '{editor.get_content()}'")

    # Undo delete
    editor.undo()
    print(f"After undo delete: '{editor.get_content()}'")

    # Undo replace
    editor.undo()
    print(f"After undo replace: '{editor.get_content()}'")

    print()


def demonstrate_macro_command():
    """Demonstrate macro commands (composite)."""
    print("=== Macro Commands ===")

    editor = TextEditor()
    doc = editor._document

    # Create a macro that formats a heading
    commands = [
        InsertCommand(doc, 0, "="),
        InsertCommand(doc, 0, "="),
        InsertCommand(doc, 0, "="),
        AppendCommand(doc, " "),
        AppendCommand(doc, "Chapter 1"),
        AppendCommand(doc, " "),
        AppendCommand(doc, "="),
        AppendCommand(doc, "="),
        AppendCommand(doc, "=")
    ]

    print("Executing macro to create formatted heading...")
    editor.execute_macro(commands, "Format Heading")
    print(f"Result: '{editor.get_content()}'")

    # Undo entire macro with one operation
    print("\nUndoing entire macro...")
    editor.undo()
    print(f"After undo: '{editor.get_content()}'")

    # Redo macro
    print("\nRedoing macro...")
    editor.redo()
    print(f"After redo: '{editor.get_content()}'")

    print()


def demonstrate_command_history():
    """Demonstrate command history tracking."""
    print("=== Command History ===")

    editor = TextEditor()

    # Perform several operations
    editor.append("Hello")
    editor.append(" ")
    editor.append("World")
    editor.insert(5, ",")
    editor.replace(12, 0, "!")

    # Show history
    print("Command History:")
    for i, desc in enumerate(editor.get_history(), 1):
        print(f"{i}. {desc}")

    print(f"\nCurrent position: {editor.get_statistics()['current_position'] + 1}")
    print(f"Content: '{editor.get_content()}'")

    print()


def demonstrate_complex_editing():
    """Demonstrate complex editing scenario."""
    print("=== Complex Editing Scenario ===")

    editor = TextEditor()

    # Create a document
    print("Creating document...")
    editor.append("Python is a programming language.")
    print(f"Initial: '{editor.get_content()}'")

    # Make several edits
    print("\nMaking edits...")
    editor.insert(10, "powerful ")
    print(f"Added 'powerful': '{editor.get_content()}'")

    # Replace "a programming" with "an amazing"
    editor.replace(19, 13, "an amazing")
    print(f"Modified description: '{editor.get_content()}'")

    editor.insert(0, "Fact: ")
    print(f"Added prefix: '{editor.get_content()}'")

    # Show we can undo everything
    print(f"\nTotal operations: {len(editor.get_history())}")

    print("\nUndoing all operations...")
    while editor.can_undo():
        editor.undo()

    print(f"After undo all: '{editor.get_content()}'")

    # And redo everything
    print("\nRedoing all operations...")
    while editor.can_redo():
        editor.redo()

    print(f"After redo all: '{editor.get_content()}'")

    print()


def demonstrate_statistics():
    """Demonstrate editor statistics."""
    print("=== Editor Statistics ===")

    editor = TextEditor()

    editor.append("The Command Pattern")
    editor.append(" is awesome!")
    editor.undo()
    editor.undo()
    editor.redo()

    stats = editor.get_statistics()
    print("Current Statistics:")
    print(f"  Content Length: {stats['content_length']} characters")
    print(f"  History Size: {stats['history_size']} commands")
    print(f"  Can Undo: {stats['can_undo']}")
    print(f"  Can Redo: {stats['can_redo']}")
    print(f"  Current Position: {stats['current_position'] + 1}/{stats['history_size']}")

    print(f"\nCurrent Content: '{editor.get_content()}'")

    print()


def demonstrate_clear_command():
    """Demonstrate clear command with undo."""
    print("=== Clear Command ===")

    editor = TextEditor()

    editor.append("Important document content that took hours to write.")
    print(f"Original: '{editor.get_content()}'")

    print("\nClearing document...")
    editor.clear()
    print(f"After clear: '{editor.get_content()}'")

    print("\nOops! Undoing clear...")
    editor.undo()
    print(f"After undo: '{editor.get_content()}'")

    print()


def demonstrate_redo_invalidation():
    """Demonstrate that new commands invalidate redo stack."""
    print("=== Redo Invalidation ===")

    editor = TextEditor()

    # Create some history
    editor.append("One")
    editor.append(" Two")
    editor.append(" Three")

    # Undo twice
    editor.undo()
    editor.undo()
    print(f"After 2 undos: '{editor.get_content()}'")
    print(f"Can redo: {editor.can_redo()}")

    # Execute new command - this should clear redo stack
    editor.append(" Four")
    print(f"\nAfter new command: '{editor.get_content()}'")
    print(f"Can redo: {editor.can_redo()} (redo stack was cleared)")

    print()


def demonstrate_real_world_scenario():
    """Demonstrate a realistic text editing scenario."""
    print("=== Real-World Scenario: Writing Code ===")

    editor = TextEditor()

    # Start writing a function
    print("Writing a Python function...")
    editor.append("def calculate_sum(numbers):")
    editor.append("\n    total = 0")
    editor.append("\n    for num in numbers:")
    editor.append("\n        total += num")
    editor.append("\n    return total")

    print("Initial function:")
    print(editor.get_content())

    # Oops, let's add a docstring
    print("\n\nAdding docstring...")
    doc = editor._document
    docstring_commands = [
        InsertCommand(doc, 28, '\n    """'),
        InsertCommand(doc, 32, "Calculate sum of numbers."),
        InsertCommand(doc, 57, "\n    "),
        InsertCommand(doc, 62, "\n    Args:"),
        InsertCommand(doc, 73, "\n        numbers: List of numbers"),
        InsertCommand(doc, 104, "\n    "),
        InsertCommand(doc, 109, "\n    Returns:"),
        InsertCommand(doc, 124, "\n        Sum of all numbers"),
        InsertCommand(doc, 151, '\n    """')
    ]
    editor.execute_macro(docstring_commands, "Add Docstring")

    print("Function with docstring:")
    print(editor.get_content())

    # Show history
    print(f"\n\nCommand History ({len(editor.get_history())} operations):")
    for i, desc in enumerate(editor.get_history()[-10:], 1):
        print(f"  {i}. {desc}")

    print()


# ============================================================================
# Main Function
# ============================================================================


def main():
    """Run all demonstrations of the Command Pattern."""
    print("Command Pattern Example: Text Editor with Undo/Redo\n")

    demonstrate_basic_commands()
    demonstrate_undo_redo()
    demonstrate_replace_and_delete()
    demonstrate_macro_command()
    demonstrate_command_history()
    demonstrate_complex_editing()
    demonstrate_statistics()
    demonstrate_clear_command()
    demonstrate_redo_invalidation()
    demonstrate_real_world_scenario()

    print("All demonstrations completed successfully!")


if __name__ == "__main__":
    main()
