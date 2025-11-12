"""
Factory Pattern Example: Transportation Logistics

This example demonstrates the Factory Pattern using a logistics application
that creates different types of transportation vehicles. The pattern allows
for centralized and extensible object creation, following SOLID principles.

Key features:
- Abstract base class for Transport
- Concrete implementations for Truck, Ship, and Plane
- Factory function for creating transports
- Type hints and comprehensive documentation
- Adherence to Open/Closed Principle
"""

from abc import ABC, abstractmethod
from typing import Protocol


class Transport(Protocol):
    """
    Protocol defining the interface for transportation vehicles.

    This protocol ensures that all transport types have the necessary methods
    for delivery operations.
    """

    @abstractmethod
    def deliver(self, cargo: str, destination: str) -> str:
        """
        Deliver cargo to the specified destination.

        Args:
            cargo: Description of the cargo to deliver
            destination: Delivery destination

        Returns:
            Delivery confirmation message
        """
        pass

    @property
    @abstractmethod
    def capacity(self) -> int:
        """
        Get the transport's cargo capacity.

        Returns:
            Maximum cargo capacity in tons
        """
        pass


class Truck:
    """
    Concrete implementation of Transport for road transportation.

    Represents a truck with specific capacity and delivery behavior.
    """

    @property
    def capacity(self) -> int:
        """Truck capacity is 10 tons."""
        return 10

    def deliver(self, cargo: str, destination: str) -> str:
        """
        Deliver cargo by road.

        Args:
            cargo: Description of the cargo
            destination: Delivery destination

        Returns:
            Delivery confirmation message
        """
        return f"Truck delivered {cargo} to {destination} via road transport."


class Ship:
    """
    Concrete implementation of Transport for sea transportation.

    Represents a ship with higher capacity and sea-based delivery.
    """

    @property
    def capacity(self) -> int:
        """Ship capacity is 1000 tons."""
        return 1000

    def deliver(self, cargo: str, destination: str) -> str:
        """
        Deliver cargo by sea.

        Args:
            cargo: Description of the cargo
            destination: Delivery destination

        Returns:
            Delivery confirmation message
        """
        return f"Ship delivered {cargo} to {destination} via sea transport."


class Plane:
    """
    Concrete implementation of Transport for air transportation.

    Represents a plane with medium capacity and fast air delivery.
    """

    @property
    def capacity(self) -> int:
        """Plane capacity is 50 tons."""
        return 50

    def deliver(self, cargo: str, destination: str) -> str:
        """
        Deliver cargo by air.

        Args:
            cargo: Description of the cargo
            destination: Delivery destination

        Returns:
            Delivery confirmation message
        """
        return f"Plane delivered {cargo} to {destination} via air transport."


class TransportType:
    """Enumeration of available transport types."""
    TRUCK = "truck"
    SHIP = "ship"
    PLANE = "plane"


def create_transport(transport_type: str) -> Transport:
    """
    Factory function for creating transport objects.

    This function encapsulates the object creation logic, allowing for easy
    extension and modification without changing client code.

    Args:
        transport_type: Type of transport to create ('truck', 'ship', or 'plane')

    Returns:
        Transport instance of the specified type

    Raises:
        ValueError: If transport_type is not recognized
    """
    if transport_type == TransportType.TRUCK:
        return Truck()
    elif transport_type == TransportType.SHIP:
        return Ship()
    elif transport_type == TransportType.PLANE:
        return Plane()
    else:
        raise ValueError(f"Unknown transport type: {transport_type}")


class LogisticsApp:
    """
    Logistics application demonstrating factory pattern usage.

    This class uses the factory to create transports without knowing
    the concrete implementations, adhering to Dependency Inversion Principle.
    """

    def __init__(self, transport_factory: callable = create_transport):
        """
        Initialize logistics app with a transport factory.

        Args:
            transport_factory: Factory function for creating transports
        """
        self._transport_factory = transport_factory

    def plan_delivery(self, transport_type: str, cargo: str, destination: str) -> str:
        """
        Plan and execute a delivery using the appropriate transport.

        Args:
            transport_type: Type of transport to use
            cargo: Description of cargo to deliver
            destination: Delivery destination

        Returns:
            Delivery result message

        Raises:
            ValueError: If transport creation fails
        """
        transport = self._transport_factory(transport_type)
        return transport.deliver(cargo, destination)

    def get_transport_info(self, transport_type: str) -> dict:
        """
        Get information about a transport type.

        Args:
            transport_type: Type of transport to query

        Returns:
            Dictionary with transport information
        """
        transport = self._transport_factory(transport_type)
        return {
            "type": transport_type,
            "capacity": transport.capacity,
            "class_name": transport.__class__.__name__
        }


def main():
    """Demonstrate the Factory Pattern in action."""
    print("=== Factory Pattern Example: Transportation Logistics ===\n")

    # Create logistics application
    app = LogisticsApp()

    # Demonstrate different transport types
    transports = [TransportType.TRUCK, TransportType.SHIP, TransportType.PLANE]

    for transport_type in transports:
        print(f"--- {transport_type.capitalize()} Transport ---")

        # Get transport info
        info = app.get_transport_info(transport_type)
        print(f"Type: {info['type']}")
        print(f"Capacity: {info['capacity']} tons")
        print(f"Implementation: {info['class_name']}")

        # Plan delivery
        result = app.plan_delivery(
            transport_type,
            "electronics",
            "New York"
        )
        print(f"Delivery: {result}\n")

    # Demonstrate error handling
    print("--- Error Handling ---")
    try:
        app.plan_delivery("bicycle", "books", "Boston")
    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()