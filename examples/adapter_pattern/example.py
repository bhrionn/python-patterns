"""
Adapter Pattern Example: Media Player System

This example demonstrates the Adapter Pattern using a media player system
that integrates multiple incompatible media libraries. The pattern allows
different audio/video libraries with varying interfaces to work seamlessly
with a unified player interface.

Key features:
- Protocol-based target interface for duck typing
- Multiple adapters for different incompatible interfaces
- Object composition (preferred over inheritance)
- Type hints and comprehensive documentation
- Adherence to Open/Closed Principle
- Error translation and handling
"""

from abc import ABC, abstractmethod
from typing import Protocol, Optional
from enum import Enum, auto


# ============================================================================
# Target Interface (What the client expects)
# ============================================================================


class MediaPlayer(Protocol):
    """
    Protocol defining the target interface for media playback.

    This protocol represents the interface expected by client code.
    All adapters must implement this interface to be compatible.
    """

    def play(self, filename: str) -> str:
        """
        Play a media file.

        Args:
            filename: Path to the media file to play

        Returns:
            Status message indicating playback state
        """
        ...

    def stop(self) -> str:
        """
        Stop media playback.

        Returns:
            Status message indicating stop state
        """
        ...

    def get_status(self) -> str:
        """
        Get current playback status.

        Returns:
            Current status information
        """
        ...


# ============================================================================
# Simple Implementation (Already compatible with target interface)
# ============================================================================


class SimpleMediaPlayer:
    """
    Simple media player that already implements the target interface.

    This player doesn't need an adapter as it's already compatible
    with the MediaPlayer protocol.
    """

    def __init__(self):
        """Initialize the simple media player."""
        self._current_file: Optional[str] = None
        self._is_playing: bool = False

    def play(self, filename: str) -> str:
        """
        Play a media file.

        Args:
            filename: Path to the media file

        Returns:
            Status message
        """
        self._current_file = filename
        self._is_playing = True
        return f"SimpleMediaPlayer: Playing '{filename}'"

    def stop(self) -> str:
        """
        Stop playback.

        Returns:
            Status message
        """
        if self._is_playing:
            self._is_playing = False
            return f"SimpleMediaPlayer: Stopped '{self._current_file}'"
        return "SimpleMediaPlayer: Not playing"

    def get_status(self) -> str:
        """
        Get playback status.

        Returns:
            Current status
        """
        if self._is_playing:
            return f"SimpleMediaPlayer: Playing '{self._current_file}'"
        return "SimpleMediaPlayer: Idle"


# ============================================================================
# Adaptee 1: Advanced Media Library (Incompatible Interface)
# ============================================================================


class PlaybackState(Enum):
    """Enumeration of playback states for AdvancedMediaLibrary."""
    IDLE = auto()
    LOADING = auto()
    PLAYING = auto()
    PAUSED = auto()
    STOPPED = auto()


class AdvancedMediaLibrary:
    """
    Third-party advanced media library with incompatible interface.

    This represents an external library that we cannot modify.
    It has a completely different method naming and structure.
    """

    def __init__(self):
        """Initialize the advanced media library."""
        self._media_source: Optional[str] = None
        self._state: PlaybackState = PlaybackState.IDLE
        self._codec_info: str = "Unknown"

    def load_media_source(self, source_path: str, codec: str = "auto") -> bool:
        """
        Load a media source with specified codec.

        Args:
            source_path: Path to media file
            codec: Codec to use for playback

        Returns:
            True if loaded successfully, False otherwise
        """
        self._media_source = source_path
        self._codec_info = codec
        self._state = PlaybackState.LOADING
        return True

    def start_playback(self) -> bool:
        """
        Start playing loaded media.

        Returns:
            True if playback started, False otherwise

        Raises:
            RuntimeError: If no media is loaded
        """
        if self._media_source is None:
            raise RuntimeError("No media source loaded")

        self._state = PlaybackState.PLAYING
        return True

    def halt_playback(self) -> None:
        """Halt the current playback."""
        self._state = PlaybackState.STOPPED

    def get_playback_state(self) -> PlaybackState:
        """
        Get current playback state.

        Returns:
            Current PlaybackState
        """
        return self._state

    def get_media_info(self) -> dict:
        """
        Get information about current media.

        Returns:
            Dictionary with media information
        """
        return {
            "source": self._media_source,
            "codec": self._codec_info,
            "state": self._state.name
        }


# ============================================================================
# Adaptee 2: Legacy Audio System (Incompatible Interface)
# ============================================================================


