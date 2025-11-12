"""
Strategy Pattern Example: Sorting Algorithms

This example demonstrates the Strategy Pattern using different sorting algorithms
that can be swapped at runtime. It shows how to define a family of algorithms,
encapsulate each one, and make them interchangeable through a common interface.

Key features:
- Strategy interface using Protocol
- Multiple sorting strategies (Bubble, Quick, Merge Sort)
- Context class that uses strategies
- Runtime strategy switching
- Performance comparison
- Type hints and comprehensive documentation
"""

from abc import ABC, abstractmethod
from typing import List, Protocol, Any, TypeVar
import time
import random

T = TypeVar('T')


class SortingStrategy(Protocol):
    """
    Protocol defining the interface for sorting strategies.

    Any object implementing this protocol can be used as a sorting strategy.
    """

    def sort(self, data: List[T]) -> List[T]:
        """
        Sort the given data and return a new sorted list.

        Args:
            data: List of comparable items to sort

        Returns:
            New sorted list (original list is not modified)
        """
        ...


class BubbleSortStrategy:
    """
    Bubble Sort implementation of the SortingStrategy.

    Bubble sort repeatedly steps through the list, compares adjacent elements
    and swaps them if they are in the wrong order. It's simple but inefficient
    for large datasets.
    """

    def sort(self, data: List[T]) -> List[T]:
        """
        Sort using bubble sort algorithm.

        Time Complexity: O(n²)
        Space Complexity: O(1) (in-place, but we create a copy)

        Args:
            data: List to sort

        Returns:
            Sorted copy of the list
        """
        # Create a copy to avoid modifying original
        sorted_data = data.copy()
        n = len(sorted_data)

        for i in range(n):
            # Flag to optimize: if no swaps in a pass, list is sorted
            swapped = False

            for j in range(0, n - i - 1):
                if sorted_data[j] > sorted_data[j + 1]:
                    # Swap elements
                    sorted_data[j], sorted_data[j + 1] = sorted_data[j + 1], sorted_data[j]
                    swapped = True

            if not swapped:
                break

        return sorted_data


class QuickSortStrategy:
    """
    Quick Sort implementation of the SortingStrategy.

    Quick sort picks a pivot element and partitions the array around the pivot.
    It's generally faster than bubble sort and widely used in practice.
    """

    def sort(self, data: List[T]) -> List[T]:
        """
        Sort using quick sort algorithm.

        Time Complexity: O(n log n) average, O(n²) worst case
        Space Complexity: O(log n) due to recursion

        Args:
            data: List to sort

        Returns:
            Sorted copy of the list
        """
        # Create a copy to avoid modifying original
        sorted_data = data.copy()

        def _quick_sort(arr: List[T], low: int, high: int) -> None:
            """Recursive quick sort helper function."""
            if low < high:
                # Partition the array and get pivot index
                pivot_index = _partition(arr, low, high)

                # Recursively sort left and right subarrays
                _quick_sort(arr, low, pivot_index - 1)
                _quick_sort(arr, pivot_index + 1, high)

        def _partition(arr: List[T], low: int, high: int) -> int:
            """Partition helper function."""
            # Choose rightmost element as pivot
            pivot = arr[high]

            # Index of smaller element
            i = low - 1

            for j in range(low, high):
                # If current element is smaller than pivot
                if arr[j] <= pivot:
                    i += 1
                    arr[i], arr[j] = arr[j], arr[i]

            # Place pivot in correct position
            arr[i + 1], arr[high] = arr[high], arr[i + 1]
            return i + 1

        _quick_sort(sorted_data, 0, len(sorted_data) - 1)
        return sorted_data


class MergeSortStrategy:
    """
    Merge Sort implementation of the SortingStrategy.

    Merge sort divides the array into two halves, recursively sorts them,
    and then merges the sorted halves. It's stable and predictable in performance.
    """

    def sort(self, data: List[T]) -> List[T]:
        """
        Sort using merge sort algorithm.

        Time Complexity: O(n log n) always
        Space Complexity: O(n) due to temporary arrays

        Args:
            data: List to sort

        Returns:
            Sorted copy of the list
        """
        if len(data) <= 1:
            return data.copy()

        # Split the array into two halves
        mid = len(data) // 2
        left_half = data[:mid]
        right_half = data[mid:]

        # Recursively sort both halves
        left_sorted = self.sort(left_half)
        right_sorted = self.sort(right_half)

        # Merge the sorted halves
        return self._merge(left_sorted, right_sorted)

    def _merge(self, left: List[T], right: List[T]) -> List[T]:
        """
        Merge two sorted lists into one sorted list.

        Args:
            left: First sorted list
            right: Second sorted list

        Returns:
            Merged sorted list
        """
        merged = []
        left_index = right_index = 0

        # Compare elements from both lists and add smaller one to merged
        while left_index < len(left) and right_index < len(right):
            if left[left_index] <= right[right_index]:
                merged.append(left[left_index])
                left_index += 1
            else:
                merged.append(right[right_index])
                right_index += 1

        # Add remaining elements from left list
        merged.extend(left[left_index:])

        # Add remaining elements from right list
        merged.extend(right[right_index:])

        return merged


