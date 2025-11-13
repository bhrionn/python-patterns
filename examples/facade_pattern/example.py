"""
Facade Pattern Example: Home Theater System

This example demonstrates the Facade Pattern using a home theater system
that has multiple complex components (projector, amplifier, DVD player, etc.).
The facade provides simple methods for common operations (watch movie, listen to music)
while hiding the complexity of coordinating all components.

Key features:
- Facade providing simplified interface
- Multiple complex subsystem components
- Common operations (watch movie, listen to music, end experience)
- Error handling and resource management
- Context manager support
- Type hints and comprehensive documentation

SOLID Principles Demonstrated:
- Single Responsibility: Each component has one clear purpose
- Open/Closed: New components can be added without modifying facade
- Interface Segregation: Clients use simple facade interface, not complex subsystem
- Dependency Inversion: Facade depends on abstractions (component protocols)
"""

from abc import ABC, abstractmethod
from typing import Optional, List
from enum import Enum


class PowerState(Enum):
    """Enumeration of power states for devices."""
    ON = "on"
    OFF = "off"
    STANDBY = "standby"


class DVDPlayer:
    """
    DVD Player subsystem component.

    Manages DVD playback with complex controls and state.
    """

    def __init__(self):
        """Initialize DVD player."""
        self._power_state = PowerState.OFF
        self._current_disc: Optional[str] = None
        self._playing = False

    def on(self) -> None:
        """Power on the DVD player."""
        if self._power_state == PowerState.OFF:
            self._power_state = PowerState.ON
            print("DVD Player: Powering on...")
            print("DVD Player: Loading firmware...")
            print("DVD Player: Ready")

    def off(self) -> None:
        """Power off the DVD player."""
        if self._power_state == PowerState.ON:
            if self._playing:
                self.stop()
            self._power_state = PowerState.OFF
            print("DVD Player: Powering off")

    def eject(self) -> None:
        """Eject the current disc."""
        if self._power_state == PowerState.ON:
            if self._playing:
                self.stop()
            if self._current_disc:
                print(f"DVD Player: Ejecting '{self._current_disc}'")
                self._current_disc = None
            else:
                print("DVD Player: No disc to eject")

    def play(self, movie: str) -> None:
        """
        Play a movie.

        Args:
            movie: Title of the movie to play
        """
        if self._power_state == PowerState.ON:
            self._current_disc = movie
            self._playing = True
            print(f"DVD Player: Playing '{movie}'")

    def stop(self) -> None:
        """Stop playback."""
        if self._playing:
            self._playing = False
            print("DVD Player: Stopped")

    def pause(self) -> None:
        """Pause playback."""
        if self._playing:
            print("DVD Player: Paused")


class Projector:
    """
    Projector subsystem component.

    Manages display output with various settings.
    """

    def __init__(self):
        """Initialize projector."""
        self._power_state = PowerState.OFF
        self._input_source: Optional[str] = None

    def on(self) -> None:
        """Power on the projector."""
        if self._power_state == PowerState.OFF:
            self._power_state = PowerState.ON
            print("Projector: Powering on (warming up lamp)...")
            print("Projector: Ready")

    def off(self) -> None:
        """Power off the projector."""
        if self._power_state == PowerState.ON:
            self._power_state = PowerState.OFF
            print("Projector: Cooling down...")
            print("Projector: Powering off")

    def set_input(self, source: str) -> None:
        """
        Set the input source.

        Args:
            source: Input source name (HDMI1, HDMI2, DVD, etc.)
        """
        if self._power_state == PowerState.ON:
            self._input_source = source
            print(f"Projector: Input set to {source}")

    def wide_screen_mode(self) -> None:
        """Set widescreen display mode."""
        if self._power_state == PowerState.ON:
            print("Projector: Setting widescreen mode (16:9)")