class LegacyAudioSystem:
    """
    Legacy audio system with outdated interface.

    This represents a legacy system that we want to integrate
    but cannot modify. It has an old-style procedural interface.
    """

    def __init__(self):
        """Initialize the legacy audio system."""
        self.audio_file_path: str = ""
        self.is_audio_active: bool = False
        self.audio_format: str = "wav"

    def open_audio_file(self, file_path: str, audio_format: str = "wav") -> int:
        """
        Open an audio file for playback.

        Args:
            file_path: Path to audio file
            audio_format: Audio format (wav, mp3, etc.)

        Returns:
            Status code (0 for success, -1 for error)
        """
        if not file_path:
            return -1

        self.audio_file_path = file_path
        self.audio_format = audio_format
        return 0

    def begin_audio(self) -> int:
        """
        Begin audio playback.

        Returns:
            Status code (0 for success, -1 for error)
        """
        if not self.audio_file_path:
            return -1

        self.is_audio_active = True
        return 0

    def terminate_audio(self) -> int:
        """
        Terminate audio playback.

        Returns:
            Status code (0 for success)
        """
        self.is_audio_active = False
        return 0

    def query_audio_status(self) -> tuple[bool, str]:
        """
        Query current audio status.

        Returns:
            Tuple of (is_active, file_path)
        """
        return (self.is_audio_active, self.audio_file_path)


# ============================================================================
# Adapter 1: Advanced Media Library Adapter
# ============================================================================


class AdvancedMediaAdapter:
    """
    Adapter for AdvancedMediaLibrary to MediaPlayer interface.

    This adapter wraps the AdvancedMediaLibrary and translates
    calls from the MediaPlayer interface to the library's interface.
    Implements Single Responsibility (only adapts interface) and
    Open/Closed (can add new adapters without modifying existing code).
    """

    def __init__(self, advanced_library: AdvancedMediaLibrary):
        """
        Initialize the adapter with an AdvancedMediaLibrary instance.

        Args:
            advanced_library: Instance of AdvancedMediaLibrary to adapt
        """
        self._library = advanced_library

    def play(self, filename: str) -> str:
        """
        Play media file by adapting to AdvancedMediaLibrary interface.

        Translates simple play() call to load_media_source() and
        start_playback() sequence.

        Args:
            filename: Path to media file

        Returns:
            Status message

        Raises:
            ValueError: If playback fails
        """
        try:
            # Translate single play() to two-step process
            self._library.load_media_source(filename, codec="auto")
            self._library.start_playback()
            return f"AdvancedMediaLibrary: Playing '{filename}' with auto codec"
        except RuntimeError as e:
            raise ValueError(f"Failed to play media: {e}") from e

    def stop(self) -> str:
        """
        Stop playback by adapting to halt_playback().

        Returns:
            Status message
        """
        self._library.halt_playback()
        info = self._library.get_media_info()
        return f"AdvancedMediaLibrary: Stopped '{info['source']}'"

    def get_status(self) -> str:
        """
        Get status by adapting to get_playback_state() and get_media_info().

        Returns:
            Current status string
        """
        info = self._library.get_media_info()
        state = self._library.get_playback_state()
        return f"AdvancedMediaLibrary: {state.name} - '{info['source']}' ({info['codec']})"


# ============================================================================
# Adapter 2: Legacy Audio System Adapter
# ============================================================================


class LegacyAudioAdapter:
    """
    Adapter for LegacyAudioSystem to MediaPlayer interface.

    This adapter wraps the LegacyAudioSystem and translates
    calls from the MediaPlayer interface to the legacy system's
    procedural interface, including error code translation.
    """

    def __init__(self, legacy_system: LegacyAudioSystem):
        """
        Initialize the adapter with a LegacyAudioSystem instance.

        Args:
            legacy_system: Instance of LegacyAudioSystem to adapt
        """
        self._system = legacy_system

    def play(self, filename: str) -> str:
        """
        Play audio file by adapting to legacy system interface.

        Translates play() to open_audio_file() and begin_audio() sequence,
        and converts error codes to exceptions.

        Args:
            filename: Path to audio file

        Returns:
            Status message

        Raises:
            ValueError: If playback fails (translates error codes)
        """
        # Translate to legacy two-step process
        result = self._system.open_audio_file(filename, audio_format="mp3")
        if result != 0:
            raise ValueError(f"Failed to open audio file: {filename}")

        result = self._system.begin_audio()
        if result != 0:
            raise ValueError(f"Failed to begin audio playback: {filename}")

        return f"LegacyAudioSystem: Playing '{filename}' in {self._system.audio_format} format"

    def stop(self) -> str:
        """
        Stop playback by adapting to terminate_audio().

        Returns:
            Status message
        """
        filename = self._system.audio_file_path
        self._system.terminate_audio()
        return f"LegacyAudioSystem: Stopped '{filename}'"

    def get_status(self) -> str:
        """
        Get status by adapting to query_audio_status().

        Translates tuple return to string message.

        Returns:
            Current status string
        """
        is_active, filepath = self._system.query_audio_status()
        state = "Playing" if is_active else "Idle"
        return f"LegacyAudioSystem: {state} - '{filepath}'"


# ============================================================================
# Client Code
# ============================================================================