class Sorter:
    """
    Context class that uses sorting strategies.

    This class demonstrates how to use different sorting strategies
    interchangeably without changing the client code.
    """

    def __init__(self, strategy: SortingStrategy):
        """
        Initialize sorter with a sorting strategy.

        Args:
            strategy: The sorting strategy to use
        """
        self._strategy = strategy

    def set_strategy(self, strategy: SortingStrategy) -> None:
        """
        Change the sorting strategy at runtime.

        Args:
            strategy: New sorting strategy to use
        """
        self._strategy = strategy

    def sort(self, data: List[T]) -> List[T]:
        """
        Sort the data using the current strategy.

        Args:
            data: List to sort

        Returns:
            Sorted list
        """
        return self._strategy.sort(data)

    def sort_with_timing(self, data: List[T]) -> tuple[List[T], float]:
        """
        Sort the data and measure execution time.

        Args:
            data: List to sort

        Returns:
            Tuple of (sorted_list, execution_time_in_seconds)
        """
        start_time = time.time()
        result = self._strategy.sort(data)
        end_time = time.time()

        execution_time = end_time - start_time
        return result, execution_time


def demonstrate_basic_usage():
    """Demonstrate basic strategy pattern usage."""
    print("=== Basic Strategy Usage ===\n")

    # Test data
    data = [64, 34, 25, 12, 22, 11, 90]
    print(f"Original data: {data}")

    # Create sorter with different strategies
    strategies = [
        ("Bubble Sort", BubbleSortStrategy()),
        ("Quick Sort", QuickSortStrategy()),
        ("Merge Sort", MergeSortStrategy())
    ]

    for name, strategy in strategies:
        sorter = Sorter(strategy)
        sorted_data = sorter.sort(data)
        print(f"{name}: {sorted_data}")

    print()


def demonstrate_runtime_switching():
    """Demonstrate switching strategies at runtime."""
    print("=== Runtime Strategy Switching ===\n")

    data = [8, 3, 1, 7, 4, 2, 9, 5, 6]
    print(f"Original data: {data}")

    # Start with bubble sort
    sorter = Sorter(BubbleSortStrategy())
    print("Using Bubble Sort:")
    result = sorter.sort(data)
    print(f"Result: {result}")

    # Switch to quick sort
    sorter.set_strategy(QuickSortStrategy())
    print("\nSwitched to Quick Sort:")
    result = sorter.sort(data)
    print(f"Result: {result}")

    # Switch to merge sort
    sorter.set_strategy(MergeSortStrategy())
    print("\nSwitched to Merge Sort:")
    result = sorter.sort(data)
    print(f"Result: {result}")

    print()


def demonstrate_performance_comparison():
    """Compare performance of different sorting strategies."""
    print("=== Performance Comparison ===\n")

    # Generate larger test data
    data_sizes = [100, 500, 1000]

    for size in data_sizes:
        print(f"Testing with {size} elements:")
        test_data = [random.randint(0, 1000) for _ in range(size)]

        strategies = [
            ("Bubble Sort", BubbleSortStrategy()),
            ("Quick Sort", QuickSortStrategy()),
            ("Merge Sort", MergeSortStrategy())
        ]

        for name, strategy in strategies:
            sorter = Sorter(strategy)
            _, execution_time = sorter.sort_with_timing(test_data)
            print(".4f")

        print()


def demonstrate_function_based_strategy():
    """Demonstrate using functions as strategies."""
    print("=== Function-Based Strategies ===\n")

    # Define sorting functions
    def reverse_sort(data: List[T]) -> List[T]:
        """Sort in descending order."""
        return sorted(data, reverse=True)

    def sort_by_length(data: List[str]) -> List[str]:
        """Sort strings by length."""
        return sorted(data, key=len)

    # Test data
    numbers = [3, 1, 4, 1, 5, 9, 2, 6]
    strings = ["apple", "a", "banana", "fig"]

    # Use function as strategy
    sorter = Sorter(reverse_sort)
    result = sorter.sort(numbers)
    print(f"Reverse sort: {result}")

    sorter.set_strategy(sort_by_length)
    result = sorter.sort(strings)
    print(f"Sort by length: {result}")

    print()


def demonstrate_callable_class_strategy():
    """Demonstrate using callable classes as strategies."""
    print("=== Callable Class Strategies ===\n")

    class CustomSortStrategy:
        """A strategy that sorts by custom criteria."""

        def __init__(self, key_func):
            """
            Initialize with a key function.

            Args:
                key_func: Function to extract comparison key
            """
            self.key_func = key_func

        def __call__(self, data: List[T]) -> List[T]:
            """Make the class callable as a strategy."""
            return sorted(data, key=self.key_func)

    # Test data
    words = ["Python", "Java", "C++", "JavaScript", "Go"]

    # Sort by string length
    strategy = CustomSortStrategy(len)
    sorter = Sorter(strategy)
    result = sorter.sort(words)
    print(f"Sort by length: {result}")

    # Sort by first letter
    strategy = CustomSortStrategy(lambda x: x[0])
    sorter.set_strategy(strategy)
    result = sorter.sort(words)
    print(f"Sort by first letter: {result}")

    print()


def main():
    """Run all demonstrations."""
    print("Strategy Pattern Example: Sorting Algorithms\n")

    demonstrate_basic_usage()
    demonstrate_runtime_switching()
    demonstrate_performance_comparison()
    demonstrate_function_based_strategy()
    demonstrate_callable_class_strategy()

    print("All demonstrations completed successfully!")


if __name__ == "__main__":
    main()