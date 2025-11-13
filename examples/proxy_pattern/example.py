"""
Proxy Pattern Example: Image Loading and Access Control

This example demonstrates the Proxy Pattern with three types of proxies:
1. Virtual Proxy - Lazy loading of images
2. Protection Proxy - Access control for sensitive documents
3. Cache Proxy - Caching expensive database queries

Key features:
- Multiple proxy types (Virtual, Protection, Cache)
- Lazy initialization
- Access control with permissions
- Result caching
- Performance measurement
- Type hints and comprehensive documentation

SOLID Principles Demonstrated:
- Single Responsibility: Each proxy type has one clear purpose
- Open/Closed: New proxy types can be added without modifying existing code
- Liskov Substitution: Proxies are substitutable for real objects
- Interface Segregation: Clean interfaces for each component
- Dependency Inversion: Clients depend on abstractions (protocols)
"""

from abc import ABC, abstractmethod
from typing import Protocol, Optional, Dict, Any, List
from dataclasses import dataclass
from enum import Enum
import time


# ============================================================================
# VIRTUAL PROXY - Lazy Loading
# ============================================================================


class Image(ABC):
    """
    Abstract interface for images.

    This ensures proxies and real images have the same interface.
    """

    @abstractmethod
    def display(self) -> None:
        """Display the image."""
        pass

    @abstractmethod
    def get_info(self) -> str:
        """Get image information."""
        pass


class RealImage(Image):
    """
    Real image that performs expensive loading operation.

    This class simulates loading a large image file from disk,
    which is an expensive operation.
    """

    def __init__(self, filename: str):
        """
        Initialize and load image from disk.

        Args:
            filename: Path to image file
        """
        self.filename = filename
        self._load_from_disk()

    def _load_from_disk(self) -> None:
        """
        Simulate expensive image loading operation.

        In real application, this would:
        - Read file from disk
        - Decode image format
        - Allocate memory for pixel data
        - Load textures to GPU
        """
        print(f"[RealImage] Loading '{self.filename}' from disk...")
        time.sleep(0.5)  # Simulate expensive I/O operation
        print(f"[RealImage] '{self.filename}' loaded successfully")

    def display(self) -> None:
        """Display the image."""
        print(f"[RealImage] Displaying '{self.filename}'")

    def get_info(self) -> str:
        """Get image information."""
        return f"RealImage: {self.filename}"


class ImageProxy(Image):
    """
    Virtual proxy for lazy loading images.

    The proxy delays creating the real image until it's actually needed.
    This improves performance when dealing with many images that might
    not all be displayed.

    Demonstrates:
    - Virtual proxy pattern
    - Lazy initialization
    - Transparent delegation
    """

    def __init__(self, filename: str):
        """
        Initialize proxy without loading image.

        Args:
            filename: Path to image file
        """
        self.filename = filename
        self._real_image: Optional[RealImage] = None
        print(f"[ImageProxy] Created proxy for '{self.filename}' (not loaded yet)")

    def _get_real_image(self) -> RealImage:
        """
        Get or create the real image (lazy loading).

        Returns:
            The real image instance
        """
        if self._real_image is None:
            print(f"[ImageProxy] First access to '{self.filename}', loading now...")
            self._real_image = RealImage(self.filename)
        return self._real_image

    def display(self) -> None:
        """Display the image (loads if not already loaded)."""
        self._get_real_image().display()

    def get_info(self) -> str:
        """Get image information without loading the image."""
        loaded_status = "loaded" if self._real_image else "not loaded"
        return f"ImageProxy: {self.filename} ({loaded_status})"


# ============================================================================
# PROTECTION PROXY - Access Control
# ============================================================================


class AccessLevel(Enum):
    """Access levels for documents."""
    PUBLIC = 1
    CONFIDENTIAL = 2
    SECRET = 3
    TOP_SECRET = 4


@dataclass
class User:
    """
    User with access level.

    Attributes:
        username: User's name
        access_level: Maximum access level for this user
    """
    username: str
    access_level: AccessLevel


class Document(ABC):
    """Abstract interface for documents."""

    @abstractmethod
    def read(self) -> str:
        """Read document content."""
        pass

    @abstractmethod
    def write(self, content: str) -> None:
        """Write content to document."""
        pass

    @abstractmethod
    def get_classification(self) -> AccessLevel:
        """Get document classification level."""
        pass


