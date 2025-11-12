"""
Observer Pattern Example: Weather Monitoring System

This example demonstrates the Observer Pattern using a weather monitoring system
where multiple display elements observe weather data changes. The pattern enables
loose coupling between the weather station (subject) and various displays (observers),
allowing dynamic addition and removal of observers at runtime.

Key features:
- Observer protocol for type safety
- Weather station as observable subject
- Multiple display observers (current conditions, statistics, forecast)
- Dynamic observer management
- Weak reference support to prevent memory leaks
- Comprehensive documentation and type hints
"""

from abc import ABC, abstractmethod
from typing import List, Protocol, Any
import weakref
import random
import time
from dataclasses import dataclass


@dataclass
class WeatherData:
    """Container for weather measurement data."""
    temperature: float
    humidity: float
    pressure: float

    def __str__(self) -> str:
        return ".1f"


class Observer(Protocol):
    """
    Observer protocol defining the interface for objects that want
    to be notified of weather data changes.
    """

    def update(self, weather_data: WeatherData) -> None:
        """
        Called when weather data is updated.

        Args:
            weather_data: Current weather measurements
        """
        ...


class Subject(Protocol):
    """
    Subject protocol defining the interface for observable objects.
    """

    def register_observer(self, observer: Observer) -> None:
        """
        Register an observer to receive notifications.

        Args:
            observer: Observer to register
        """
        ...

    def remove_observer(self, observer: Observer) -> None:
        """
        Remove an observer from notifications.

        Args:
            observer: Observer to remove
        """
        ...

    def notify_observers(self) -> None:
        """
        Notify all registered observers of changes.
        """
        ...


class WeatherStation:
    """
    Weather station that collects weather data and notifies observers.

    This is the subject in the Observer pattern - it maintains the current
    weather state and broadcasts changes to all registered observers.
    """

    def __init__(self):
        self._observers: List[weakref.ReferenceType[Observer]] = []
        self._weather_data = WeatherData(0.0, 0.0, 0.0)

    def register_observer(self, observer: Observer) -> None:
        """
        Register an observer using weak reference to prevent memory leaks.

        Args:
            observer: Observer to register
        """
        self._observers.append(weakref.ref(observer))

    def remove_observer(self, observer: Observer) -> None:
        """
        Remove an observer from the notification list.

        Args:
            observer: Observer to remove
        """
        # Remove dead references and the specific observer
        self._observers = [
            ref for ref in self._observers
            if ref() is not None and ref() is not observer
        ]

    def notify_observers(self) -> None:
        """
        Notify all registered observers of the current weather data.

        Automatically removes any observers that have been garbage collected.
        """
        # Clean up dead references and notify living observers
        living_observers = []
        for ref in self._observers:
            observer = ref()
            if observer is not None:
                living_observers.append(ref)
                observer.update(self._weather_data)
            # Dead references are automatically removed

        self._observers = living_observers

    def set_measurements(self, temperature: float, humidity: float, pressure: float) -> None:
        """
        Update weather measurements and notify observers.

        Args:
            temperature: Current temperature in Celsius
            humidity: Current humidity percentage
            pressure: Current pressure in hPa
        """
        self._weather_data = WeatherData(temperature, humidity, pressure)
        self.notify_observers()

    @property
    def weather_data(self) -> WeatherData:
        """Get current weather data."""
        return self._weather_data


class CurrentConditionsDisplay:
    """
    Display showing current weather conditions.

    This observer displays the most recent temperature, humidity, and pressure readings.
    """

    def __init__(self, weather_station: WeatherStation):
        """
        Initialize display and register with weather station.

        Args:
            weather_station: Weather station to observe
        """
        self._weather_station = weather_station
        self._weather_station.register_observer(self)
        self._display_name = "Current Conditions"

    def update(self, weather_data: WeatherData) -> None:
        """
        Update display with new weather data.

        Args:
            weather_data: New weather measurements
        """
        print(f"{self._display_name}: {weather_data}")

    def unregister(self) -> None:
        """Unregister from weather station notifications."""
        self._weather_station.remove_observer(self)


