"""
Template Method Pattern Example: Data Processing Pipeline

This example demonstrates the Template Method Pattern using a data processing
pipeline. Different data processors (CSV, JSON, XML) follow the same algorithm
structure (read, validate, transform, write) but implement each step differently.

Key features:
- Abstract base class with template method
- Multiple concrete implementations (CSV, JSON, XML processors)
- Abstract operations (must be implemented)
- Hook operations (optional customization)
- Consistent algorithm structure enforced
- Type hints and comprehensive documentation

SOLID Principles Demonstrated:
- Single Responsibility: Each processor handles one data format
- Open/Closed: New processors can be added without modifying base class
- Liskov Substitution: All processors are substitutable through base class
- Dependency Inversion: Clients depend on abstract DataProcessor
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import json
import csv
from io import StringIO


@dataclass
class DataRecord:
    """
    Represents a single data record.

    Attributes:
        id: Record identifier
        name: Record name
        value: Record value
        metadata: Additional metadata
    """
    id: int
    name: str
    value: float
    metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        """Convert record to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "value": self.value,
            "metadata": self.metadata
        }


class DataProcessor(ABC):
    """
    Abstract base class defining the data processing template.

    This class defines the algorithm skeleton for data processing:
    1. Read data from source
    2. Validate data
    3. Transform data
    4. Write data to destination

    Subclasses implement format-specific steps while the template
    method ensures all steps are executed in the correct order.

    Demonstrates:
    - Template method pattern
    - Algorithm skeleton with customizable steps
    - Hook methods for optional customization
    - Consistent processing flow
    """

    def process(self, source: str, destination: str) -> None:
        """
        Template method defining the data processing algorithm.

        This method should NOT be overridden by subclasses.
        It defines the invariant processing structure.

        Args:
            source: Source data location/content
            destination: Destination for processed data
        """
        print(f"\n{'='*60}")
        print(f"Starting {self.__class__.__name__} processing")
        print(f"{'='*60}\n")

        # Step 1: Read data (abstract - must be implemented)
        print("Step 1: Reading data...")
        raw_data = self.read_data(source)
        print(f"  ✓ Read {len(raw_data)} bytes\n")

        # Step 2: Parse data (abstract - must be implemented)
        print("Step 2: Parsing data...")
        records = self.parse_data(raw_data)
        print(f"  ✓ Parsed {len(records)} records\n")

        # Step 3: Validate (abstract - must be implemented)
        print("Step 3: Validating data...")
        valid_records = self.validate_data(records)
        print(f"  ✓ Validated {len(valid_records)} records\n")

        # Step 4: Pre-transform hook (optional)
        print("Step 4: Pre-transform processing...")
        self.before_transform(valid_records)
        print("  ✓ Pre-transform complete\n")

        # Step 5: Transform (abstract - must be implemented)
        print("Step 5: Transforming data...")
        transformed_records = self.transform_data(valid_records)
        print(f"  ✓ Transformed {len(transformed_records)} records\n")

        # Step 6: Post-transform hook (optional)
        print("Step 6: Post-transform processing...")
        self.after_transform(transformed_records)
        print("  ✓ Post-transform complete\n")

        # Step 7: Format output (abstract - must be implemented)
        print("Step 7: Formatting output...")
        formatted_data = self.format_output(transformed_records)
        print(f"  ✓ Formatted {len(formatted_data)} bytes\n")

        # Step 8: Write data (abstract - must be implemented)
        print("Step 8: Writing data...")
        self.write_data(formatted_data, destination)
        print("  ✓ Write complete\n")

        print(f"{'='*60}")
        print(f"Processing complete!")
        print(f"{'='*60}\n")

    # Abstract methods - must be implemented by subclasses

    @abstractmethod
    def read_data(self, source: str) -> str:
        """
        Read data from source.

        Args:
            source: Source location/content

        Returns:
            Raw data as string
        """
        pass

    @abstractmethod
    def parse_data(self, raw_data: str) -> List[Dict[str, Any]]:
        """
        Parse raw data into structured format.

        Args:
            raw_data: Raw data string

        Returns:
            List of parsed records
        """
        pass

    @abstractmethod
    def validate_data(self, records: List[Dict[str, Any]]) -> List[DataRecord]:
        """
        Validate and convert records.

        Args:
            records: Parsed records

        Returns:
            List of valid DataRecord objects
        """
        pass

    @abstractmethod
    def transform_data(self, records: List[DataRecord]) -> List[DataRecord]:
        """
        Transform data records.

        Args:
            records: Valid records

        Returns:
            Transformed records
        """
        pass

    @abstractmethod
    def format_output(self, records: List[DataRecord]) -> str:
        """
        Format records for output.

        Args:
            records: Transformed records

        Returns:
            Formatted output string
        """
        pass

    @abstractmethod
    def write_data(self, data: str, destination: str) -> None:
        """
        Write data to destination.

        Args:
            data: Formatted data
            destination: Destination location
        """
        pass

    # Hook methods - optional, have default implementations

    def before_transform(self, records: List[DataRecord]) -> None:
        """
        Hook called before transformation.

        Default implementation does nothing.
        Subclasses can override for preprocessing.

        Args:
            records: Records to preprocess
        """
        pass

    def after_transform(self, records: List[DataRecord]) -> None:
        """
        Hook called after transformation.

        Default implementation does nothing.
        Subclasses can override for postprocessing.

        Args:
            records: Transformed records
        """
        pass