class UniversalMediaPlayer:
    """
    Universal media player that works with any MediaPlayer-compatible object.

    This client demonstrates the benefit of the Adapter pattern:
    it works with any object conforming to the MediaPlayer protocol,
    regardless of the underlying implementation.

    Follows Dependency Inversion Principle by depending on the
    MediaPlayer protocol (abstraction) rather than concrete classes.
    """

    def __init__(self, player: MediaPlayer):
        """
        Initialize with a media player implementation.

        Args:
            player: Any object implementing MediaPlayer protocol
        """
        self._player = player

    def play_media(self, filename: str) -> str:
        """
        Play media using the configured player.

        Args:
            filename: Path to media file

        Returns:
            Playback result message
        """
        try:
            result = self._player.play(filename)
            return result
        except (ValueError, RuntimeError) as e:
            return f"Error: {e}"

    def stop_media(self) -> str:
        """
        Stop media playback.

        Returns:
            Stop result message
        """
        return self._player.stop()

    def check_status(self) -> str:
        """
        Check player status.

        Returns:
            Status message
        """
        return self._player.get_status()


# ============================================================================
# Demonstration Functions
# ============================================================================


def demonstrate_simple_player():
    """Demonstrate using the simple player (no adapter needed)."""
    print("=== Simple Media Player (No Adapter Needed) ===")

    simple = SimpleMediaPlayer()
    player = UniversalMediaPlayer(simple)

    print(player.play_media("song.mp3"))
    print(player.check_status())
    print(player.stop_media())
    print(player.check_status())
    print()


def demonstrate_advanced_library_adapter():
    """Demonstrate adapting the advanced media library."""
    print("=== Advanced Media Library (With Adapter) ===")

    # Create the incompatible library
    advanced_lib = AdvancedMediaLibrary()

    # Wrap it with an adapter
    adapter = AdvancedMediaAdapter(advanced_lib)

    # Use it through the universal interface
    player = UniversalMediaPlayer(adapter)

    print(player.play_media("movie.mp4"))
    print(player.check_status())
    print(player.stop_media())
    print(player.check_status())
    print()


def demonstrate_legacy_audio_adapter():
    """Demonstrate adapting the legacy audio system."""
    print("=== Legacy Audio System (With Adapter) ===")

    # Create the legacy system
    legacy = LegacyAudioSystem()

    # Wrap it with an adapter
    adapter = LegacyAudioAdapter(legacy)

    # Use it through the universal interface
    player = UniversalMediaPlayer(adapter)

    print(player.play_media("podcast.mp3"))
    print(player.check_status())
    print(player.stop_media())
    print(player.check_status())
    print()


def demonstrate_polymorphism():
    """Demonstrate polymorphic usage of different players."""
    print("=== Polymorphic Usage (All Through Same Interface) ===")

    # Create different players with different implementations
    players = [
        ("Simple Player", UniversalMediaPlayer(SimpleMediaPlayer())),
        ("Advanced Library", UniversalMediaPlayer(
            AdvancedMediaAdapter(AdvancedMediaLibrary())
        )),
        ("Legacy Audio", UniversalMediaPlayer(
            LegacyAudioAdapter(LegacyAudioSystem())
        ))
    ]

    # Play different files with different players
    files = ["track1.mp3", "video.mp4", "audio.wav"]

    for (name, player), filename in zip(players, files):
        print(f"--- Using {name} ---")
        print(player.play_media(filename))
        print(player.check_status())
        print()


def demonstrate_error_handling():
    """Demonstrate error handling and translation."""
    print("=== Error Handling and Translation ===")

    # Test error handling with advanced library
    print("--- Testing Advanced Library Error ---")
    advanced_lib = AdvancedMediaLibrary()
    adapter = AdvancedMediaAdapter(advanced_lib)
    player = UniversalMediaPlayer(adapter)

    # This will work
    print(player.play_media("test.mp4"))

    # Test with legacy system - empty filename
    print("\n--- Testing Legacy System Error ---")
    legacy = LegacyAudioSystem()
    adapter = LegacyAudioAdapter(legacy)
    player = UniversalMediaPlayer(adapter)

    # This will raise an error (translated from error code)
    print(player.play_media(""))
    print()


def demonstrate_interchangeability():
    """Demonstrate runtime interchangeability of adapters."""
    print("=== Runtime Interchangeability ===")

    # Create a playlist with different player implementations
    playlist = [
        ("Opening Theme", SimpleMediaPlayer()),
        ("Main Content", AdvancedMediaAdapter(AdvancedMediaLibrary())),
        ("Closing Credits", LegacyAudioAdapter(LegacyAudioSystem()))
    ]

    for filename, player_impl in playlist:
        player = UniversalMediaPlayer(player_impl)
        print(f"Playing: {filename}")
        print(player.play_media(f"{filename.lower().replace(' ', '_')}.mp3"))
        print()


# ============================================================================
# Main Function
# ============================================================================


def main():
    """Run all demonstrations of the Adapter Pattern."""
    print("Adapter Pattern Example: Media Player System\n")

    demonstrate_simple_player()
    demonstrate_advanced_library_adapter()
    demonstrate_legacy_audio_adapter()
    demonstrate_polymorphism()
    demonstrate_error_handling()
    demonstrate_interchangeability()

    print("All demonstrations completed successfully!")


if __name__ == "__main__":
    main()