class RealDocument(Document):
    """
    Real document containing sensitive information.

    This class has no access control - it's the proxy's responsibility
    to enforce security.
    """

    def __init__(self, title: str, content: str, classification: AccessLevel):
        """
        Initialize document.

        Args:
            title: Document title
            content: Document content
            classification: Security classification level
        """
        self.title = title
        self._content = content
        self.classification = classification

    def read(self) -> str:
        """Read document content."""
        return self._content

    def write(self, content: str) -> None:
        """Write content to document."""
        self._content = content
        print(f"[RealDocument] Content written to '{self.title}'")

    def get_classification(self) -> AccessLevel:
        """Get document classification level."""
        return self.classification


class DocumentProxy(Document):
    """
    Protection proxy that enforces access control.

    This proxy checks user permissions before allowing access
    to the real document.

    Demonstrates:
    - Protection proxy pattern
    - Access control
    - Security checks before delegation
    """

    def __init__(self, real_document: RealDocument, user: User):
        """
        Initialize document proxy with access control.

        Args:
            real_document: The real document to protect
            user: The user accessing the document
        """
        self._real_document = real_document
        self._user = user

    def _check_read_access(self) -> bool:
        """
        Check if user has read access.

        Returns:
            True if access granted, False otherwise
        """
        has_access = self._user.access_level.value >= self._real_document.classification.value
        if not has_access:
            print(f"[DocumentProxy] ⛔ Access DENIED for {self._user.username} "
                  f"(Level {self._user.access_level.name}) to read "
                  f"{self._real_document.classification.name} document")
        return has_access

    def _check_write_access(self) -> bool:
        """
        Check if user has write access.

        Write access requires higher privileges than read access.

        Returns:
            True if access granted, False otherwise
        """
        # Write requires at least one level higher than document classification
        required_level = min(self._real_document.classification.value + 1, 4)
        has_access = self._user.access_level.value >= required_level
        if not has_access:
            print(f"[DocumentProxy] ⛔ Access DENIED for {self._user.username} "
                  f"to write to {self._real_document.classification.name} document")
        return has_access

    def read(self) -> str:
        """
        Read document if user has sufficient access.

        Returns:
            Document content if access granted

        Raises:
            PermissionError: If user lacks read access
        """
        if self._check_read_access():
            print(f"[DocumentProxy] ✅ Access GRANTED for {self._user.username} to read")
            return self._real_document.read()
        else:
            raise PermissionError(f"User {self._user.username} cannot read this document")

    def write(self, content: str) -> None:
        """
        Write to document if user has sufficient access.

        Args:
            content: Content to write

        Raises:
            PermissionError: If user lacks write access
        """
        if self._check_write_access():
            print(f"[DocumentProxy] ✅ Access GRANTED for {self._user.username} to write")
            self._real_document.write(content)
        else:
            raise PermissionError(f"User {self._user.username} cannot write to this document")

    def get_classification(self) -> AccessLevel:
        """Get document classification level."""
        return self._real_document.get_classification()


# ============================================================================
# CACHE PROXY - Result Caching
# ============================================================================


class DatabaseQuery(Protocol):
    """Protocol for database query objects."""

    def execute(self, query: str) -> List[Dict[str, Any]]:
        """Execute a database query."""
        ...


class RealDatabase:
    """
    Real database that performs expensive queries.

    Simulates a database with slow query execution.
    """

    def __init__(self, name: str):
        """
        Initialize database.

        Args:
            name: Database name
        """
        self.name = name
        self._data = self._initialize_data()

    def _initialize_data(self) -> List[Dict[str, Any]]:
        """Initialize sample data."""
        return [
            {"id": 1, "name": "Alice", "department": "Engineering"},
            {"id": 2, "name": "Bob", "department": "Sales"},
            {"id": 3, "name": "Charlie", "department": "Engineering"},
            {"id": 4, "name": "Diana", "department": "Marketing"},
            {"id": 5, "name": "Eve", "department": "Engineering"},
        ]

    def execute(self, query: str) -> List[Dict[str, Any]]:
        """
        Execute a database query (slow operation).

        Args:
            query: SQL-like query string

        Returns:
            Query results
        """
        print(f"[RealDatabase] Executing query: {query}")
        time.sleep(0.3)  # Simulate slow database query

        # Simple query parsing (just for demonstration)
        if "Engineering" in query:
            results = [row for row in self._data if row["department"] == "Engineering"]
        elif "Sales" in query:
            results = [row for row in self._data if row["department"] == "Sales"]
        else:
            results = self._data

        print(f"[RealDatabase] Query returned {len(results)} results")
        return results


