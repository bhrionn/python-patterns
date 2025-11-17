"""
State Pattern Example: Media Player

This example demonstrates the State Pattern using a media player that can be
in different states (Stopped, Playing, Paused). Each state has different
behavior for the same operations (play, pause, stop).

Key features:
- State interface using ABC
- Multiple concrete states (Stopped, Playing, Paused)
- Context class (MediaPlayer) delegating to states
- Explicit state transitions
- State-specific behavior
- Entry and exit actions
- Type hints and comprehensive documentation

SOLID Principles Demonstrated:
- Single Responsibility: Each state handles one state's behavior
- Open/Closed: New states can be added without modifying existing code
- Liskov Substitution: All states are substitutable through common interface
- Interface Segregation: Clean state interface
- Dependency Inversion: Context depends on state abstraction
"""

from abc import ABC, abstractmethod
from typing import Optional, List
from dataclasses import dataclass
from enum import Enum, auto


class PlayerEvent(Enum):
    """Events that can occur in the media player."""
    PLAY = auto()
    PAUSE = auto()
    STOP = auto()
    NEXT = auto()
    PREVIOUS = auto()


@dataclass
class Track:
    """
    Represents a music track.

    Attributes:
        title: Track title
        artist: Artist name
        duration: Duration in seconds
    """
    title: str
    artist: str
    duration: int

    def __str__(self) -> str:
        minutes = self.duration // 60
        seconds = self.duration % 60
        return f"{self.title} by {self.artist} ({minutes}:{seconds:02d})"


class PlayerState(ABC):
    """
    Abstract base class for player states.

    Each state implements different behavior for player operations.
    States can trigger transitions to other states.
    """

    def __init__(self):
        """Initialize state."""
        self.name = self.__class__.__name__

    def on_enter(self, player: 'MediaPlayer') -> None:
        """
        Called when entering this state.

        Args:
            player: The media player context
        """
        print(f"[State] Entering {self.name} state")

    def on_exit(self, player: 'MediaPlayer') -> None:
        """
        Called when exiting this state.

        Args:
            player: The media player context
        """
        print(f"[State] Exiting {self.name} state")

    @abstractmethod
    def play(self, player: 'MediaPlayer') -> None:
        """
        Handle play button press.

        Args:
            player: The media player context
        """
        pass

    @abstractmethod
    def pause(self, player: 'MediaPlayer') -> None:
        """
        Handle pause button press.

        Args:
            player: The media player context
        """
        pass

    @abstractmethod
    def stop(self, player: 'MediaPlayer') -> None:
        """
        Handle stop button press.

        Args:
            player: The media player context
        """
        pass

    def next_track(self, player: 'MediaPlayer') -> None:
        """
        Handle next track button press.

        Default implementation works for all states.

        Args:
            player: The media player context
        """
        if player.has_next_track():
            player.move_to_next_track()
            print(f"[Player] ⏭️  Next track: {player.current_track}")
        else:
            print("[Player] Already at last track")

    def previous_track(self, player: 'MediaPlayer') -> None:
        """
        Handle previous track button press.

        Default implementation works for all states.

        Args:
            player: The media player context
        """
        if player.has_previous_track():
            player.move_to_previous_track()
            print(f"[Player] ⏮️  Previous track: {player.current_track}")
        else:
            print("[Player] Already at first track")


class StoppedState(PlayerState):
    """
    State when player is stopped.

    In this state:
    - Play starts playback
    - Pause does nothing
    - Stop does nothing
    """

    def play(self, player: 'MediaPlayer') -> None:
        """Start playback from current track."""
        print(f"[Player] ▶️  Starting playback: {player.current_track}")
        player.set_state(PlayingState())

    def pause(self, player: 'MediaPlayer') -> None:
        """Cannot pause when stopped."""
        print("[Player] ⚠️  Cannot pause - player is stopped")

    def stop(self, player: 'MediaPlayer') -> None:
        """Already stopped."""
        print("[Player] ⚠️  Player is already stopped")


class PlayingState(PlayerState):
    """
    State when player is playing.

    In this state:
    - Play does nothing (already playing)
    - Pause pauses playback
    - Stop stops playback
    """

    def on_enter(self, player: 'MediaPlayer') -> None:
        """Start audio playback when entering playing state."""
        super().on_enter(player)
        print(f"[Audio] 🔊 Playing audio: {player.current_track}")

    def on_exit(self, player: 'MediaPlayer') -> None:
        """Stop audio when exiting playing state."""
        print("[Audio] 🔇 Stopping audio")
        super().on_exit(player)

    def play(self, player: 'MediaPlayer') -> None:
        """Already playing."""
        print("[Player] ⚠️  Already playing")

    def pause(self, player: 'MediaPlayer') -> None:
        """Pause playback."""
        print(f"[Player] ⏸️  Pausing: {player.current_track}")
        player.set_state(PausedState())

    def stop(self, player: 'MediaPlayer') -> None:
        """Stop playback."""
        print(f"[Player] ⏹️  Stopping: {player.current_track}")
        player.set_state(StoppedState())

    def next_track(self, player: 'MediaPlayer') -> None:
        """
        Skip to next track while playing.

        Overrides default to auto-play next track.
        """
        if player.has_next_track():
            # Exit current state (stop audio)
            self.on_exit(player)
            player.move_to_next_track()
            print(f"[Player] ⏭️  Next track: {player.current_track}")
            # Re-enter state (start new audio)
            self.on_enter(player)
        else:
            print("[Player] Already at last track")

    def previous_track(self, player: 'MediaPlayer') -> None:
        """
        Skip to previous track while playing.

        Overrides default to auto-play previous track.
        """
        if player.has_previous_track():
            # Exit current state (stop audio)
            self.on_exit(player)
            player.move_to_previous_track()
            print(f"[Player] ⏮️  Previous track: {player.current_track}")
            # Re-enter state (start new audio)
            self.on_enter(player)
        else:
            print("[Player] Already at first track")