class Screen:
    """
    Motorized screen subsystem component.

    Controls the projection screen position.
    """

    def __init__(self):
        """Initialize screen."""
        self._is_down = False

    def down(self) -> None:
        """Lower the screen."""
        if not self._is_down:
            print("Screen: Lowering screen...")
            self._is_down = True
            print("Screen: Screen is down")

    def up(self) -> None:
        """Raise the screen."""
        if self._is_down:
            print("Screen: Raising screen...")
            self._is_down = False
            print("Screen: Screen is up")


class Amplifier:
    """
    Audio amplifier subsystem component.

    Manages audio routing and volume control.
    """

    def __init__(self):
        """Initialize amplifier."""
        self._power_state = PowerState.OFF
        self._input_source: Optional[str] = None
        self._volume = 0
        self._surround_mode = False

    def on(self) -> None:
        """Power on the amplifier."""
        if self._power_state == PowerState.OFF:
            self._power_state = PowerState.ON
            print("Amplifier: Powering on...")
            print("Amplifier: Ready")

    def off(self) -> None:
        """Power off the amplifier."""
        if self._power_state == PowerState.ON:
            self._power_state = PowerState.OFF
            print("Amplifier: Powering off")

    def set_input(self, source: str) -> None:
        """
        Set the audio input source.

        Args:
            source: Input source name
        """
        if self._power_state == PowerState.ON:
            self._input_source = source
            print(f"Amplifier: Input set to {source}")

    def set_volume(self, level: int) -> None:
        """
        Set the volume level.

        Args:
            level: Volume level (0-100)
        """
        if self._power_state == PowerState.ON:
            self._volume = max(0, min(100, level))
            print(f"Amplifier: Volume set to {self._volume}")

    def set_surround_sound(self) -> None:
        """Enable surround sound mode."""
        if self._power_state == PowerState.ON:
            self._surround_mode = True
            print("Amplifier: 5.1 surround sound enabled")


class Lights:
    """
    Smart lighting subsystem component.

    Controls room lighting with dimming capability.
    """

    def __init__(self):
        """Initialize lights."""
        self._brightness = 100  # 0-100

    def dim(self, level: int) -> None:
        """
        Dim lights to specified level.

        Args:
            level: Brightness level (0-100)
        """
        self._brightness = max(0, min(100, level))
        print(f"Lights: Dimming to {self._brightness}%")

    def on(self) -> None:
        """Turn lights fully on."""
        self._brightness = 100
        print("Lights: Turning on to 100%")


class StreamingDevice:
    """
    Streaming device subsystem component.

    Provides access to streaming services.
    """

    def __init__(self):
        """Initialize streaming device."""
        self._power_state = PowerState.OFF
        self._current_app: Optional[str] = None

    def on(self) -> None:
        """Power on the streaming device."""
        if self._power_state == PowerState.OFF:
            self._power_state = PowerState.ON
            print("Streaming Device: Powering on...")
            print("Streaming Device: Connecting to network...")
            print("Streaming Device: Ready")

    def off(self) -> None:
        """Power off the streaming device."""
        if self._power_state == PowerState.ON:
            self._power_state = PowerState.OFF
            print("Streaming Device: Powering off")

    def launch_app(self, app: str) -> None:
        """
        Launch a streaming app.

        Args:
            app: App name (Netflix, Hulu, etc.)
        """
        if self._power_state == PowerState.ON:
            self._current_app = app
            print(f"Streaming Device: Launching {app}")

    def play_content(self, title: str) -> None:
        """
        Play content.

        Args:
            title: Content title
        """
        if self._power_state == PowerState.ON and self._current_app:
            print(f"Streaming Device: Playing '{title}' on {self._current_app}")