class CachingDatabaseProxy:
    """
    Cache proxy that caches database query results.

    This proxy caches query results to avoid repeated expensive
    database operations for the same queries.

    Demonstrates:
    - Cache proxy pattern
    - Result caching
    - Performance optimization
    """

    def __init__(self, real_database: RealDatabase):
        """
        Initialize caching proxy.

        Args:
            real_database: The real database to proxy
        """
        self._real_database = real_database
        self._cache: Dict[str, List[Dict[str, Any]]] = {}
        self._cache_hits = 0
        self._cache_misses = 0

    def execute(self, query: str) -> List[Dict[str, Any]]:
        """
        Execute query with caching.

        Args:
            query: SQL-like query string

        Returns:
            Query results (from cache or database)
        """
        if query in self._cache:
            self._cache_hits += 1
            print(f"[CachingProxy] 🎯 Cache HIT for query: {query}")
            return self._cache[query]
        else:
            self._cache_misses += 1
            print(f"[CachingProxy] ❌ Cache MISS for query: {query}")
            results = self._real_database.execute(query)
            self._cache[query] = results
            return results

    def get_cache_stats(self) -> Dict[str, int]:
        """
        Get cache statistics.

        Returns:
            Dictionary with cache hit/miss statistics
        """
        total = self._cache_hits + self._cache_misses
        hit_rate = (self._cache_hits / total * 100) if total > 0 else 0
        return {
            "hits": self._cache_hits,
            "misses": self._cache_misses,
            "hit_rate": hit_rate,
            "cached_queries": len(self._cache)
        }

    def clear_cache(self) -> None:
        """Clear the cache."""
        self._cache.clear()
        print("[CachingProxy] Cache cleared")


# ============================================================================
# DEMONSTRATIONS
# ============================================================================


def demonstrate_virtual_proxy():
    """Demonstrate lazy loading with virtual proxy."""
    print("=== VIRTUAL PROXY (Lazy Loading) ===\n")

    # Create proxies for multiple images (fast)
    print("Creating image proxies (no loading yet):")
    images = [
        ImageProxy("photo1.jpg"),
        ImageProxy("photo2.jpg"),
        ImageProxy("photo3.jpg")
    ]
    print()

    # Display info without loading
    print("Getting info (without loading):")
    for img in images:
        print(f"  {img.get_info()}")
    print()

    # Display only first image (only this one gets loaded)
    print("Displaying only first image:")
    images[0].display()
    print()

    # Display first image again (already loaded, no loading delay)
    print("Displaying first image again (already loaded):")
    images[0].display()
    print()

    # Check info again
    print("Info after partial loading:")
    for img in images:
        print(f"  {img.get_info()}")
    print()