class StatisticsDisplay:
    """
    Display showing weather statistics over time.

    This observer tracks minimum, maximum, and average values for temperature,
    humidity, and pressure since it was created.
    """

    def __init__(self, weather_station: WeatherStation):
        """
        Initialize statistics tracking and register with weather station.

        Args:
            weather_station: Weather station to observe
        """
        self._weather_station = weather_station
        self._weather_station.register_observer(self)
        self._display_name = "Statistics"

        # Initialize statistics
        self._temp_readings: List[float] = []
        self._humidity_readings: List[float] = []
        self._pressure_readings: List[float] = []

    def update(self, weather_data: WeatherData) -> None:
        """
        Update statistics with new weather data.

        Args:
            weather_data: New weather measurements
        """
        self._temp_readings.append(weather_data.temperature)
        self._humidity_readings.append(weather_data.humidity)
        self._pressure_readings.append(weather_data.pressure)

        if len(self._temp_readings) > 0:
            temp_min = min(self._temp_readings)
            temp_max = max(self._temp_readings)
            temp_avg = sum(self._temp_readings) / len(self._temp_readings)

            humidity_min = min(self._humidity_readings)
            humidity_max = max(self._humidity_readings)
            humidity_avg = sum(self._humidity_readings) / len(self._humidity_readings)

            pressure_min = min(self._pressure_readings)
            pressure_max = max(self._pressure_readings)
            pressure_avg = sum(self._pressure_readings) / len(self._pressure_readings)

            print(f"{self._display_name} (readings: {len(self._temp_readings)}):")
            print(f"  Temperature - Min: {temp_min:.1f}°C, Max: {temp_max:.1f}°C, Avg: {temp_avg:.1f}°C")
            print(f"  Humidity - Min: {humidity_min:.1f}%, Max: {humidity_max:.1f}%, Avg: {humidity_avg:.1f}%")
            print(f"  Pressure - Min: {pressure_min:.1f}hPa, Max: {pressure_max:.1f}hPa, Avg: {pressure_avg:.1f}hPa")

    def unregister(self) -> None:
        """Unregister from weather station notifications."""
        self._weather_station.remove_observer(self)


class ForecastDisplay:
    """
    Display showing weather forecast based on pressure changes.

    This observer provides a simple forecast based on pressure trends.
    """

    def __init__(self, weather_station: WeatherStation):
        """
        Initialize forecast tracking and register with weather station.

        Args:
            weather_station: Weather station to observe
        """
        self._weather_station = weather_station
        self._weather_station.register_observer(self)
        self._display_name = "Forecast"
        self._previous_pressure = None

    def update(self, weather_data: WeatherData) -> None:
        """
        Update forecast based on pressure change.

        Args:
            weather_data: New weather measurements
        """
        forecast = self._get_forecast(weather_data.pressure)
        print(f"{self._display_name}: {forecast}")
        self._previous_pressure = weather_data.pressure

    def _get_forecast(self, current_pressure: float) -> str:
        """
        Generate forecast based on pressure change.

        Args:
            current_pressure: Current pressure reading

        Returns:
            Forecast string
        """
        if self._previous_pressure is None:
            return "Forecast unavailable - need more data"
        elif current_pressure > self._previous_pressure:
            return "Improving weather on the way!"
        elif current_pressure < self._previous_pressure:
            return "Watch out for cooler, rainy weather"
        else:
            return "More of the same weather expected"

    def unregister(self) -> None:
        """Unregister from weather station notifications."""
        self._weather_station.remove_observer(self)