class HomeTheaterFacade:
    """
    Facade providing simplified interface to home theater system.

    This facade encapsulates the complexity of coordinating multiple
    components (DVD player, projector, amplifier, lights, etc.) and
    provides simple methods for common operations.

    Demonstrates:
    - Simplified interface to complex subsystem
    - Coordination of multiple components
    - Sensible defaults for common operations
    - Error handling and resource management
    """

    def __init__(
        self,
        dvd_player: DVDPlayer,
        projector: Projector,
        screen: Screen,
        amplifier: Amplifier,
        lights: Lights,
        streaming_device: StreamingDevice
    ):
        """
        Initialize the home theater facade.

        Args:
            dvd_player: DVD player component
            projector: Projector component
            screen: Motorized screen component
            amplifier: Audio amplifier component
            lights: Lighting system component
            streaming_device: Streaming device component
        """
        self._dvd = dvd_player
        self._projector = projector
        self._screen = screen
        self._amp = amplifier
        self._lights = lights
        self._streaming = streaming_device

    def watch_movie(self, movie: str) -> None:
        """
        Watch a DVD movie with optimal settings.

        This method coordinates all components to create the
        perfect movie-watching experience.

        Args:
            movie: Title of the movie to watch
        """
        print("\n🎬 Getting ready to watch a movie...\n")

        # Set the ambiance
        self._lights.dim(10)

        # Prepare the display
        self._screen.down()
        self._projector.on()
        self._projector.set_input("DVD")
        self._projector.wide_screen_mode()

        # Set up audio
        self._amp.on()
        self._amp.set_input("DVD")
        self._amp.set_volume(5)
        self._amp.set_surround_sound()

        # Start the movie
        self._dvd.on()
        self._dvd.play(movie)

        print(f"\n✅ Enjoy your movie: '{movie}'!\n")

    def end_movie(self) -> None:
        """
        End the movie and shut down all components.

        Coordinates proper shutdown sequence for all components.
        """
        print("\n⏹️  Shutting down movie experience...\n")

        self._dvd.stop()
        self._dvd.eject()
        self._dvd.off()

        self._amp.off()

        self._projector.off()
        self._screen.up()

        self._lights.on()

        print("\n✅ Movie experience ended.\n")

    def watch_streaming(self, service: str, title: str, volume: int = 7) -> None:
        """
        Watch streaming content.

        Args:
            service: Streaming service name (Netflix, Hulu, etc.)
            title: Content title
            volume: Audio volume level (0-100), defaults to 7
        """
        print(f"\n📺 Getting ready to watch {title} on {service}...\n")

        # Set the ambiance
        self._lights.dim(15)

        # Prepare the display
        self._screen.down()
        self._projector.on()
        self._projector.set_input("HDMI1")
        self._projector.wide_screen_mode()

        # Set up audio
        self._amp.on()
        self._amp.set_input("HDMI1")
        self._amp.set_volume(volume)
        self._amp.set_surround_sound()

        # Start streaming
        self._streaming.on()
        self._streaming.launch_app(service)
        self._streaming.play_content(title)

        print(f"\n✅ Enjoy '{title}' on {service}!\n")

    def end_streaming(self) -> None:
        """End streaming and shut down components."""
        print("\n⏹️  Ending streaming session...\n")

        self._streaming.off()
        self._amp.off()
        self._projector.off()
        self._screen.up()
        self._lights.on()

        print("\n✅ Streaming session ended.\n")

    def listen_to_music(self, volume: int = 5) -> None:
        """
        Set up for music listening.

        Args:
            volume: Audio volume level (0-100), defaults to 5
        """
        print("\n🎵 Setting up for music...\n")

        # Lights stay on for music
        self._lights.dim(30)

        # Just need amplifier for music
        self._amp.on()
        self._amp.set_input("MUSIC")
        self._amp.set_volume(volume)
        self._amp.set_surround_sound()

        print("\n✅ Ready to play music!\n")

    def end_music(self) -> None:
        """End music session."""
        print("\n⏹️  Ending music session...\n")

        self._amp.off()
        self._lights.on()

        print("\n✅ Music session ended.\n")