def demonstrate_protection_proxy():
    """Demonstrate access control with protection proxy."""
    print("=== PROTECTION PROXY (Access Control) ===\n")

    # Create users with different access levels
    public_user = User("john_public", AccessLevel.PUBLIC)
    confidential_user = User("jane_confidential", AccessLevel.CONFIDENTIAL)
    secret_user = User("admin_secret", AccessLevel.SECRET)
    top_secret_user = User("director", AccessLevel.TOP_SECRET)

    # Create documents with different classifications
    public_doc = RealDocument(
        "Company Newsletter",
        "Welcome to our monthly newsletter...",
        AccessLevel.PUBLIC
    )

    secret_doc = RealDocument(
        "Project Plans",
        "Top secret project information...",
        AccessLevel.SECRET
    )

    print("1. Public user trying to read PUBLIC document:")
    proxy = DocumentProxy(public_doc, public_user)
    try:
        content = proxy.read()
        print(f"   Content: {content[:30]}...\n")
    except PermissionError as e:
        print(f"   Error: {e}\n")

    print("2. Public user trying to read SECRET document:")
    proxy = DocumentProxy(secret_doc, public_user)
    try:
        content = proxy.read()
        print(f"   Content: {content}\n")
    except PermissionError as e:
        print(f"   Error: {e}\n")

    print("3. Secret user trying to read SECRET document:")
    proxy = DocumentProxy(secret_doc, secret_user)
    try:
        content = proxy.read()
        print(f"   Content: {content[:30]}...\n")
    except PermissionError as e:
        print(f"   Error: {e}\n")

    print("4. Secret user trying to WRITE to SECRET document:")
    proxy = DocumentProxy(secret_doc, secret_user)
    try:
        proxy.write("Updated secret content")
        print()
    except PermissionError as e:
        print(f"   Error: {e}\n")

    print("5. Top Secret user trying to WRITE to SECRET document:")
    proxy = DocumentProxy(secret_doc, top_secret_user)
    try:
        proxy.write("Updated secret content")
        print()
    except PermissionError as e:
        print(f"   Error: {e}\n")


def demonstrate_cache_proxy():
    """Demonstrate result caching with cache proxy."""
    print("=== CACHE PROXY (Result Caching) ===\n")

    # Create database and caching proxy
    db = RealDatabase("EmployeeDB")
    cache_proxy = CachingDatabaseProxy(db)

    # Execute same query multiple times
    print("Executing query for first time:")
    results1 = cache_proxy.execute("SELECT * FROM employees WHERE department='Engineering'")
    print(f"Results: {len(results1)} employees\n")

    print("Executing SAME query again:")
    results2 = cache_proxy.execute("SELECT * FROM employees WHERE department='Engineering'")
    print(f"Results: {len(results2)} employees\n")

    print("Executing SAME query third time:")
    results3 = cache_proxy.execute("SELECT * FROM employees WHERE department='Engineering'")
    print(f"Results: {len(results3)} employees\n")

    print("Executing DIFFERENT query:")
    results4 = cache_proxy.execute("SELECT * FROM employees WHERE department='Sales'")
    print(f"Results: {len(results4)} employees\n")

    print("Executing first query again:")
    results5 = cache_proxy.execute("SELECT * FROM employees WHERE department='Engineering'")
    print(f"Results: {len(results5)} employees\n")

    # Show cache statistics
    stats = cache_proxy.get_cache_stats()
    print("Cache Statistics:")
    print(f"  Total queries: {stats['hits'] + stats['misses']}")
    print(f"  Cache hits: {stats['hits']}")
    print(f"  Cache misses: {stats['misses']}")
    print(f"  Hit rate: {stats['hit_rate']:.1f}%")
    print(f"  Cached queries: {stats['cached_queries']}")
    print()


def demonstrate_performance_comparison():
    """Compare performance with and without proxies."""
    print("=== PERFORMANCE COMPARISON ===\n")

    print("1. Virtual Proxy Performance:\n")

    # Without proxy - all images loaded immediately
    print("Without proxy (loading 5 images immediately):")
    start = time.time()
    real_images = [RealImage(f"photo{i}.jpg") for i in range(5)]
    load_time = time.time() - start
    print(f"Total time: {load_time:.3f}s\n")

    # With proxy - images loaded only when accessed
    print("With proxy (creating 5 proxies, accessing only 1):")
    start = time.time()
    proxy_images = [ImageProxy(f"photo{i}.jpg") for i in range(5)]
    proxy_images[0].display()  # Only load one
    proxy_time = time.time() - start
    print(f"Total time: {proxy_time:.3f}s\n")

    print(f"Speedup: {load_time/proxy_time:.2f}x faster with proxy\n")


def main():
    """Run all demonstrations."""
    print("Proxy Pattern Example: Multiple Proxy Types\n")
    print("=" * 60 + "\n")

    demonstrate_virtual_proxy()
    print("=" * 60 + "\n")

    demonstrate_protection_proxy()
    print("=" * 60 + "\n")

    demonstrate_cache_proxy()
    print("=" * 60 + "\n")

    demonstrate_performance_comparison()
    print("=" * 60)

    print("\nAll demonstrations completed successfully!")


if __name__ == "__main__":
    main()