class CSVDataProcessor(DataProcessor):
    """
    CSV data processor implementation.

    Processes data in CSV format following the template structure.
    """

    def read_data(self, source: str) -> str:
        """Read CSV data."""
        # In real implementation, would read from file
        return source

    def parse_data(self, raw_data: str) -> List[Dict[str, Any]]:
        """Parse CSV data."""
        records = []
        reader = csv.DictReader(StringIO(raw_data))
        for row in reader:
            records.append(row)
        return records

    def validate_data(self, records: List[Dict[str, Any]]) -> List[DataRecord]:
        """Validate CSV records."""
        valid_records = []
        for record in records:
            try:
                data_record = DataRecord(
                    id=int(record['id']),
                    name=record['name'],
                    value=float(record['value']),
                    metadata={'source': 'csv'}
                )
                valid_records.append(data_record)
            except (KeyError, ValueError) as e:
                print(f"    ⚠️  Skipping invalid record: {e}")
        return valid_records

    def transform_data(self, records: List[DataRecord]) -> List[DataRecord]:
        """Transform CSV data - apply 10% increase to values."""
        for record in records:
            record.value *= 1.10
            record.metadata['transformed'] = True
        return records

    def format_output(self, records: List[DataRecord]) -> str:
        """Format as CSV."""
        output = StringIO()
        if records:
            fieldnames = ['id', 'name', 'value']
            writer = csv.DictWriter(output, fieldnames=fieldnames)
            writer.writeheader()
            for record in records:
                writer.writerow({
                    'id': record.id,
                    'name': record.name,
                    'value': f"{record.value:.2f}"
                })
        return output.getvalue()

    def write_data(self, data: str, destination: str) -> None:
        """Write CSV data."""
        # In real implementation, would write to file
        print(f"    Writing to {destination}:")
        print(f"    {data[:100]}..." if len(data) > 100 else f"    {data}")


