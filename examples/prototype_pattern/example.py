"""
Prototype Pattern Example: Game Character System

This example demonstrates the Prototype Pattern using a game character system
where creating characters involves expensive initialization (loading graphics,
animations, sounds). Instead of recreating characters from scratch, we clone
prototypes and customize them.

Key features:
- Prototype interface using ABC
- Deep and shallow copying examples
- Prototype registry for managing multiple prototypes
- Performance comparison between creation and cloning
- Handling of complex nested objects
- Type hints and comprehensive documentation

SOLID Principles Demonstrated:
- Single Responsibility: Each class has one clear purpose
- Open/Closed: New character types can be added without modifying existing code
- Dependency Inversion: Client depends on Prototype abstraction, not concrete classes
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
import copy
import time
from enum import Enum


class CharacterClass(Enum):
    """Enumeration of character classes."""
    WARRIOR = "Warrior"
    MAGE = "Mage"
    ARCHER = "Archer"
    ROGUE = "Rogue"


@dataclass
class Equipment:
    """
    Represents equipment that a character can wear.

    This is a nested object to demonstrate deep vs shallow copying.

    Attributes:
        weapon: Weapon name
        armor: Armor name
        accessories: List of accessory names
    """
    weapon: str
    armor: str
    accessories: List[str] = field(default_factory=list)

    def __str__(self) -> str:
        acc = ", ".join(self.accessories) if self.accessories else "None"
        return f"Weapon: {self.weapon}, Armor: {self.armor}, Accessories: {acc}"


@dataclass
class Stats:
    """
    Character statistics.

    Attributes:
        health: Health points
        mana: Mana points
        strength: Strength attribute
        intelligence: Intelligence attribute
        agility: Agility attribute
    """
    health: int
    mana: int
    strength: int
    intelligence: int
    agility: int

    def __str__(self) -> str:
        return (f"HP: {self.health}, MP: {self.mana}, "
                f"STR: {self.strength}, INT: {self.intelligence}, AGI: {self.agility}")


class GameCharacter(ABC):
    """
    Abstract base class for game characters (Prototype interface).

    This class defines the prototype interface that all concrete
    character types must implement.
    """

    def __init__(
        self,
        name: str,
        char_class: CharacterClass,
        level: int,
        stats: Stats,
        equipment: Equipment
    ):
        """
        Initialize a game character.

        Args:
            name: Character name
            char_class: Character class
            level: Character level
            stats: Character statistics
            equipment: Character equipment
        """
        self.name = name
        self.char_class = char_class
        self.level = level
        self.stats = stats
        self.equipment = equipment
        # Simulate expensive initialization
        self._graphics_data = self._load_graphics()
        self._animation_data = self._load_animations()
        self._sound_data = self._load_sounds()

    def _load_graphics(self) -> Dict[str, Any]:
        """
        Simulate loading graphics from disk (expensive operation).

        Returns:
            Dictionary representing graphics data
        """
        # Simulate expensive I/O operation
        time.sleep(0.01)
        return {
            "textures": f"{self.char_class.value}_textures",
            "models": f"{self.char_class.value}_models",
            "sprites": f"{self.char_class.value}_sprites"
        }

    def _load_animations(self) -> Dict[str, Any]:
        """
        Simulate loading animations (expensive operation).

        Returns:
            Dictionary representing animation data
        """
        # Simulate expensive I/O operation
        time.sleep(0.01)
        return {
            "idle": f"{self.char_class.value}_idle_anim",
            "walk": f"{self.char_class.value}_walk_anim",
            "attack": f"{self.char_class.value}_attack_anim"
        }

    def _load_sounds(self) -> Dict[str, Any]:
        """
        Simulate loading sound effects (expensive operation).

        Returns:
            Dictionary representing sound data
        """
        # Simulate expensive I/O operation
        time.sleep(0.01)
        return {
            "attack": f"{self.char_class.value}_attack_sound",
            "hurt": f"{self.char_class.value}_hurt_sound",
            "death": f"{self.char_class.value}_death_sound"
        }

    @abstractmethod
    def clone(self) -> 'GameCharacter':
        """
        Clone this character (deep copy).

        Returns:
            A new instance that is a deep copy of this character
        """
        pass

    def shallow_clone(self) -> 'GameCharacter':
        """
        Create a shallow copy of this character.

        This is faster but shares nested objects (equipment, stats).
        Use with caution.

        Returns:
            A new instance that is a shallow copy
        """
        return copy.copy(self)

    def __str__(self) -> str:
        return (f"{self.name} (Level {self.level} {self.char_class.value})\n"
                f"  Stats: {self.stats}\n"
                f"  Equipment: {self.equipment}")


class Warrior(GameCharacter):
    """
    Warrior character class.

    Warriors are strong melee fighters with high health and strength.
    """

    def __init__(
        self,
        name: str = "Warrior",
        level: int = 1,
        stats: Optional[Stats] = None,
        equipment: Optional[Equipment] = None
    ):
        """
        Initialize a warrior character.

        Args:
            name: Character name
            level: Character level
            stats: Character statistics (defaults to warrior stats)
            equipment: Character equipment (defaults to warrior equipment)
        """
        if stats is None:
            stats = Stats(health=150, mana=30, strength=20, intelligence=5, agility=10)
        if equipment is None:
            equipment = Equipment(weapon="Iron Sword", armor="Plate Mail", accessories=["Shield"])

        super().__init__(name, CharacterClass.WARRIOR, level, stats, equipment)

    def clone(self) -> 'Warrior':
        """
        Clone this warrior using deep copy.

        Returns:
            A new Warrior instance that is a deep copy
        """
        return copy.deepcopy(self)


class Mage(GameCharacter):
    """
    Mage character class.

    Mages are powerful spellcasters with high mana and intelligence.
    """

    def __init__(
        self,
        name: str = "Mage",
        level: int = 1,
        stats: Optional[Stats] = None,
        equipment: Optional[Equipment] = None
    ):
        """
        Initialize a mage character.

        Args:
            name: Character name
            level: Character level
            stats: Character statistics (defaults to mage stats)
            equipment: Character equipment (defaults to mage equipment)
        """
        if stats is None:
            stats = Stats(health=80, mana=200, strength=5, intelligence=25, agility=8)
        if equipment is None:
            equipment = Equipment(weapon="Magic Staff", armor="Robe", accessories=["Spell Book", "Wand"])

        super().__init__(name, CharacterClass.MAGE, level, stats, equipment)

    def clone(self) -> 'Mage':
        """
        Clone this mage using deep copy.

        Returns:
            A new Mage instance that is a deep copy
        """
        return copy.deepcopy(self)


class Archer(GameCharacter):
    """
    Archer character class.

    Archers are ranged attackers with high agility.
    """

    def __init__(
        self,
        name: str = "Archer",
        level: int = 1,
        stats: Optional[Stats] = None,
        equipment: Optional[Equipment] = None
    ):
        """
        Initialize an archer character.

        Args:
            name: Character name
            level: Character level
            stats: Character statistics (defaults to archer stats)
            equipment: Character equipment (defaults to archer equipment)
        """
        if stats is None:
            stats = Stats(health=100, mana=50, strength=12, intelligence=10, agility=22)
        if equipment is None:
            equipment = Equipment(weapon="Longbow", armor="Leather Armor", accessories=["Quiver"])

        super().__init__(name, CharacterClass.ARCHER, level, stats, equipment)

    def clone(self) -> 'Archer':
        """
        Clone this archer using deep copy.

        Returns:
            A new Archer instance that is a deep copy
        """
        return copy.deepcopy(self)


class CharacterPrototypeRegistry:
    """
    Registry for managing character prototypes.

    This class provides centralized management of character prototypes,
    allowing clients to create new characters by cloning registered prototypes.

    Demonstrates:
    - Prototype registry pattern
    - Factory-like interface for prototype access
    - Centralized prototype management
    """

    def __init__(self):
        """Initialize the prototype registry."""
        self._prototypes: Dict[str, GameCharacter] = {}

    def register_prototype(self, key: str, prototype: GameCharacter) -> None:
        """
        Register a prototype in the registry.

        Args:
            key: Unique identifier for the prototype
            prototype: The prototype character to register
        """
        self._prototypes[key] = prototype

    def unregister_prototype(self, key: str) -> None:
        """
        Remove a prototype from the registry.

        Args:
            key: Identifier of the prototype to remove

        Raises:
            KeyError: If the key doesn't exist in the registry
        """
        del self._prototypes[key]

    def create_character(self, key: str, name: Optional[str] = None) -> GameCharacter:
        """
        Create a new character by cloning a registered prototype.

        Args:
            key: Identifier of the prototype to clone
            name: Optional name for the new character

        Returns:
            A new character cloned from the prototype

        Raises:
            KeyError: If the key doesn't exist in the registry
        """
        if key not in self._prototypes:
            raise KeyError(f"No prototype registered with key '{key}'")

        character = self._prototypes[key].clone()
        if name:
            character.name = name
        return character

    def list_prototypes(self) -> List[str]:
        """
        Get list of registered prototype keys.

        Returns:
            List of prototype identifiers
        """
        return list(self._prototypes.keys())


def demonstrate_basic_cloning():
    """Demonstrate basic character cloning."""
    print("=== Basic Character Cloning ===\n")

    # Create a warrior prototype
    warrior_proto = Warrior(name="Warrior Template", level=10)
    warrior_proto.stats.strength = 30  # Enhanced stats for template
    print("Original Warrior:")
    print(warrior_proto)
    print()

    # Clone the warrior
    warrior_clone = warrior_proto.clone()
    warrior_clone.name = "Ragnar"
    warrior_clone.level = 15
    print("Cloned Warrior (customized):")
    print(warrior_clone)
    print()

    # Verify independence
    warrior_proto.stats.strength = 50  # Modify original
    print("After modifying original's strength to 50:")
    print(f"Original strength: {warrior_proto.stats.strength}")
    print(f"Clone's strength: {warrior_clone.stats.strength} (unchanged)")
    print()


def demonstrate_shallow_vs_deep_copy():
    """Demonstrate the difference between shallow and deep copying."""
    print("=== Shallow vs Deep Copy ===\n")

    # Create original mage
    mage_original = Mage(name="Gandalf", level=20)
    print("Original Mage:")
    print(mage_original)
    print()

    # Shallow clone
    mage_shallow = mage_original.shallow_clone()
    mage_shallow.name = "Shallow Clone"

    # Deep clone
    mage_deep = mage_original.clone()
    mage_deep.name = "Deep Clone"

    # Modify original's equipment (nested object)
    mage_original.equipment.accessories.append("Magic Ring")

    print("After adding 'Magic Ring' to original's accessories:")
    print(f"Original accessories: {mage_original.equipment.accessories}")
    print(f"Shallow clone accessories: {mage_shallow.equipment.accessories} (shared!)")
    print(f"Deep clone accessories: {mage_deep.equipment.accessories} (independent)")
    print()


def demonstrate_prototype_registry():
    """Demonstrate using a prototype registry."""
    print("=== Prototype Registry ===\n")

    # Create registry
    registry = CharacterPrototypeRegistry()

    # Create and register prototypes
    warrior_proto = Warrior(name="Warrior Template", level=1)
    mage_proto = Mage(name="Mage Template", level=1)
    archer_proto = Archer(name="Archer Template", level=1)

    registry.register_prototype("warrior", warrior_proto)
    registry.register_prototype("mage", mage_proto)
    registry.register_prototype("archer", archer_proto)

    print(f"Registered prototypes: {registry.list_prototypes()}")
    print()

    # Create characters from prototypes
    characters = [
        registry.create_character("warrior", "Conan"),
        registry.create_character("warrior", "Beowulf"),
        registry.create_character("mage", "Merlin"),
        registry.create_character("archer", "Legolas"),
        registry.create_character("archer", "Robin Hood")
    ]

    print("Created characters from registry:")
    for char in characters:
        print(f"- {char.name} ({char.char_class.value}, Level {char.level})")
    print()


def demonstrate_performance_comparison():
    """Compare performance of creation vs cloning."""
    print("=== Performance Comparison ===\n")

    # Create original (expensive)
    print("Creating original warrior (with expensive initialization)...")
    start_time = time.time()
    original = Warrior(name="Template")
    creation_time = time.time() - start_time
    print(f"Creation time: {creation_time:.4f} seconds")
    print()

    # Clone multiple times (fast)
    print("Cloning 10 warriors from prototype...")
    start_time = time.time()
    clones = []
    for i in range(10):
        clone = original.clone()
        clone.name = f"Warrior {i+1}"
        clones.append(clone)
    cloning_time = time.time() - start_time
    print(f"Total cloning time: {cloning_time:.4f} seconds")
    print(f"Average time per clone: {cloning_time/10:.4f} seconds")
    print()

    # Create from scratch multiple times (expensive)
    print("Creating 10 warriors from scratch...")
    start_time = time.time()
    warriors = []
    for i in range(10):
        warrior = Warrior(name=f"Warrior {i+1}")
        warriors.append(warrior)
    from_scratch_time = time.time() - start_time
    print(f"Total creation time: {from_scratch_time:.4f} seconds")
    print(f"Average time per creation: {from_scratch_time/10:.4f} seconds")
    print()

    speedup = from_scratch_time / cloning_time
    print(f"Speedup: {speedup:.2f}x faster using cloning")
    print()


def demonstrate_customization_after_cloning():
    """Demonstrate customizing cloned characters."""
    print("=== Customization After Cloning ===\n")

    # Create base archer
    base_archer = Archer(name="Base Archer", level=5)
    print("Base Archer Template:")
    print(base_archer)
    print()

    # Clone and customize for different roles
    print("Creating specialized archers from template:\n")

    # Sniper archer (high agility)
    sniper = base_archer.clone()
    sniper.name = "Sniper"
    sniper.stats.agility += 10
    sniper.equipment.weapon = "Precision Bow"
    sniper.equipment.accessories.append("Scope")
    print("1. Sniper Archer:")
    print(sniper)
    print()

    # Tank archer (high health)
    tank = base_archer.clone()
    tank.name = "Tank Archer"
    tank.stats.health += 50
    tank.stats.agility -= 5
    tank.equipment.armor = "Heavy Armor"
    tank.equipment.accessories.append("Shield")
    print("2. Tank Archer:")
    print(tank)
    print()

    # Magic archer (mana-based)
    magic = base_archer.clone()
    magic.name = "Magic Archer"
    magic.stats.mana += 100
    magic.stats.intelligence += 15
    magic.equipment.weapon = "Enchanted Bow"
    magic.equipment.accessories.append("Magic Quiver")
    print("3. Magic Archer:")
    print(magic)
    print()


def main():
    """Run all demonstrations."""
    print("Prototype Pattern Example: Game Character System\n")

    demonstrate_basic_cloning()
    demonstrate_shallow_vs_deep_copy()
    demonstrate_prototype_registry()
    demonstrate_performance_comparison()
    demonstrate_customization_after_cloning()

    print("All demonstrations completed successfully!")


if __name__ == "__main__":
    main()
