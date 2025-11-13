"""
Composite Pattern Example: File System Hierarchy

This example demonstrates the Composite Pattern using a file system structure
with files and directories. The pattern allows uniform treatment of individual
files and directories (which can contain files and subdirectories), enabling
recursive operations on the entire tree structure.

Key features:
- Abstract Component interface for all file system items
- Leaf components (Files) with no children
- Composite components (Directories) that contain children
- Recursive operations (size calculation, display, search)
- Type hints and comprehensive documentation
- Adherence to Open/Closed and Single Responsibility Principles
- Multiple traversal strategies
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Iterator, Set
from datetime import datetime
from enum import Enum, auto
from collections import deque


# ============================================================================
# Component Interface (Base for all file system items)
# ============================================================================


class FileSystemItem(ABC):
    """
    Abstract base class for all file system items.

    This is the Component in the Composite pattern. Both files (leaves)
    and directories (composites) implement this interface, allowing
    clients to treat them uniformly.
    """

    def __init__(self, name: str):
        """
        Initialize a file system item.

        Args:
            name: Name of the item
        """
        self._name = name
        self._created_at = datetime.now()
        self._parent: Optional['Directory'] = None

    @property
    def name(self) -> str:
        """Get the name of the item."""
        return self._name

    @property
    def parent(self) -> Optional['Directory']:
        """Get the parent directory."""
        return self._parent

    @abstractmethod
    def get_size(self) -> int:
        """
        Get the size of the item in bytes.

        Returns:
            Size in bytes
        """
        pass

    @abstractmethod
    def display(self, indent: int = 0) -> str:
        """
        Display the item with indentation.

        Args:
            indent: Indentation level

        Returns:
            String representation with indentation
        """
        pass

    def get_path(self) -> str:
        """
        Get the full path of the item.

        Returns:
            Full path from root to this item
        """
        if self._parent is None:
            return f"/{self._name}"
        return f"{self._parent.get_path()}/{self._name}"

    def get_created_at(self) -> datetime:
        """
        Get creation timestamp.

        Returns:
            Creation datetime
        """
        return self._created_at

    def is_directory(self) -> bool:
        """
        Check if this item is a directory.

        Returns:
            True if directory, False otherwise
        """
        return isinstance(self, Directory)


# ============================================================================
# Leaf Component (File)
# ============================================================================


class File(FileSystemItem):
    """
    Leaf component representing a file.

    Files have no children and represent the end points of the tree structure.
    They implement all Component operations but do not support child management.
    """

    def __init__(self, name: str, size: int, content: str = ""):
        """
        Initialize a file.

        Args:
            name: File name
            size: File size in bytes
            content: File content (optional)
        """
        super().__init__(name)
        self._size = size
        self._content = content

    def get_size(self) -> int:
        """
        Get file size.

        Returns:
            Size in bytes
        """
        return self._size

    def display(self, indent: int = 0) -> str:
        """
        Display file with indentation.

        Args:
            indent: Indentation level

        Returns:
            Formatted string showing file name and size
        """
        indent_str = "  " * indent
        return f"{indent_str}📄 {self._name} ({self._size} bytes)"

    def get_content(self) -> str:
        """
        Get file content.

        Returns:
            File content string
        """
        return self._content

    def __repr__(self) -> str:
        """String representation of file."""
        return f"File('{self._name}', {self._size} bytes)"


# ============================================================================
# Composite Component (Directory)
# ============================================================================


class Directory(FileSystemItem):
    """
    Composite component representing a directory.

    Directories can contain both files and other directories, forming
    a tree structure. Operations on a directory are recursively applied
    to all its children.
    """

    def __init__(self, name: str):
        """
        Initialize a directory.

        Args:
            name: Directory name
        """
        super().__init__(name)
        self._children: List[FileSystemItem] = []

    def add(self, item: FileSystemItem) -> None:
        """
        Add a child item to this directory.

        Args:
            item: File or directory to add

        Raises:
            ValueError: If item with same name already exists
        """
        # Check for duplicate names
        if any(child.name == item.name for child in self._children):
            raise ValueError(f"Item with name '{item.name}' already exists in {self._name}")

        self._children.append(item)
        item._parent = self

    def remove(self, item: FileSystemItem) -> None:
        """
        Remove a child item from this directory.

        Args:
            item: File or directory to remove

        Raises:
            ValueError: If item not found
        """
        try:
            self._children.remove(item)
            item._parent = None
        except ValueError:
            raise ValueError(f"Item '{item.name}' not found in {self._name}")

    def get_child(self, name: str) -> Optional[FileSystemItem]:
        """
        Get a child by name.

        Args:
            name: Name of child to find

        Returns:
            Child item or None if not found
        """
        for child in self._children:
            if child.name == name:
                return child
        return None

    def get_children(self) -> List[FileSystemItem]:
        """
        Get all children.

        Returns:
            List of child items
        """
        return self._children.copy()

    def get_size(self) -> int:
        """
        Get total size of directory and all its contents recursively.

        Returns:
            Total size in bytes of all files in this directory tree
        """
        return sum(child.get_size() for child in self._children)

    def display(self, indent: int = 0) -> str:
        """
        Display directory and all its contents recursively.

        Args:
            indent: Indentation level

        Returns:
            Formatted string showing directory structure
        """
        indent_str = "  " * indent
        result = [f"{indent_str}📁 {self._name}/ ({self.get_size()} bytes)"]

        for child in self._children:
            result.append(child.display(indent + 1))

        return "\n".join(result)

    def count_files(self) -> int:
        """
        Count total number of files in this directory tree.

        Returns:
            Number of files
        """
        count = 0
        for child in self._children:
            if isinstance(child, File):
                count += 1
            elif isinstance(child, Directory):
                count += child.count_files()
        return count

    def count_directories(self) -> int:
        """
        Count total number of subdirectories.

        Returns:
            Number of directories
        """
        count = 0
        for child in self._children:
            if isinstance(child, Directory):
                count += 1 + child.count_directories()
        return count

    def find_by_name(self, name: str) -> List[FileSystemItem]:
        """
        Find all items with given name in this directory tree.

        Args:
            name: Name to search for

        Returns:
            List of matching items
        """
        results = []

        for child in self._children:
            if child.name == name:
                results.append(child)

            if isinstance(child, Directory):
                results.extend(child.find_by_name(name))

        return results

    def find_by_extension(self, extension: str) -> List[File]:
        """
        Find all files with given extension.

        Args:
            extension: File extension (e.g., 'txt', '.txt')

        Returns:
            List of matching files
        """
        if not extension.startswith('.'):
            extension = '.' + extension

        results = []

        for child in self._children:
            if isinstance(child, File) and child.name.endswith(extension):
                results.append(child)
            elif isinstance(child, Directory):
                results.extend(child.find_by_extension(extension))

        return results

    def get_all_files(self) -> List[File]:
        """
        Get all files in this directory tree.

        Returns:
            List of all files
        """
        files = []

        for child in self._children:
            if isinstance(child, File):
                files.append(child)
            elif isinstance(child, Directory):
                files.extend(child.get_all_files())

        return files

    def traverse_depth_first(self) -> Iterator[FileSystemItem]:
        """
        Traverse the tree depth-first (pre-order).

        Yields:
            File system items in depth-first order
        """
        yield self

        for child in self._children:
            if isinstance(child, Directory):
                yield from child.traverse_depth_first()
            else:
                yield child

    def traverse_breadth_first(self) -> Iterator[FileSystemItem]:
        """
        Traverse the tree breadth-first.

        Yields:
            File system items in breadth-first order
        """
        queue = deque([self])

        while queue:
            current = queue.popleft()
            yield current

            if isinstance(current, Directory):
                queue.extend(current._children)

    def is_empty(self) -> bool:
        """
        Check if directory is empty.

        Returns:
            True if directory has no children
        """
        return len(self._children) == 0

    def __len__(self) -> int:
        """Get number of direct children."""
        return len(self._children)

    def __iter__(self) -> Iterator[FileSystemItem]:
        """Iterate over direct children."""
        return iter(self._children)

    def __repr__(self) -> str:
        """String representation of directory."""
        return f"Directory('{self._name}', {len(self._children)} items)"


# ============================================================================
# Utility Functions
# ============================================================================


def calculate_total_size(item: FileSystemItem) -> int:
    """
    Calculate total size of a file system item.

    Demonstrates that client code can treat files and directories uniformly.

    Args:
        item: File or directory

    Returns:
        Total size in bytes
    """
    return item.get_size()


def print_tree(item: FileSystemItem, indent: int = 0) -> None:
    """
    Print file system tree.

    Args:
        item: Root item to print from
        indent: Starting indentation level
    """
    print(item.display(indent))


def find_largest_file(root: Directory) -> Optional[File]:
    """
    Find the largest file in the directory tree.

    Args:
        root: Root directory to search

    Returns:
        Largest file or None if no files exist
    """
    all_files = root.get_all_files()

    if not all_files:
        return None

    return max(all_files, key=lambda f: f.get_size())


def get_statistics(root: Directory) -> dict:
    """
    Get statistics about the directory tree.

    Args:
        root: Root directory

    Returns:
        Dictionary with statistics
    """
    all_files = root.get_all_files()

    return {
        'total_size': root.get_size(),
        'num_files': root.count_files(),
        'num_directories': root.count_directories(),
        'largest_file': find_largest_file(root),
        'average_file_size': sum(f.get_size() for f in all_files) / len(all_files) if all_files else 0
    }


# ============================================================================
# Demonstration Functions
# ============================================================================


def demonstrate_basic_composite():
    """Demonstrate basic composite structure."""
    print("=== Basic Composite Structure ===")

    # Create root directory
    root = Directory("root")

    # Add files to root
    root.add(File("readme.txt", 1024, "Welcome to the project"))
    root.add(File("license.txt", 2048, "MIT License"))

    # Create subdirectory
    src = Directory("src")
    src.add(File("main.py", 5120, "print('Hello, World!')"))
    src.add(File("utils.py", 3072, "def helper(): pass"))

    # Add subdirectory to root
    root.add(src)

    # Display tree
    print(root.display())
    print(f"\nTotal size: {root.get_size()} bytes")
    print()


def demonstrate_deep_nesting():
    """Demonstrate deeply nested directory structure."""
    print("=== Deep Nesting ===")

    # Create nested structure: root/docs/api/v1/
    root = Directory("project")

    docs = Directory("docs")
    api = Directory("api")
    v1 = Directory("v1")

    v1.add(File("endpoints.md", 4096))
    v1.add(File("authentication.md", 2048))

    api.add(v1)
    docs.add(api)
    docs.add(File("readme.md", 1024))

    root.add(docs)

    # Show structure
    print(root.display())
    print()


def demonstrate_uniform_treatment():
    """Demonstrate uniform treatment of files and directories."""
    print("=== Uniform Treatment ===")

    # Create structure
    root = Directory("data")
    root.add(File("file1.txt", 100))

    subdir = Directory("subdir")
    subdir.add(File("file2.txt", 200))
    root.add(subdir)

    # Treat all items uniformly
    items = [root, subdir, File("standalone.txt", 50)]

    print("Calculating sizes uniformly:")
    for item in items:
        print(f"{item.name}: {calculate_total_size(item)} bytes")

    print()


def demonstrate_operations():
    """Demonstrate various composite operations."""
    print("=== Composite Operations ===")

    # Build sample file system
    root = Directory("workspace")

    # Add source files
    src = Directory("src")
    src.add(File("main.py", 5000))
    src.add(File("config.py", 2000))
    src.add(File("utils.py", 3000))
    root.add(src)

    # Add test files
    tests = Directory("tests")
    tests.add(File("test_main.py", 1500))
    tests.add(File("test_utils.py", 1000))
    root.add(tests)

    # Add documentation
    docs = Directory("docs")
    docs.add(File("readme.md", 800))
    docs.add(File("api.md", 1200))
    root.add(docs)

    # Perform operations
    print("--- File Counts ---")
    print(f"Total files: {root.count_files()}")
    print(f"Total directories: {root.count_directories()}")

    print("\n--- Search Operations ---")
    py_files = root.find_by_extension('.py')
    print(f"Python files: {len(py_files)}")
    for file in py_files:
        print(f"  - {file.get_path()}")

    print("\n--- Statistics ---")
    stats = get_statistics(root)
    print(f"Total size: {stats['total_size']} bytes")
    print(f"Files: {stats['num_files']}")
    print(f"Directories: {stats['num_directories']}")
    print(f"Average file size: {stats['average_file_size']:.0f} bytes")
    if stats['largest_file']:
        print(f"Largest file: {stats['largest_file'].name} ({stats['largest_file'].get_size()} bytes)")

    print()


def demonstrate_traversal():
    """Demonstrate different traversal strategies."""
    print("=== Tree Traversal ===")

    # Build tree
    root = Directory("root")

    dir_a = Directory("A")
    dir_a.add(File("a1.txt", 100))
    dir_a.add(File("a2.txt", 200))

    dir_b = Directory("B")
    dir_b.add(File("b1.txt", 150))

    root.add(dir_a)
    root.add(dir_b)
    root.add(File("root.txt", 50))

    print("--- Depth-First Traversal ---")
    for item in root.traverse_depth_first():
        print(f"  {item.name} ({'dir' if item.is_directory() else 'file'})")

    print("\n--- Breadth-First Traversal ---")
    for item in root.traverse_breadth_first():
        print(f"  {item.name} ({'dir' if item.is_directory() else 'file'})")

    print()


def demonstrate_child_management():
    """Demonstrate adding and removing children."""
    print("=== Child Management ===")

    folder = Directory("temp")

    # Add children
    file1 = File("doc1.txt", 100)
    file2 = File("doc2.txt", 200)

    folder.add(file1)
    folder.add(file2)

    print(f"After adding: {len(folder)} items")
    print(folder.display())

    # Remove child
    folder.remove(file1)
    print(f"\nAfter removing doc1.txt: {len(folder)} items")
    print(folder.display())

    # Try to add duplicate
    print("\nTrying to add duplicate...")
    try:
        folder.add(File("doc2.txt", 50))
    except ValueError as e:
        print(f"Error: {e}")

    print()


def demonstrate_paths():
    """Demonstrate path operations."""
    print("=== Path Operations ===")

    root = Directory("home")
    user = Directory("user")
    documents = Directory("documents")

    file = File("report.pdf", 50000)

    documents.add(file)
    user.add(documents)
    root.add(user)

    print(f"Root path: {root.get_path()}")
    print(f"User path: {user.get_path()}")
    print(f"Documents path: {documents.get_path()}")
    print(f"File path: {file.get_path()}")

    print()


def demonstrate_search():
    """Demonstrate search operations."""
    print("=== Search Operations ===")

    root = Directory("projects")

    # Create multiple files with same name in different locations
    proj1 = Directory("project1")
    proj1.add(File("config.json", 512))
    proj1.add(File("main.py", 1024))

    proj2 = Directory("project2")
    proj2.add(File("config.json", 768))
    proj2.add(File("app.py", 2048))

    root.add(proj1)
    root.add(proj2)

    # Search by name
    print("--- Finding all 'config.json' files ---")
    configs = root.find_by_name("config.json")
    for config in configs:
        print(f"  {config.get_path()} - {config.get_size()} bytes")

    # Search by extension
    print("\n--- Finding all Python files ---")
    py_files = root.find_by_extension('.py')
    for py_file in py_files:
        print(f"  {py_file.get_path()}")

    print()


def demonstrate_real_world_example():
    """Demonstrate a realistic project structure."""
    print("=== Real-World Project Structure ===")

    # Create a typical web application structure
    project = Directory("web-app")

    # Source code
    src = Directory("src")

    models = Directory("models")
    models.add(File("user.py", 3500))
    models.add(File("product.py", 2800))
    models.add(File("order.py", 4200))

    views = Directory("views")
    views.add(File("home.py", 1500))
    views.add(File("product.py", 2200))

    controllers = Directory("controllers")
    controllers.add(File("auth.py", 3000))
    controllers.add(File("api.py", 5500))

    src.add(models)
    src.add(views)
    src.add(controllers)
    src.add(File("__init__.py", 100))
    src.add(File("app.py", 2000))

    # Tests
    tests = Directory("tests")
    tests.add(File("test_models.py", 2500))
    tests.add(File("test_views.py", 1800))
    tests.add(File("test_api.py", 3200))

    # Static files
    static = Directory("static")
    css = Directory("css")
    css.add(File("styles.css", 8000))
    css.add(File("responsive.css", 4500))

    js = Directory("js")
    js.add(File("app.js", 12000))
    js.add(File("utils.js", 6000))

    static.add(css)
    static.add(js)

    # Documentation
    docs = Directory("docs")
    docs.add(File("README.md", 2500))
    docs.add(File("API.md", 5000))
    docs.add(File("CONTRIBUTING.md", 1800))

    # Root files
    project.add(File("requirements.txt", 500))
    project.add(File(".gitignore", 300))
    project.add(File("LICENSE", 1100))

    # Assemble project
    project.add(src)
    project.add(tests)
    project.add(static)
    project.add(docs)

    # Display and analyze
    print(project.display())

    print("\n--- Project Statistics ---")
    stats = get_statistics(project)
    print(f"Total size: {stats['total_size']:,} bytes")
    print(f"Total files: {stats['num_files']}")
    print(f"Total directories: {stats['num_directories']}")

    print("\n--- File Type Distribution ---")
    py_files = project.find_by_extension('.py')
    md_files = project.find_by_extension('.md')
    css_files = project.find_by_extension('.css')
    js_files = project.find_by_extension('.js')

    print(f"Python files: {len(py_files)} ({sum(f.get_size() for f in py_files):,} bytes)")
    print(f"Markdown files: {len(md_files)} ({sum(f.get_size() for f in md_files):,} bytes)")
    print(f"CSS files: {len(css_files)} ({sum(f.get_size() for f in css_files):,} bytes)")
    print(f"JavaScript files: {len(js_files)} ({sum(f.get_size() for f in js_files):,} bytes)")

    print()


# ============================================================================
# Main Function
# ============================================================================


def main():
    """Run all demonstrations of the Composite Pattern."""
    print("Composite Pattern Example: File System Hierarchy\n")

    demonstrate_basic_composite()
    demonstrate_deep_nesting()
    demonstrate_uniform_treatment()
    demonstrate_operations()
    demonstrate_traversal()
    demonstrate_child_management()
    demonstrate_paths()
    demonstrate_search()
    demonstrate_real_world_example()

    print("All demonstrations completed successfully!")


if __name__ == "__main__":
    main()