class HeatIndexDisplay:
    """
    Display showing heat index calculation.

    This observer calculates and displays the heat index (feels-like temperature)
    based on temperature and humidity.
    """

    def __init__(self, weather_station: WeatherStation):
        """
        Initialize heat index display and register with weather station.

        Args:
            weather_station: Weather station to observe
        """
        self._weather_station = weather_station
        self._weather_station.register_observer(self)
        self._display_name = "Heat Index"

    def update(self, weather_data: WeatherData) -> None:
        """
        Calculate and display heat index.

        Args:
            weather_data: New weather measurements
        """
        heat_index = self._calculate_heat_index(
            weather_data.temperature,
            weather_data.humidity
        )
        print(f"{self._display_name}: {heat_index:.1f}°C (feels like)")

    def _calculate_heat_index(self, temperature: float, humidity: float) -> float:
        """
        Calculate heat index using temperature and humidity.

        This is a simplified heat index calculation.

        Args:
            temperature: Temperature in Celsius
            humidity: Humidity percentage

        Returns:
            Heat index in Celsius
        """
        # Simplified heat index calculation
        # In reality, this would use a more complex formula
        if temperature < 27:
            return temperature  # No heat index effect below 27°C

        # Simple approximation
        heat_index = temperature + (humidity - 40) * 0.1
        return min(heat_index, temperature + 10)  # Cap the effect

    def unregister(self) -> None:
        """Unregister from weather station notifications."""
        self._weather_station.remove_observer(self)


def simulate_weather_data(weather_station: WeatherStation, readings: int = 10) -> None:
    """
    Simulate weather data readings.

    Args:
        weather_station: Weather station to update
        readings: Number of readings to simulate
    """
    print(f"\n=== Simulating {readings} Weather Readings ===\n")

    for i in range(readings):
        # Generate random weather data
        temperature = random.uniform(15, 35)  # 15-35°C
        humidity = random.uniform(30, 90)     # 30-90%
        pressure = random.uniform(990, 1030)  # 990-1030 hPa

        print(f"Reading {i + 1}: Setting measurements...")
        weather_station.set_measurements(temperature, humidity, pressure)
        print()
        time.sleep(0.5)  # Pause between readings


def demonstrate_observer_management():
    """Demonstrate adding and removing observers dynamically."""
    print("=== Observer Management Demonstration ===\n")

    weather_station = WeatherStation()

    # Start with current conditions display
    current_display = CurrentConditionsDisplay(weather_station)
    print("Added Current Conditions Display")

    weather_station.set_measurements(25.0, 60.0, 1013.0)
    print()

    # Add statistics display
    stats_display = StatisticsDisplay(weather_station)
    print("Added Statistics Display")

    weather_station.set_measurements(26.5, 55.0, 1012.0)
    print()

    # Add forecast display
    forecast_display = ForecastDisplay(weather_station)
    print("Added Forecast Display")

    weather_station.set_measurements(24.0, 70.0, 1015.0)
    print()

    # Remove current conditions display
    current_display.unregister()
    print("Removed Current Conditions Display")

    weather_station.set_measurements(27.0, 50.0, 1010.0)
    print()

    # Add heat index display
    heat_display = HeatIndexDisplay(weather_station)
    print("Added Heat Index Display")

    weather_station.set_measurements(30.0, 75.0, 1008.0)
    print()


def demonstrate_weak_references():
    """Demonstrate that weak references prevent memory leaks."""
    print("=== Weak References Demonstration ===\n")

    weather_station = WeatherStation()

    # Create observers
    displays = []
    for i in range(3):
        display = CurrentConditionsDisplay(weather_station)
        displays.append(display)
        print(f"Created display {i + 1}")

    print(f"Observers registered: {len(weather_station._observers)}")

    # Delete one display explicitly
    del displays[1]
    print("Deleted display 2 explicitly")

    # Force garbage collection (in real scenarios, this happens automatically)
    import gc
    gc.collect()

    # Notify - this should clean up dead references
    weather_station.notify_observers()
    print(f"Observers after cleanup: {len(weather_station._observers)}")

    # Delete remaining displays
    del displays
    gc.collect()

    weather_station.notify_observers()
    print(f"Observers after deleting all: {len(weather_station._observers)}")
    print()


def main():
    """Run all demonstrations."""
    print("Observer Pattern Example: Weather Monitoring System\n")

    demonstrate_observer_management()
    demonstrate_weak_references()

    # Create weather station with all displays
    weather_station = WeatherStation()
    displays = [
        CurrentConditionsDisplay(weather_station),
        StatisticsDisplay(weather_station),
        ForecastDisplay(weather_station),
        HeatIndexDisplay(weather_station)
    ]

    # Simulate weather data
    simulate_weather_data(weather_station, 5)

    print("=== Demonstration Complete ===")
    print("All displays have been automatically cleaned up via weak references!")


if __name__ == "__main__":
    main()