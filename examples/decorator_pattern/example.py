"""
Decorator Pattern Example: Data Stream Processing

This example demonstrates the Decorator Pattern using a data stream processing
system that dynamically adds functionality to data streams. The pattern allows
behaviors like encryption, compression, logging, and validation to be added
or removed at runtime without modifying the core stream classes.

Key features:
- Classic OOP decorator pattern with component interface
- Multiple concrete decorators for different behaviors
- Decorator stacking and composition
- Type hints and comprehensive documentation
- Adherence to Open/Closed and Single Responsibility Principles
- Both synchronous decorators and stateful decorators
"""

from abc import ABC, abstractmethod
from typing import Protocol, Optional, List
import hashlib
import base64
import time
from datetime import datetime
import zlib


# ============================================================================
# Component Interface (What can be decorated)
# ============================================================================


class DataStream(Protocol):
    """
    Protocol defining the interface for data streams.

    This is the component interface that both concrete components
    and decorators must implement, ensuring they are interchangeable.
    """

    def write(self, data: str) -> None:
        """
        Write data to the stream.

        Args:
            data: String data to write
        """
        ...

    def read(self) -> str:
        """
        Read data from the stream.

        Returns:
            String data from the stream
        """
        ...


# ============================================================================
# Concrete Components (Base implementations)
# ============================================================================


class MemoryStream:
    """
    Concrete component: In-memory data stream.

    This is the basic component that stores data in memory.
    It can be used alone or wrapped with decorators.
    """

    def __init__(self):
        """Initialize an empty memory stream."""
        self._buffer: str = ""

    def write(self, data: str) -> None:
        """
        Write data to memory buffer.

        Args:
            data: String data to write
        """
        self._buffer += data

    def read(self) -> str:
        """
        Read all data from memory buffer.

        Returns:
            All data in the buffer
        """
        return self._buffer

    def clear(self) -> None:
        """Clear the buffer."""
        self._buffer = ""


class FileStream:
    """
    Concrete component: File-based data stream.

    This component writes data to a file. In a real implementation,
    this would handle actual file I/O.
    """

    def __init__(self, filename: str):
        """
        Initialize file stream.

        Args:
            filename: Name of the file to write to
        """
        self._filename = filename
        self._data: str = ""

    def write(self, data: str) -> None:
        """
        Write data to file (simulated).

        Args:
            data: String data to write
        """
        self._data += data
        # In real implementation: write to actual file

    def read(self) -> str:
        """
        Read data from file (simulated).

        Returns:
            Data from the file
        """
        # In real implementation: read from actual file
        return self._data

    @property
    def filename(self) -> str:
        """Get the filename."""
        return self._filename


# ============================================================================
# Decorator Base Class
# ============================================================================


class StreamDecorator(ABC):
    """
    Base decorator class for data streams.

    This abstract base class provides the common structure for all
    stream decorators. It wraps a DataStream component and delegates
    operations to it while allowing subclasses to add behavior.

    Follows the Decorator pattern by implementing the same interface
    as the component it wraps.
    """

    def __init__(self, stream: DataStream):
        """
        Initialize decorator with a stream to wrap.

        Args:
            stream: DataStream component to decorate
        """
        self._wrapped_stream = stream

    @abstractmethod
    def write(self, data: str) -> None:
        """
        Write data to the decorated stream.

        Args:
            data: String data to write
        """
        pass

    @abstractmethod
    def read(self) -> str:
        """
        Read data from the decorated stream.

        Returns:
            String data from the stream
        """
        pass


# ============================================================================
# Concrete Decorators (Add specific behaviors)
# ============================================================================


