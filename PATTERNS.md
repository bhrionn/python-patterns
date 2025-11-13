# Python Design Patterns - Study Cheat Sheet

## **Creational Patterns**
*Patterns that deal with object creation mechanisms*

### Singleton
Ensures a class has only one instance and provides a global access point to it.
```python
class Singleton:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
```
**Use when:** You need exactly one instance (database connections, loggers, configuration managers).

### Factory Method
Defines an interface for creating objects but lets subclasses decide which class to instantiate.
```python
from abc import ABC, abstractmethod

class Creator(ABC):
    @abstractmethod
    def factory_method(self):
        pass
    
    def operation(self):
        product = self.factory_method()
        return product.use()
```
**Use when:** You don't know the exact types of objects your code should work with ahead of time.

### Abstract Factory
Provides an interface for creating families of related objects without specifying their concrete classes.
```python
class GUIFactory(ABC):
    @abstractmethod
    def create_button(self): pass
    
    @abstractmethod
    def create_checkbox(self): pass
```
**Use when:** Your system needs to work with multiple families of related products.

### Builder
Separates complex object construction from its representation, allowing step-by-step construction.
```python
class QueryBuilder:
    def __init__(self):
        self.query = {}
    
    def select(self, fields):
        self.query['select'] = fields
        return self
    
    def where(self, condition):
        self.query['where'] = condition
        return self
    
    def build(self):
        return Query(self.query)
```
**Use when:** Constructing complex objects with many optional parameters or steps.

### Prototype
Creates new objects by copying existing instances (cloning).
```python
import copy

class Prototype:
    def clone(self):
        return copy.deepcopy(self)
```
**Use when:** Object creation is expensive or complex, and you want to copy existing instances.

---

## **Structural Patterns**
*Patterns that deal with object composition and relationships*

### Adapter
Converts one interface into another that clients expect, allowing incompatible interfaces to work together.
```python
class EuropeanSocket:
    def voltage(self): return 230

class USASocketAdapter:
    def __init__(self, socket):
        self.socket = socket
    
    def voltage(self):
        return 110  # Convert from 230V
```
**Use when:** You need to integrate classes with incompatible interfaces.

### Bridge
Separates abstraction from implementation so they can vary independently.
```python
class Device(ABC):
    @abstractmethod
    def turn_on(self): pass

class RemoteControl:
    def __init__(self, device: Device):
        self.device = device
    
    def power(self):
        self.device.turn_on()
```
**Use when:** You want to avoid permanent binding between abstraction and implementation.

### Composite
Composes objects into tree structures to represent part-whole hierarchies, treating individual objects and compositions uniformly.
```python
class Component(ABC):
    @abstractmethod
    def operation(self): pass

class Composite(Component):
    def __init__(self):
        self.children = []
    
    def add(self, component):
        self.children.append(component)
    
    def operation(self):
        for child in self.children:
            child.operation()
```
**Use when:** You need to represent hierarchies of objects (file systems, UI components, org charts).

### Decorator
Adds new functionality to objects dynamically without altering their structure.
```python
def log_calls(func):
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

@log_calls
def process_data(data):
    return data
```
**Use when:** You need to add responsibilities to objects dynamically and transparently.

### Facade
Provides a simplified interface to a complex subsystem.
```python
class ComputerFacade:
    def __init__(self):
        self.cpu = CPU()
        self.memory = Memory()
        self.disk = HardDrive()
    
    def start(self):
        self.cpu.freeze()
        self.memory.load()
        self.cpu.execute()
```
**Use when:** You want to provide a simple interface to a complex system.

### Flyweight
Shares common state between multiple objects to save memory.
```python
class CharacterFlyweight:
    _characters = {}
    
    @classmethod
    def get_character(cls, char):
        if char not in cls._characters:
            cls._characters[char] = Character(char)
        return cls._characters[char]
```
**Use when:** You need to support large numbers of similar objects efficiently.

### Proxy
Provides a surrogate or placeholder to control access to another object.
```python
class ImageProxy:
    def __init__(self, filename):
        self.filename = filename
        self._image = None
    
    def display(self):
        if self._image is None:
            self._image = RealImage(self.filename)
        self._image.display()
```
**Use when:** You need lazy initialization, access control, or remote object representation.

---

## **Behavioral Patterns**
*Patterns that deal with object collaboration and responsibility distribution*