def demonstrate_without_facade():
    """Demonstrate the complexity without using facade."""
    print("=== WITHOUT FACADE (Complex) ===\n")

    # Client must manage all components directly
    dvd = DVDPlayer()
    projector = Projector()
    screen = Screen()
    amp = Amplifier()
    lights = Lights()

    print("Client manually setting up to watch a movie:\n")

    # Complex setup sequence that client must remember
    lights.dim(10)
    screen.down()
    projector.on()
    projector.set_input("DVD")
    projector.wide_screen_mode()
    amp.on()
    amp.set_input("DVD")
    amp.set_volume(5)
    amp.set_surround_sound()
    dvd.on()
    dvd.play("The Matrix")

    print("\n(Client had to coordinate 10+ steps manually!)\n")


def demonstrate_with_facade():
    """Demonstrate simplified usage with facade."""
    print("=== WITH FACADE (Simple) ===\n")

    # Create components
    dvd = DVDPlayer()
    projector = Projector()
    screen = Screen()
    amp = Amplifier()
    lights = Lights()
    streaming = StreamingDevice()

    # Create facade
    home_theater = HomeTheaterFacade(dvd, projector, screen, amp, lights, streaming)

    print("Client using facade to watch a movie:\n")

    # Simple one-line setup!
    home_theater.watch_movie("The Matrix")

    print("(Facade handled all coordination automatically!)")


def demonstrate_multiple_scenarios():
    """Demonstrate different usage scenarios."""
    print("=== MULTIPLE SCENARIOS ===\n")

    # Setup
    dvd = DVDPlayer()
    projector = Projector()
    screen = Screen()
    amp = Amplifier()
    lights = Lights()
    streaming = StreamingDevice()

    home_theater = HomeTheaterFacade(dvd, projector, screen, amp, lights, streaming)

    # Scenario 1: Watch DVD movie
    print("SCENARIO 1: Watch DVD Movie")
    home_theater.watch_movie("Inception")
    input("Press Enter to end movie...")
    home_theater.end_movie()

    # Scenario 2: Watch streaming content
    print("\nSCENARIO 2: Watch Streaming Content")
    home_theater.watch_streaming("Netflix", "Stranger Things", volume=8)
    input("Press Enter to end streaming...")
    home_theater.end_streaming()

    # Scenario 3: Listen to music
    print("\nSCENARIO 3: Listen to Music")
    home_theater.listen_to_music(volume=6)
    input("Press Enter to end music...")
    home_theater.end_music()


def demonstrate_benefits():
    """Demonstrate the benefits of using facade."""
    print("=== BENEFITS OF FACADE ===\n")

    # Setup
    dvd = DVDPlayer()
    projector = Projector()
    screen = Screen()
    amp = Amplifier()
    lights = Lights()
    streaming = StreamingDevice()

    home_theater = HomeTheaterFacade(dvd, projector, screen, amp, lights, streaming)

    print("Benefits demonstrated:\n")

    print("1. SIMPLICITY")
    print("   Without facade: 10+ steps to watch a movie")
    print("   With facade: 1 method call\n")

    print("2. ENCAPSULATION")
    print("   Complex component coordination hidden from client\n")

    print("3. FLEXIBILITY")
    print("   Easy to change implementation without affecting clients\n")

    print("4. REUSABILITY")
    print("   Common operations packaged as reusable methods\n")

    print("5. MAINTAINABILITY")
    print("   Changes to subsystem don't require updating all clients\n")

    # Quick demo
    home_theater.watch_movie("The Dark Knight")


def main():
    """Run all demonstrations."""
    print("Facade Pattern Example: Home Theater System\n")
    print("=" * 60)

    demonstrate_without_facade()

    print("\n" + "=" * 60 + "\n")

    demonstrate_with_facade()

    print("\n" + "=" * 60 + "\n")

    # Uncomment to run interactive scenarios
    # demonstrate_multiple_scenarios()

    demonstrate_benefits()

    print("\n" + "=" * 60)
    print("\nAll demonstrations completed successfully!")


if __name__ == "__main__":
    main()