class EncryptionDecorator(StreamDecorator):
    """
    Decorator that adds encryption/decryption to a stream.

    This decorator encrypts data on write and decrypts on read,
    demonstrating how decorators can transform data.
    Uses simple base64 encoding for demonstration (not secure encryption).
    """

    def __init__(self, stream: DataStream, key: str = "secret"):
        """
        Initialize encryption decorator.

        Args:
            stream: DataStream to wrap
            key: Encryption key (for demonstration)
        """
        super().__init__(stream)
        self._key = key

    def write(self, data: str) -> None:
        """
        Encrypt data before writing to wrapped stream.

        Args:
            data: Plain text data to encrypt and write
        """
        encrypted = self._encrypt(data)
        self._wrapped_stream.write(encrypted)

    def read(self) -> str:
        """
        Read and decrypt data from wrapped stream.

        Returns:
            Decrypted data
        """
        encrypted_data = self._wrapped_stream.read()
        return self._decrypt(encrypted_data)

    def _encrypt(self, data: str) -> str:
        """
        Encrypt data (simple base64 for demonstration).

        Args:
            data: Plain text to encrypt

        Returns:
            Encrypted data
        """
        # Simple XOR with key for demonstration
        encrypted_bytes = bytes([ord(c) ^ ord(self._key[i % len(self._key)])
                                for i, c in enumerate(data)])
        return base64.b64encode(encrypted_bytes).decode('utf-8')

    def _decrypt(self, data: str) -> str:
        """
        Decrypt data.

        Args:
            data: Encrypted data

        Returns:
            Decrypted plain text
        """
        if not data:
            return ""
        try:
            encrypted_bytes = base64.b64decode(data)
            decrypted = ''.join([chr(b ^ ord(self._key[i % len(self._key)]))
                                for i, b in enumerate(encrypted_bytes)])
            return decrypted
        except Exception:
            return ""


class CompressionDecorator(StreamDecorator):
    """
    Decorator that adds compression/decompression to a stream.

    This decorator compresses data on write and decompresses on read,
    demonstrating how decorators can optimize data storage.
    """

    def write(self, data: str) -> None:
        """
        Compress data before writing to wrapped stream.

        Args:
            data: Uncompressed data to compress and write
        """
        compressed = self._compress(data)
        self._wrapped_stream.write(compressed)

    def read(self) -> str:
        """
        Read and decompress data from wrapped stream.

        Returns:
            Decompressed data
        """
        compressed_data = self._wrapped_stream.read()
        return self._decompress(compressed_data)

    def _compress(self, data: str) -> str:
        """
        Compress data using zlib.

        Args:
            data: Uncompressed string

        Returns:
            Base64-encoded compressed data
        """
        compressed_bytes = zlib.compress(data.encode('utf-8'))
        return base64.b64encode(compressed_bytes).decode('utf-8')

    def _decompress(self, data: str) -> str:
        """
        Decompress data using zlib.

        Args:
            data: Base64-encoded compressed data

        Returns:
            Decompressed string
        """
        if not data:
            return ""
        try:
            compressed_bytes = base64.b64decode(data)
            decompressed_bytes = zlib.decompress(compressed_bytes)
            return decompressed_bytes.decode('utf-8')
        except Exception:
            return ""