### Chain of Responsibility
Passes requests along a chain of handlers where each handler decides to process or pass the request.
```python
class Handler(ABC):
    def __init__(self, successor=None):
        self.successor = successor
    
    def handle(self, request):
        if self.successor:
            return self.successor.handle(request)
```
**Use when:** Multiple objects can handle a request and the handler isn't known beforehand.

### Command
Encapsulates a request as an object, allowing parameterization and queuing of requests.
```python
class Command(ABC):
    @abstractmethod
    def execute(self): pass

class SaveCommand(Command):
    def __init__(self, document):
        self.document = document
    
    def execute(self):
        self.document.save()
```
**Use when:** You need to parameterize objects with operations, queue operations, or support undo.

### Iterator
Provides sequential access to elements without exposing underlying representation.
```python
class Iterator(ABC):
    @abstractmethod
    def __next__(self): pass

class BookIterator:
    def __init__(self, books):
        self.books = books
        self.index = 0
    
    def __next__(self):
        if self.index < len(self.books):
            result = self.books[self.index]
            self.index += 1
            return result
        raise StopIteration
```
**Use when:** You need to traverse collections without exposing their internal structure.

### Mediator
Defines an object that encapsulates how objects interact, promoting loose coupling.
```python
class ChatMediator:
    def __init__(self):
        self.users = []
    
    def send_message(self, message, sender):
        for user in self.users:
            if user != sender:
                user.receive(message)
```
**Use when:** Object interactions are complex and you want to centralize communication logic.

### Memento
Captures and externalizes an object's internal state for later restoration without violating encapsulation.
```python
class Memento:
    def __init__(self, state):
        self._state = state
    
    def get_state(self):
        return self._state

class Editor:
    def save(self):
        return Memento(self.text)
    
    def restore(self, memento):
        self.text = memento.get_state()
```
**Use when:** You need to implement undo/redo functionality or snapshots.

### Observer
Defines a one-to-many dependency where when one object changes state, all dependents are notified.
```python
class Subject:
    def __init__(self):
        self._observers = []
    
    def attach(self, observer):
        self._observers.append(observer)
    
    def notify(self):
        for observer in self._observers:
            observer.update(self)
```
**Use when:** Changes to one object require changing others, and you don't know how many objects need to change.

### State
Allows an object to alter its behavior when its internal state changes.
```python
class State(ABC):
    @abstractmethod
    def handle(self, context): pass

class Context:
    def __init__(self, state):
        self._state = state
    
    def request(self):
        self._state.handle(self)
```
**Use when:** Object behavior depends on its state and must change at runtime.

### Strategy
Defines a family of algorithms, encapsulates each one, and makes them interchangeable.
```python
class SortStrategy(ABC):
    @abstractmethod
    def sort(self, data): pass

class QuickSort(SortStrategy):
    def sort(self, data):
        # Quick sort implementation
        pass

class Sorter:
    def __init__(self, strategy: SortStrategy):
        self.strategy = strategy
    
    def sort(self, data):
        return self.strategy.sort(data)
```
**Use when:** You have multiple algorithms for a task and want to switch between them at runtime.

### Template Method
Defines the skeleton of an algorithm in a base class, letting subclasses override specific steps.
```python
class DataProcessor(ABC):
    def process(self):
        self.read_data()
        self.process_data()
        self.save_data()
    
    @abstractmethod
    def read_data(self): pass
    
    @abstractmethod
    def process_data(self): pass
```
**Use when:** You want to define the overall structure of an algorithm while letting subclasses customize certain steps.

### Visitor
Separates algorithms from the objects they operate on, allowing new operations without modifying classes.
```python
class Visitor(ABC):
    @abstractmethod
    def visit(self, element): pass

class Element(ABC):
    @abstractmethod
    def accept(self, visitor): pass
```
**Use when:** You need to perform operations across a heterogeneous collection of objects.

---

## **Quick Reference Guide**

**Need to create objects?** → Creational Patterns

**Need to compose objects?** → Structural Patterns

**Need objects to communicate?** → Behavioral Patterns

**Most commonly used in modern Python:** Singleton, Factory, Decorator, Observer, Strategy, Command

**Python-specific considerations:** Many patterns are simplified in Python due to first-class functions, decorators, and duck typing.
