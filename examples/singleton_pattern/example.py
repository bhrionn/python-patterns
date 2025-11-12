"""
Singleton Pattern Example: Configuration Manager

This example demonstrates the Singleton Pattern using a configuration manager
that ensures only one instance exists across the application. The pattern is
implemented using a metaclass for thread-safety and proper Python practices.

Key features:
- Thread-safe singleton using metaclass
- Lazy initialization
- Comprehensive documentation
- Testing-friendly with reset capability
- Type hints and error handling
"""

import threading
import time
from typing import Dict, Any, Optional


class SingletonMeta(type):
    """
    Metaclass for creating thread-safe singleton classes.

    This metaclass ensures that only one instance of any class using it
    can exist, and provides thread-safe instantiation using double-checked locking.
    """

    _instances: Dict[type, Any] = {}
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        """
        Create or return the singleton instance.

        Uses double-checked locking for thread safety.
        """
        # First check (no lock)
        if cls not in cls._instances:
            # Acquire lock for thread safety
            with cls._lock:
                # Second check (with lock)
                if cls not in cls._instances:
                    cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class ConfigurationManager(metaclass=SingletonMeta):
    """
    Configuration manager implemented as a singleton.

    This class ensures that configuration is loaded once and shared across
    the entire application, preventing multiple loads and inconsistent state.
    """

    def __init__(self):
        """
        Initialize the configuration manager.

        The __init__ method is called only once due to singleton behavior.
        """
        self._config: Dict[str, Any] = {}
        self._loaded = False
        self._load_config()

    def _load_config(self) -> None:
        """
        Simulate loading configuration from a file or database.

        In a real application, this might load from environment variables,
        configuration files, or remote services.
        """
        # Simulate loading time
        time.sleep(0.1)

        # Mock configuration data
        self._config = {
            "database": {
                "host": "localhost",
                "port": 5432,
                "name": "app_db",
                "max_connections": 10
            },
            "logging": {
                "level": "INFO",
                "file": "app.log",
                "max_size": "10MB"
            },
            "cache": {
                "ttl": 3600,
                "max_items": 1000
            },
            "features": {
                "new_ui": True,
                "beta_features": False
            }
        }
        self._loaded = True

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value by key.

        Supports nested keys using dot notation (e.g., "database.host").

        Args:
            key: Configuration key to retrieve
            default: Default value if key not found

        Returns:
            Configuration value or default
        """
        keys = key.split('.')
        value = self._config

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default

        return value

    def set(self, key: str, value: Any) -> None:
        """
        Set a configuration value.

        Args:
            key: Configuration key to set
            value: Value to set
        """
        keys = key.split('.')
        config = self._config

        # Navigate to the parent of the final key
        for k in keys[:-1]:
            if k not in config or not isinstance(config[k], dict):
                config[k] = {}
            config = config[k]

        # Set the final value
        config[keys[-1]] = value

    def is_loaded(self) -> bool:
        """
        Check if configuration has been loaded.

        Returns:
            True if configuration is loaded, False otherwise
        """
        return self._loaded

    def reload(self) -> None:
        """
        Reload configuration from source.

        This method allows refreshing configuration at runtime.
        """
        self._config = {}
        self._loaded = False
        self._load_config()

    @classmethod
    def reset_instance(cls) -> None:
        """
        Reset the singleton instance (for testing purposes).

        This method allows tests to reset the singleton state between test runs.
        In production code, this method should be removed or protected.
        """
        with SingletonMeta._lock:
            if cls in SingletonMeta._instances:
                del SingletonMeta._instances[cls]


def demonstrate_singleton():
    """Demonstrate that only one instance exists."""
    print("=== Singleton Demonstration ===\n")

    # Create first instance
    config1 = ConfigurationManager()
    print(f"First instance ID: {id(config1)}")

    # Create second instance
    config2 = ConfigurationManager()
    print(f"Second instance ID: {id(config2)}")

    print(f"Same instance? {config1 is config2}")

    # Modify config through first instance
    config1.set("app.version", "1.2.3")

    # Check if second instance sees the change
    version = config2.get("app.version")
    print(f"Version from second instance: {version}")
    print()


def demonstrate_thread_safety():
    """Demonstrate thread-safe singleton creation."""
    print("=== Thread Safety Demonstration ===\n")

    instances = []
    instance_ids = set()

    def create_instance():
        """Create a singleton instance and record its ID."""
        instance = ConfigurationManager()
        instances.append(instance)
        instance_ids.add(id(instance))

    # Create multiple threads that try to create instances
    threads = []
    for i in range(10):
        thread = threading.Thread(target=create_instance)
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    print(f"Created {len(instances)} instances")
    print(f"Unique instance IDs: {len(instance_ids)}")
    print(f"All instances are the same? {len(instance_ids) == 1}")
    print()


def demonstrate_usage():
    """Demonstrate typical usage of the configuration manager."""
    print("=== Usage Demonstration ===\n")

    config = ConfigurationManager()

    # Get database configuration
    db_host = config.get("database.host")
    db_port = config.get("database.port")
    print(f"Database: {db_host}:{db_port}")

    # Get logging configuration
    log_level = config.get("logging.level")
    log_file = config.get("logging.file")
    print(f"Logging: {log_level} to {log_file}")

    # Check features
    new_ui = config.get("features.new_ui")
    beta_features = config.get("features.beta_features")
    print(f"New UI enabled: {new_ui}")
    print(f"Beta features enabled: {beta_features}")

    # Set a custom value
    config.set("custom.api_key", "secret123")
    api_key = config.get("custom.api_key")
    print(f"Custom API key: {api_key}")

    # Try to get non-existent key
    missing = config.get("nonexistent.key", "default_value")
    print(f"Missing key with default: {missing}")
    print()


def demonstrate_reset():
    """Demonstrate instance reset for testing."""
    print("=== Reset Demonstration ===\n")

    config1 = ConfigurationManager()
    config1.set("test.value", "original")

    print(f"Original value: {config1.get('test.value')}")

    # Reset the instance
    ConfigurationManager.reset_instance()

    # Create new instance (should be fresh)
    config2 = ConfigurationManager()
    test_value = config2.get("test.value", "not_set")
    print(f"After reset: {test_value}")

    # Verify different instances
    print(f"Different instances? {config1 is not config2}")
    print()


def main():
    """Run all demonstrations."""
    print("Singleton Pattern Example: Configuration Manager\n")

    demonstrate_singleton()
    demonstrate_thread_safety()
    demonstrate_usage()
    demonstrate_reset()

    print("All demonstrations completed successfully!")


if __name__ == "__main__":
    main()