class PausedState(PlayerState):
    """
    State when player is paused.

    In this state:
    - Play resumes playback
    - Pause does nothing (already paused)
    - Stop stops playback
    """

    def play(self, player: 'MediaPlayer') -> None:
        """Resume playback."""
        print(f"[Player] ▶️  Resuming: {player.current_track}")
        player.set_state(PlayingState())

    def pause(self, player: 'MediaPlayer') -> None:
        """Already paused."""
        print("[Player] ⚠️  Already paused")

    def stop(self, player: 'MediaPlayer') -> None:
        """Stop playback."""
        print(f"[Player] ⏹️  Stopping: {player.current_track}")
        player.set_state(StoppedState())


class MediaPlayer:
    """
    Media player context class.

    This class maintains the current state and delegates all
    operations to the current state object. It also manages
    the playlist and track navigation.

    Demonstrates:
    - Context maintaining current state
    - Delegating operations to state
    - State transition management
    - Separation of concerns (player manages tracks, states handle behavior)
    """

    def __init__(self, playlist: List[Track]):
        """
        Initialize media player.

        Args:
            playlist: List of tracks to play
        """
        if not playlist:
            raise ValueError("Playlist cannot be empty")

        self._playlist = playlist
        self._current_track_index = 0
        self._state = StoppedState()
        self._state_history: List[str] = []

        print(f"[Player] Initialized with {len(playlist)} tracks")
        print(f"[Player] Current track: {self.current_track}")

    @property
    def current_track(self) -> Track:
        """Get the current track."""
        return self._playlist[self._current_track_index]

    @property
    def state_name(self) -> str:
        """Get the name of the current state."""
        return self._state.name

    def set_state(self, state: PlayerState) -> None:
        """
        Set a new state.

        This method handles the state transition, calling
        on_exit on the old state and on_enter on the new state.

        Args:
            state: New state to transition to
        """
        self._state.on_exit(self)
        self._state_history.append(self._state.name)
        self._state = state
        self._state.on_enter(self)

    def has_next_track(self) -> bool:
        """Check if there's a next track."""
        return self._current_track_index < len(self._playlist) - 1

    def has_previous_track(self) -> bool:
        """Check if there's a previous track."""
        return self._current_track_index > 0

    def move_to_next_track(self) -> None:
        """Move to next track."""
        if self.has_next_track():
            self._current_track_index += 1

    def move_to_previous_track(self) -> None:
        """Move to previous track."""
        if self.has_previous_track():
            self._current_track_index -= 1

    # Public API - delegates to current state

    def play(self) -> None:
        """Play or resume playback."""
        print(f"\n▶️  PLAY button pressed (Current state: {self.state_name})")
        self._state.play(self)

    def pause(self) -> None:
        """Pause playback."""
        print(f"\n⏸️  PAUSE button pressed (Current state: {self.state_name})")
        self._state.pause(self)

    def stop(self) -> None:
        """Stop playback."""
        print(f"\n⏹️  STOP button pressed (Current state: {self.state_name})")
        self._state.stop(self)

    def next_track(self) -> None:
        """Skip to next track."""
        print(f"\n⏭️  NEXT button pressed (Current state: {self.state_name})")
        self._state.next_track(self)

    def previous_track(self) -> None:
        """Skip to previous track."""
        print(f"\n⏮️  PREVIOUS button pressed (Current state: {self.state_name})")
        self._state.previous_track(self)

    def get_state_history(self) -> List[str]:
        """
        Get history of state transitions.

        Returns:
            List of state names in chronological order
        """
        return self._state_history.copy()

    def display_status(self) -> None:
        """Display current player status."""
        print(f"\n📊 Player Status:")
        print(f"  State: {self.state_name}")
        print(f"  Track: {self.current_track}")
        print(f"  Track {self._current_track_index + 1} of {len(self._playlist)}")


# ============================================================================
# DEMONSTRATIONS
# ============================================================================