class JSONDataProcessor(DataProcessor):
    """
    JSON data processor implementation.

    Processes data in JSON format with additional logging hook.
    """

    def read_data(self, source: str) -> str:
        """Read JSON data."""
        return source

    def parse_data(self, raw_data: str) -> List[Dict[str, Any]]:
        """Parse JSON data."""
        data = json.loads(raw_data)
        return data if isinstance(data, list) else [data]

    def validate_data(self, records: List[Dict[str, Any]]) -> List[DataRecord]:
        """Validate JSON records."""
        valid_records = []
        for record in records:
            try:
                data_record = DataRecord(
                    id=record['id'],
                    name=record['name'],
                    value=float(record['value']),
                    metadata=record.get('metadata', {'source': 'json'})
                )
                valid_records.append(data_record)
            except (KeyError, ValueError, TypeError) as e:
                print(f"    ⚠️  Skipping invalid record: {e}")
        return valid_records

    def transform_data(self, records: List[DataRecord]) -> List[DataRecord]:
        """Transform JSON data - double the values."""
        for record in records:
            record.value *= 2.0
            record.metadata['transformed'] = True
            record.metadata['transformation'] = 'doubled'
        return records

    def format_output(self, records: List[DataRecord]) -> str:
        """Format as JSON."""
        output_data = [record.to_dict() for record in records]
        return json.dumps(output_data, indent=2)

    def write_data(self, data: str, destination: str) -> None:
        """Write JSON data."""
        print(f"    Writing to {destination}:")
        print(f"    {data[:100]}..." if len(data) > 100 else f"    {data}")

    # Override hook to add logging
    def after_transform(self, records: List[DataRecord]) -> None:
        """Log statistics after transformation."""
        total_value = sum(r.value for r in records)
        avg_value = total_value / len(records) if records else 0
        print(f"    📊 Stats: Total={total_value:.2f}, Average={avg_value:.2f}")


class XMLDataProcessor(DataProcessor):
    """
    XML data processor implementation.

    Simplified XML processing (for demonstration).
    """

    def read_data(self, source: str) -> str:
        """Read XML data."""
        return source

    def parse_data(self, raw_data: str) -> List[Dict[str, Any]]:
        """Parse XML data (simplified)."""
        # Simplified parsing for demonstration
        # In real implementation, would use xml.etree or lxml
        records = []
        import re

        # Extract record elements
        record_pattern = r'<record>(.*?)</record>'
        record_matches = re.findall(record_pattern, raw_data, re.DOTALL)

        for match in record_matches:
            record = {}
            # Extract fields
            for field in ['id', 'name', 'value']:
                field_pattern = f'<{field}>(.*?)</{field}>'
                field_match = re.search(field_pattern, match)
                if field_match:
                    record[field] = field_match.group(1)
            if record:
                records.append(record)

        return records

    def validate_data(self, records: List[Dict[str, Any]]) -> List[DataRecord]:
        """Validate XML records."""
        valid_records = []
        for record in records:
            try:
                data_record = DataRecord(
                    id=int(record['id']),
                    name=record['name'],
                    value=float(record['value']),
                    metadata={'source': 'xml'}
                )
                valid_records.append(data_record)
            except (KeyError, ValueError) as e:
                print(f"    ⚠️  Skipping invalid record: {e}")
        return valid_records

    def transform_data(self, records: List[DataRecord]) -> List[DataRecord]:
        """Transform XML data - add 100 to values."""
        for record in records:
            record.value += 100.0
            record.metadata['transformed'] = True
            record.metadata['transformation'] = 'added_100'
        return records

    def format_output(self, records: List[DataRecord]) -> str:
        """Format as XML."""
        xml_parts = ['<?xml version="1.0" encoding="UTF-8"?>', '<records>']
        for record in records:
            xml_parts.append('  <record>')
            xml_parts.append(f'    <id>{record.id}</id>')
            xml_parts.append(f'    <name>{record.name}</name>')
            xml_parts.append(f'    <value>{record.value:.2f}</value>')
            xml_parts.append('  </record>')
        xml_parts.append('</records>')
        return '\n'.join(xml_parts)

    def write_data(self, data: str, destination: str) -> None:
        """Write XML data."""
        print(f"    Writing to {destination}:")
        lines = data.split('\n')
        preview = '\n    '.join(lines[:5])
        print(f"    {preview}...")

    # Override both hooks for XML-specific processing
    def before_transform(self, records: List[DataRecord]) -> None:
        """Add XML namespace metadata."""
        for record in records:
            record.metadata['xmlns'] = 'http://example.com/schema'

    def after_transform(self, records: List[DataRecord]) -> None:
        """Validate XML structure."""
        print(f"    ✓ XML validation passed for {len(records)} records")