class LoggingDecorator(StreamDecorator):
    """
    Decorator that adds logging to stream operations.

    This decorator logs all write and read operations,
    demonstrating how decorators can add cross-cutting concerns
    without modifying the core functionality.
    """

    def __init__(self, stream: DataStream, prefix: str = "LOG"):
        """
        Initialize logging decorator.

        Args:
            stream: DataStream to wrap
            prefix: Prefix for log messages
        """
        super().__init__(stream)
        self._prefix = prefix
        self._log_entries: List[str] = []

    def write(self, data: str) -> None:
        """
        Log write operation and delegate to wrapped stream.

        Args:
            data: Data to write
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{self._prefix}] {timestamp} - WRITE: {len(data)} bytes"
        self._log_entries.append(log_entry)
        print(log_entry)
        self._wrapped_stream.write(data)

    def read(self) -> str:
        """
        Log read operation and delegate to wrapped stream.

        Returns:
            Data from wrapped stream
        """
        data = self._wrapped_stream.read()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{self._prefix}] {timestamp} - READ: {len(data)} bytes"
        self._log_entries.append(log_entry)
        print(log_entry)
        return data

    def get_logs(self) -> List[str]:
        """
        Get all log entries.

        Returns:
            List of log entries
        """
        return self._log_entries.copy()


class ValidationDecorator(StreamDecorator):
    """
    Decorator that adds validation to stream operations.

    This decorator validates data before writing and after reading,
    demonstrating how decorators can enforce business rules.
    """

    def __init__(self, stream: DataStream, max_size: int = 1000):
        """
        Initialize validation decorator.

        Args:
            stream: DataStream to wrap
            max_size: Maximum allowed data size in bytes
        """
        super().__init__(stream)
        self._max_size = max_size

    def write(self, data: str) -> None:
        """
        Validate data before writing to wrapped stream.

        Args:
            data: Data to validate and write

        Raises:
            ValueError: If data is invalid
        """
        self._validate_data(data)
        self._wrapped_stream.write(data)

    def read(self) -> str:
        """
        Read and validate data from wrapped stream.

        Returns:
            Validated data

        Raises:
            ValueError: If data is invalid
        """
        data = self._wrapped_stream.read()
        self._validate_data(data)
        return data

    def _validate_data(self, data: str) -> None:
        """
        Validate data against rules.

        Args:
            data: Data to validate

        Raises:
            ValueError: If data is invalid
        """
        if not data:
            return

        if len(data) > self._max_size:
            raise ValueError(
                f"Data size ({len(data)} bytes) exceeds maximum ({self._max_size} bytes)"
            )

        # Could add more validation rules here


class ChecksumDecorator(StreamDecorator):
    """
    Decorator that adds checksum verification to a stream.

    This decorator calculates and verifies checksums to ensure
    data integrity, demonstrating stateful decorators.
    """

    def __init__(self, stream: DataStream):
        """
        Initialize checksum decorator.

        Args:
            stream: DataStream to wrap
        """
        super().__init__(stream)
        self._write_checksum: Optional[str] = None

    def write(self, data: str) -> None:
        """
        Calculate checksum and write data with checksum.

        Args:
            data: Data to write
        """
        self._write_checksum = self._calculate_checksum(data)
        # In a real implementation, might append checksum to data
        self._wrapped_stream.write(data)

    def read(self) -> str:
        """
        Read data and verify checksum.

        Returns:
            Data from stream

        Raises:
            ValueError: If checksum doesn't match
        """
        data = self._wrapped_stream.read()
        if self._write_checksum:
            current_checksum = self._calculate_checksum(data)
            if current_checksum != self._write_checksum:
                raise ValueError(
                    f"Checksum mismatch! Expected {self._write_checksum}, "
                    f"got {current_checksum}"
                )
        return data

    def _calculate_checksum(self, data: str) -> str:
        """
        Calculate SHA-256 checksum of data.

        Args:
            data: Data to checksum

        Returns:
            Hexadecimal checksum string
        """
        return hashlib.sha256(data.encode('utf-8')).hexdigest()

    def get_checksum(self) -> Optional[str]:
        """
        Get the stored checksum.

        Returns:
            Checksum string or None
        """
        return self._write_checksum


class TimestampDecorator(StreamDecorator):
    """
    Decorator that adds timestamp metadata to stream operations.

    This decorator tracks when data was written and read,
    demonstrating metadata addition.
    """

    def __init__(self, stream: DataStream):
        """
        Initialize timestamp decorator.

        Args:
            stream: DataStream to wrap
        """
        super().__init__(stream)
        self._write_time: Optional[float] = None
        self._read_time: Optional[float] = None

    def write(self, data: str) -> None:
        """
        Record write timestamp and delegate to wrapped stream.

        Args:
            data: Data to write
        """
        self._write_time = time.time()
        self._wrapped_stream.write(data)

    def read(self) -> str:
        """
        Record read timestamp and delegate to wrapped stream.

        Returns:
            Data from wrapped stream
        """
        self._read_time = time.time()
        return self._wrapped_stream.read()

    def get_write_timestamp(self) -> Optional[str]:
        """
        Get formatted write timestamp.

        Returns:
            Formatted timestamp or None
        """
        if self._write_time:
            return datetime.fromtimestamp(self._write_time).strftime("%Y-%m-%d %H:%M:%S.%f")
        return None

    def get_read_timestamp(self) -> Optional[str]:
        """
        Get formatted read timestamp.

        Returns:
            Formatted timestamp or None
        """
        if self._read_time:
            return datetime.fromtimestamp(self._read_time).strftime("%Y-%m-%d %H:%M:%S.%f")
        return None


# ============================================================================
# Demonstration Functions
# ============================================================================


def demonstrate_basic_decorator():
    """Demonstrate basic decorator usage."""
    print("=== Basic Decorator Usage ===")

    # Create base stream
    stream = MemoryStream()

    # Wrap with single decorator
    encrypted_stream = EncryptionDecorator(stream, key="mykey")

    # Use the decorated stream
    encrypted_stream.write("Hello, World!")
    print(f"Stored (encrypted): {stream.read()}")
    print(f"Retrieved (decrypted): {encrypted_stream.read()}")
    print()


def demonstrate_stacked_decorators():
    """Demonstrate stacking multiple decorators."""
    print("=== Stacked Decorators ===")

    # Create base stream
    stream = MemoryStream()

    # Stack multiple decorators
    # Order: Base -> Compression -> Encryption -> Logging
    decorated_stream = LoggingDecorator(
        EncryptionDecorator(
            CompressionDecorator(stream),
            key="secret"
        ),
        prefix="STACK"
    )

    # Write data (goes through all decorators)
    print("Writing data...")
    decorated_stream.write("This is a test message that will be compressed and encrypted!")

    print("\nReading data...")
    result = decorated_stream.read()
    print(f"Final result: {result}")
    print()


def demonstrate_logging_decorator():
    """Demonstrate logging decorator functionality."""
    print("=== Logging Decorator ===")

    stream = MemoryStream()
    logged_stream = LoggingDecorator(stream, prefix="DEMO")

    logged_stream.write("First message")
    logged_stream.write("Second message")
    data = logged_stream.read()

    print(f"\nFinal data: {data}")
    print(f"\nAll logs: {len(logged_stream.get_logs())} entries")
    print()


def demonstrate_validation_decorator():
    """Demonstrate validation decorator with error handling."""
    print("=== Validation Decorator ===")

    stream = MemoryStream()
    validated_stream = ValidationDecorator(stream, max_size=50)

    # Valid write
    print("Writing valid data...")
    validated_stream.write("Short message")
    print("Success!")

    # Invalid write
    print("\nWriting invalid data (too large)...")
    try:
        validated_stream.write("x" * 100)
    except ValueError as e:
        print(f"Validation error: {e}")
    print()


def demonstrate_checksum_decorator():
    """Demonstrate checksum verification."""
    print("=== Checksum Decorator ===")

    stream = MemoryStream()
    checksum_stream = ChecksumDecorator(stream)

    # Write data
    message = "Important data that must not be corrupted"
    checksum_stream.write(message)
    print(f"Written: {message}")
    print(f"Checksum: {checksum_stream.get_checksum()}")

    # Read and verify
    print("\nReading with checksum verification...")
    result = checksum_stream.read()
    print(f"Read: {result}")
    print("Checksum verified successfully!")

    # Demonstrate corruption detection
    print("\nSimulating data corruption...")
    stream._buffer = "Corrupted data"
    try:
        result = checksum_stream.read()
    except ValueError as e:
        print(f"Corruption detected: {e}")
    print()


def demonstrate_complex_composition():
    """Demonstrate complex decorator composition."""
    print("=== Complex Decorator Composition ===")

    # Create a fully decorated stream with all features
    stream = MemoryStream()

    # Build decorator stack: Base -> Validation -> Checksum -> Compression -> Encryption -> Timestamp -> Logging
    decorated_stream = LoggingDecorator(
        TimestampDecorator(
            EncryptionDecorator(
                CompressionDecorator(
                    ChecksumDecorator(
                        ValidationDecorator(stream, max_size=500)
                    )
                ),
                key="secure123"
            )
        ),
        prefix="FULL"
    )

    # Use the fully decorated stream
    print("Writing to fully decorated stream...")
    message = "This message goes through validation, checksum, compression, encryption, timestamp, and logging!"
    decorated_stream.write(message)

    print("\nReading from fully decorated stream...")
    result = decorated_stream.read()
    print(f"Final result: {result}")

    # Access timestamp decorator features (if we had a reference)
    print(f"\nMessage verified through all layers successfully!")
    print()


def demonstrate_different_components():
    """Demonstrate decorating different component types."""
    print("=== Different Component Types ===")

    # Decorate memory stream
    print("--- Memory Stream with Encryption ---")
    memory_stream = EncryptionDecorator(MemoryStream(), key="mem")
    memory_stream.write("Memory data")
    print(f"Memory: {memory_stream.read()}")

    # Decorate file stream
    print("\n--- File Stream with Compression ---")
    file_stream = CompressionDecorator(FileStream("data.txt"))
    file_stream.write("File data that will be compressed")
    print(f"File: {file_stream.read()}")
    print()


def demonstrate_decorator_independence():
    """Demonstrate that decorators can be used independently."""
    print("=== Decorator Independence ===")

    base = MemoryStream()

    # Create different decorated versions
    encrypted = EncryptionDecorator(MemoryStream(), key="key1")
    compressed = CompressionDecorator(MemoryStream())
    logged = LoggingDecorator(MemoryStream(), prefix="IND")

    # Each works independently
    encrypted.write("Secret")
    compressed.write("Big data")
    logged.write("Tracked data")

    print("All decorators work independently!")
    print()


def demonstrate_runtime_composition():
    """Demonstrate composing decorators at runtime based on needs."""
    print("=== Runtime Decorator Composition ===")

    def create_stream(needs_encryption: bool, needs_compression: bool, needs_logging: bool) -> DataStream:
        """
        Create a stream with decorators based on requirements.

        Args:
            needs_encryption: Whether to add encryption
            needs_compression: Whether to add compression
            needs_logging: Whether to add logging

        Returns:
            Decorated stream based on requirements
        """
        stream: DataStream = MemoryStream()

        if needs_compression:
            stream = CompressionDecorator(stream)

        if needs_encryption:
            stream = EncryptionDecorator(stream, key="runtime")

        if needs_logging:
            stream = LoggingDecorator(stream, prefix="RUNTIME")

        return stream

    # Create different configurations
    print("--- Configuration 1: Encryption + Logging ---")
    stream1 = create_stream(needs_encryption=True, needs_compression=False, needs_logging=True)
    stream1.write("Config 1 data")

    print("\n--- Configuration 2: All Features ---")
    stream2 = create_stream(needs_encryption=True, needs_compression=True, needs_logging=True)
    stream2.write("Config 2 data")

    print("\n--- Configuration 3: No Decorators ---")
    stream3 = create_stream(needs_encryption=False, needs_compression=False, needs_logging=False)
    stream3.write("Config 3 data")
    print(f"Plain data: {stream3.read()}")
    print()


# ============================================================================
# Main Function
# ============================================================================


def main():
    """Run all demonstrations of the Decorator Pattern."""
    print("Decorator Pattern Example: Data Stream Processing\n")

    demonstrate_basic_decorator()
    demonstrate_stacked_decorators()
    demonstrate_logging_decorator()
    demonstrate_validation_decorator()
    demonstrate_checksum_decorator()
    demonstrate_complex_composition()
    demonstrate_different_components()
    demonstrate_decorator_independence()
    demonstrate_runtime_composition()

    print("All demonstrations completed successfully!")


if __name__ == "__main__":
    main()