def demonstrate_basic_state_transitions():
    """Demonstrate basic state transitions."""
    print("=== BASIC STATE TRANSITIONS ===\n")

    # Create playlist
    playlist = [
        Track("Bohemian Rhapsody", "Queen", 354),
        Track("Stairway to Heaven", "Led Zeppelin", 482),
        Track("Hotel California", "Eagles", 390)
    ]

    player = MediaPlayer(playlist)
    player.display_status()

    # Transition: Stopped -> Playing
    player.play()

    # Try to play again (already playing)
    player.play()

    # Transition: Playing -> Paused
    player.pause()

    # Transition: Paused -> Playing
    player.play()

    # Transition: Playing -> Stopped
    player.stop()

    # Try to pause when stopped
    player.pause()

    player.display_status()


def demonstrate_track_navigation():
    """Demonstrate track navigation in different states."""
    print("\n=== TRACK NAVIGATION ===\n")

    playlist = [
        Track("Song 1", "Artist A", 180),
        Track("Song 2", "Artist B", 200),
        Track("Song 3", "Artist C", 220)
    ]

    player = MediaPlayer(playlist)

    # Navigate while stopped
    print("\n--- Navigation while STOPPED ---")
    player.next_track()
    player.display_status()

    # Start playing
    player.play()

    # Navigate while playing (auto-continues playback)
    print("\n--- Navigation while PLAYING ---")
    player.next_track()
    player.display_status()

    # Try to go beyond last track
    player.next_track()

    # Go back
    player.previous_track()
    player.display_status()


def demonstrate_state_history():
    """Demonstrate tracking state history."""
    print("\n=== STATE HISTORY ===\n")

    playlist = [Track("Test Song", "Test Artist", 180)]
    player = MediaPlayer(playlist)

    # Perform various operations
    player.play()
    player.pause()
    player.play()
    player.stop()
    player.play()
    player.stop()

    # Show state history
    history = player.get_state_history()
    print(f"\n📜 State Transition History:")
    for i, state in enumerate(history, 1):
        print(f"  {i}. {state}")
    print(f"  {len(history) + 1}. {player.state_name} (current)")


def demonstrate_state_specific_behavior():
    """Demonstrate how same action has different behavior in different states."""
    print("\n=== STATE-SPECIFIC BEHAVIOR ===\n")

    playlist = [
        Track("Example Song", "Example Artist", 200),
        Track("Another Song", "Another Artist", 180)
    ]

    player = MediaPlayer(playlist)

    print("Testing PLAY button in different states:\n")

    # Play in Stopped state -> starts playback
    print("1. When STOPPED:")
    player.play()

    # Play in Playing state -> already playing
    print("\n2. When PLAYING:")
    player.play()

    # Pause, then play in Paused state -> resumes
    player.pause()
    print("\n3. When PAUSED:")
    player.play()

    print("\n" + "=" * 50)
    print("\nTesting PAUSE button in different states:\n")

    # Stop first
    player.stop()

    # Pause in Stopped state -> cannot pause
    print("1. When STOPPED:")
    player.pause()

    # Start playing and pause
    player.play()
    print("\n2. When PLAYING:")
    player.pause()

    # Pause in Paused state -> already paused
    print("\n3. When PAUSED:")
    player.pause()


def demonstrate_without_state_pattern():
    """Show what the code would look like without State pattern."""
    print("\n=== WITHOUT STATE PATTERN (Anti-pattern) ===\n")

    print("Without State Pattern, the MediaPlayer class would have:")
    print("""
class MediaPlayer:
    def __init__(self, playlist):
        self.playlist = playlist
        self.state = "stopped"  # String-based state!

    def play(self):
        if self.state == "stopped":
            print("Starting playback")
            self.state = "playing"
        elif self.state == "playing":
            print("Already playing")
        elif self.state == "paused":
            print("Resuming playback")
            self.state = "playing"

    def pause(self):
        if self.state == "stopped":
            print("Cannot pause")
        elif self.state == "playing":
            print("Pausing")
            self.state = "paused"
        elif self.state == "paused":
            print("Already paused")

    # More conditionals in every method!
    # Hard to maintain, test, and extend!
    """)

    print("Problems:")
    print("  ❌ Complex conditionals in every method")
    print("  ❌ Adding new states requires modifying all methods")
    print("  ❌ State transitions are scattered and implicit")
    print("  ❌ Violates Open/Closed Principle")
    print("  ❌ Difficult to test individual state behaviors")
    print("  ❌ No compile-time checking of state transitions")


def main():
    """Run all demonstrations."""
    print("State Pattern Example: Media Player\n")
    print("=" * 60)

    demonstrate_basic_state_transitions()
    print("\n" + "=" * 60)

    demonstrate_track_navigation()
    print("\n" + "=" * 60)

    demonstrate_state_history()
    print("\n" + "=" * 60)

    demonstrate_state_specific_behavior()
    print("\n" + "=" * 60)

    demonstrate_without_state_pattern()
    print("\n" + "=" * 60)

    print("\nAll demonstrations completed successfully!")


if __name__ == "__main__":
    main()