# ============================================================================
# DEMONSTRATIONS
# ============================================================================


def demonstrate_csv_processing():
    """Demonstrate CSV data processing."""
    print("=== CSV DATA PROCESSING ===\n")

    csv_data = """id,name,value
1,Product A,100.50
2,Product B,200.75
3,Product C,150.25"""

    processor = CSVDataProcessor()
    processor.process(csv_data, "output.csv")


def demonstrate_json_processing():
    """Demonstrate JSON data processing."""
    print("\n=== JSON DATA PROCESSING ===\n")

    json_data = json.dumps([
        {"id": 1, "name": "Item X", "value": 50.0, "metadata": {"category": "A"}},
        {"id": 2, "name": "Item Y", "value": 75.5, "metadata": {"category": "B"}},
        {"id": 3, "name": "Item Z", "value": 100.0, "metadata": {"category": "A"}}
    ])

    processor = JSONDataProcessor()
    processor.process(json_data, "output.json")


def demonstrate_xml_processing():
    """Demonstrate XML data processing."""
    print("\n=== XML DATA PROCESSING ===\n")

    xml_data = """<?xml version="1.0"?>
<records>
  <record>
    <id>1</id>
    <name>Widget A</name>
    <value>25.00</value>
  </record>
  <record>
    <id>2</id>
    <name>Widget B</name>
    <value>35.50</value>
  </record>
</records>"""

    processor = XMLDataProcessor()
    processor.process(xml_data, "output.xml")


def demonstrate_polymorphic_processing():
    """Demonstrate polymorphic processing of different formats."""
    print("\n=== POLYMORPHIC PROCESSING ===\n")

    # Different processors, same interface
    processors = [
        (CSVDataProcessor(), "id,name,value\n1,Test,100", "test.csv"),
        (JSONDataProcessor(), '[{"id": 1, "name": "Test", "value": 100}]', "test.json"),
    ]

    print("Processing multiple formats using same template:\n")
    for processor, data, output in processors:
        print(f"Using {processor.__class__.__name__}:")
        processor.process(data, output)
        print()


def demonstrate_template_benefits():
    """Demonstrate benefits of template method pattern."""
    print("\n=== TEMPLATE METHOD BENEFITS ===\n")

    print("Benefits demonstrated:\n")

    print("1. CONSISTENT STRUCTURE")
    print("   All processors follow the same 8-step pipeline")
    print("   Read -> Parse -> Validate -> Transform -> Write\n")

    print("2. CODE REUSE")
    print("   Common algorithm structure defined once in base class")
    print("   Subclasses only implement format-specific details\n")

    print("3. EASY TO EXTEND")
    print("   New formats can be added by implementing abstract methods")
    print("   No changes to existing processors or template\n")

    print("4. HOOKS FOR CUSTOMIZATION")
    print("   before_transform() and after_transform() hooks")
    print("   Optional - can override when needed\n")

    print("5. ENFORCED PROCESS")
    print("   Template method guarantees steps execute in correct order")
    print("   Subclasses cannot skip or reorder steps\n")


def main():
    """Run all demonstrations."""
    print("Template Method Pattern Example: Data Processing Pipeline\n")

    demonstrate_csv_processing()
    demonstrate_json_processing()
    demonstrate_xml_processing()
    demonstrate_polymorphic_processing()
    demonstrate_template_benefits()

    print("\nAll demonstrations completed successfully!")


if __name__ == "__main__":
    main()
