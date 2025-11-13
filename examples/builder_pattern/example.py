"""
Builder Pattern Example: SQL Query Builder

This example demonstrates the Builder Pattern using a SQL query builder system
that constructs complex database queries step by step. The pattern separates
the construction of queries from their representation, enabling flexible and
readable query creation.

Key features:
- Fluent interface with method chaining
- Immutable query objects after building
- Validation at build time
- Multiple query types (SELECT, INSERT, UPDATE, DELETE)
- Type hints and comprehensive documentation
- Adherence to Single Responsibility and Open/Closed Principles
- Director pattern for common query templates
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any, Union
from dataclasses import dataclass, field
from enum import Enum


# ============================================================================
# Product Classes (The complex objects being built)
# ============================================================================


@dataclass(frozen=True)
class SelectQuery:
    """
    Immutable SELECT query representation.

    This is the product built by SelectQueryBuilder. Once built,
    the query cannot be modified, ensuring thread safety and predictability.

    Attributes:
        columns: List of column names to select
        table: Table name to query from
        joins: List of JOIN clauses
        where: WHERE clause condition
        group_by: List of columns to group by
        having: HAVING clause condition
        order_by: List of ORDER BY clauses
        limit: Maximum number of rows to return
        offset: Number of rows to skip
    """
    columns: List[str] = field(default_factory=lambda: ["*"])
    table: str = ""
    joins: List[str] = field(default_factory=list)
    where: Optional[str] = None
    group_by: List[str] = field(default_factory=list)
    having: Optional[str] = None
    order_by: List[str] = field(default_factory=list)
    limit: Optional[int] = None
    offset: Optional[int] = None

    def to_sql(self) -> str:
        """
        Convert query to SQL string.

        Returns:
            SQL query string

        Raises:
            ValueError: If query is invalid
        """
        if not self.table:
            raise ValueError("Table name is required")

        # Build SELECT clause
        columns_str = ", ".join(self.columns)
        sql = f"SELECT {columns_str} FROM {self.table}"

        # Add JOINs
        if self.joins:
            sql += " " + " ".join(self.joins)

        # Add WHERE clause
        if self.where:
            sql += f" WHERE {self.where}"

        # Add GROUP BY
        if self.group_by:
            group_by_str = ", ".join(self.group_by)
            sql += f" GROUP BY {group_by_str}"

        # Add HAVING
        if self.having:
            sql += f" HAVING {self.having}"

        # Add ORDER BY
        if self.order_by:
            order_by_str = ", ".join(self.order_by)
            sql += f" ORDER BY {order_by_str}"

        # Add LIMIT
        if self.limit is not None:
            sql += f" LIMIT {self.limit}"

        # Add OFFSET
        if self.offset is not None:
            sql += f" OFFSET {self.offset}"

        return sql


@dataclass(frozen=True)
class InsertQuery:
    """
    Immutable INSERT query representation.

    Attributes:
        table: Table name to insert into
        columns: List of column names
        values: List of values to insert
    """
    table: str = ""
    columns: List[str] = field(default_factory=list)
    values: List[Any] = field(default_factory=list)

    def to_sql(self) -> str:
        """
        Convert query to SQL string.

        Returns:
            SQL query string

        Raises:
            ValueError: If query is invalid
        """
        if not self.table:
            raise ValueError("Table name is required")
        if not self.columns:
            raise ValueError("Columns are required")
        if not self.values:
            raise ValueError("Values are required")
        if len(self.columns) != len(self.values):
            raise ValueError("Number of columns must match number of values")

        columns_str = ", ".join(self.columns)
        # Convert values to SQL representation
        values_str = ", ".join(self._format_value(v) for v in self.values)

        return f"INSERT INTO {self.table} ({columns_str}) VALUES ({values_str})"

    @staticmethod
    def _format_value(value: Any) -> str:
        """Format a value for SQL."""
        if value is None:
            return "NULL"
        elif isinstance(value, str):
            # Escape single quotes
            escaped = value.replace("'", "''")
            return f"'{escaped}'"
        elif isinstance(value, bool):
            return "TRUE" if value else "FALSE"
        else:
            return str(value)


@dataclass(frozen=True)
class UpdateQuery:
    """
    Immutable UPDATE query representation.

    Attributes:
        table: Table name to update
        updates: Dictionary of column-value pairs to update
        where: WHERE clause condition
    """
    table: str = ""
    updates: Dict[str, Any] = field(default_factory=dict)
    where: Optional[str] = None

    def to_sql(self) -> str:
        """
        Convert query to SQL string.

        Returns:
            SQL query string

        Raises:
            ValueError: If query is invalid
        """
        if not self.table:
            raise ValueError("Table name is required")
        if not self.updates:
            raise ValueError("Updates are required")

        # Build SET clause
        set_pairs = []
        for column, value in self.updates.items():
            formatted_value = InsertQuery._format_value(value)
            set_pairs.append(f"{column} = {formatted_value}")

        set_str = ", ".join(set_pairs)
        sql = f"UPDATE {self.table} SET {set_str}"

        # Add WHERE clause
        if self.where:
            sql += f" WHERE {self.where}"

        return sql


# ============================================================================
# Builder Classes (Step-by-step construction)
# ============================================================================


class SelectQueryBuilder:
    """
    Builder for constructing SELECT queries with fluent interface.

    This builder provides a readable, step-by-step approach to building
    complex SELECT queries. Methods return self to enable method chaining.

    Example:
        >>> builder = SelectQueryBuilder()
        >>> query = (builder
        ...     .select(["name", "email"])
        ...     .from_table("users")
        ...     .where("age > 18")
        ...     .order_by(["name ASC"])
        ...     .limit(10)
        ...     .build())
    """

    def __init__(self):
        """Initialize a new SelectQueryBuilder with default values."""
        self._columns: List[str] = ["*"]
        self._table: str = ""
        self._joins: List[str] = []
        self._where: Optional[str] = None
        self._group_by: List[str] = []
        self._having: Optional[str] = None
        self._order_by: List[str] = []
        self._limit: Optional[int] = None
        self._offset: Optional[int] = None

    def select(self, columns: List[str]) -> "SelectQueryBuilder":
        """
        Specify columns to select.

        Args:
            columns: List of column names

        Returns:
            Self for method chaining

        Raises:
            ValueError: If columns list is empty
        """
        if not columns:
            raise ValueError("Columns list cannot be empty")
        self._columns = columns.copy()
        return self

    def from_table(self, table: str) -> "SelectQueryBuilder":
        """
        Specify table to query from.

        Args:
            table: Table name

        Returns:
            Self for method chaining

        Raises:
            ValueError: If table name is empty
        """
        if not table:
            raise ValueError("Table name cannot be empty")
        self._table = table
        return self

    def join(self, join_clause: str) -> "SelectQueryBuilder":
        """
        Add a JOIN clause.

        Args:
            join_clause: Complete JOIN clause (e.g., "INNER JOIN orders ON users.id = orders.user_id")

        Returns:
            Self for method chaining
        """
        if join_clause:
            self._joins.append(join_clause)
        return self

    def where(self, condition: str) -> "SelectQueryBuilder":
        """
        Set WHERE clause condition.

        Args:
            condition: WHERE condition

        Returns:
            Self for method chaining
        """
        self._where = condition
        return self

    def group_by(self, columns: List[str]) -> "SelectQueryBuilder":
        """
        Specify columns to group by.

        Args:
            columns: List of column names

        Returns:
            Self for method chaining
        """
        self._group_by = columns.copy()
        return self

    def having(self, condition: str) -> "SelectQueryBuilder":
        """
        Set HAVING clause condition.

        Args:
            condition: HAVING condition

        Returns:
            Self for method chaining
        """
        self._having = condition
        return self

    def order_by(self, columns: List[str]) -> "SelectQueryBuilder":
        """
        Specify ordering.

        Args:
            columns: List of ORDER BY clauses (e.g., ["name ASC", "age DESC"])

        Returns:
            Self for method chaining
        """
        self._order_by = columns.copy()
        return self

    def limit(self, limit: int) -> "SelectQueryBuilder":
        """
        Set maximum number of rows to return.

        Args:
            limit: Maximum number of rows

        Returns:
            Self for method chaining

        Raises:
            ValueError: If limit is negative
        """
        if limit < 0:
            raise ValueError("Limit cannot be negative")
        self._limit = limit
        return self

    def offset(self, offset: int) -> "SelectQueryBuilder":
        """
        Set number of rows to skip.

        Args:
            offset: Number of rows to skip

        Returns:
            Self for method chaining

        Raises:
            ValueError: If offset is negative
        """
        if offset < 0:
            raise ValueError("Offset cannot be negative")
        self._offset = offset
        return self

    def build(self) -> SelectQuery:
        """
        Build the final immutable SelectQuery.

        Returns:
            Immutable SelectQuery instance

        Raises:
            ValueError: If required fields are not set
        """
        if not self._table:
            raise ValueError("Table name is required. Use from_table() to set it.")

        return SelectQuery(
            columns=self._columns.copy(),
            table=self._table,
            joins=self._joins.copy(),
            where=self._where,
            group_by=self._group_by.copy(),
            having=self._having,
            order_by=self._order_by.copy(),
            limit=self._limit,
            offset=self._offset
        )

    def reset(self) -> "SelectQueryBuilder":
        """
        Reset the builder to default state for reuse.

        Returns:
            Self for method chaining
        """
        self.__init__()
        return self


class InsertQueryBuilder:
    """
    Builder for constructing INSERT queries with fluent interface.

    Example:
        >>> builder = InsertQueryBuilder()
        >>> query = (builder
        ...     .into("users")
        ...     .columns(["name", "email", "age"])
        ...     .values(["John Doe", "john@example.com", 30])
        ...     .build())
    """

    def __init__(self):
        """Initialize a new InsertQueryBuilder."""
        self._table: str = ""
        self._columns: List[str] = []
        self._values: List[Any] = []

    def into(self, table: str) -> "InsertQueryBuilder":
        """
        Specify table to insert into.

        Args:
            table: Table name

        Returns:
            Self for method chaining
        """
        if not table:
            raise ValueError("Table name cannot be empty")
        self._table = table
        return self

    def columns(self, columns: List[str]) -> "InsertQueryBuilder":
        """
        Specify columns to insert.

        Args:
            columns: List of column names

        Returns:
            Self for method chaining
        """
        if not columns:
            raise ValueError("Columns list cannot be empty")
        self._columns = columns.copy()
        return self

    def values(self, values: List[Any]) -> "InsertQueryBuilder":
        """
        Specify values to insert.

        Args:
            values: List of values

        Returns:
            Self for method chaining
        """
        if not values:
            raise ValueError("Values list cannot be empty")
        self._values = values.copy()
        return self

    def build(self) -> InsertQuery:
        """
        Build the final immutable InsertQuery.

        Returns:
            Immutable InsertQuery instance

        Raises:
            ValueError: If required fields are not set
        """
        if not self._table:
            raise ValueError("Table name is required. Use into() to set it.")
        if not self._columns:
            raise ValueError("Columns are required. Use columns() to set them.")
        if not self._values:
            raise ValueError("Values are required. Use values() to set them.")

        return InsertQuery(
            table=self._table,
            columns=self._columns.copy(),
            values=self._values.copy()
        )


class UpdateQueryBuilder:
    """
    Builder for constructing UPDATE queries with fluent interface.

    Example:
        >>> builder = UpdateQueryBuilder()
        >>> query = (builder
        ...     .table("users")
        ...     .set("name", "Jane Doe")
        ...     .set("age", 31)
        ...     .where("id = 1")
        ...     .build())
    """

    def __init__(self):
        """Initialize a new UpdateQueryBuilder."""
        self._table: str = ""
        self._updates: Dict[str, Any] = {}
        self._where: Optional[str] = None

    def table(self, table: str) -> "UpdateQueryBuilder":
        """
        Specify table to update.

        Args:
            table: Table name

        Returns:
            Self for method chaining
        """
        if not table:
            raise ValueError("Table name cannot be empty")
        self._table = table
        return self

    def set(self, column: str, value: Any) -> "UpdateQueryBuilder":
        """
        Set a column to a value.

        Args:
            column: Column name
            value: Value to set

        Returns:
            Self for method chaining
        """
        if not column:
            raise ValueError("Column name cannot be empty")
        self._updates[column] = value
        return self

    def set_multiple(self, updates: Dict[str, Any]) -> "UpdateQueryBuilder":
        """
        Set multiple columns at once.

        Args:
            updates: Dictionary of column-value pairs

        Returns:
            Self for method chaining
        """
        self._updates.update(updates)
        return self

    def where(self, condition: str) -> "UpdateQueryBuilder":
        """
        Set WHERE clause condition.

        Args:
            condition: WHERE condition

        Returns:
            Self for method chaining
        """
        self._where = condition
        return self

    def build(self) -> UpdateQuery:
        """
        Build the final immutable UpdateQuery.

        Returns:
            Immutable UpdateQuery instance

        Raises:
            ValueError: If required fields are not set
        """
        if not self._table:
            raise ValueError("Table name is required. Use table() to set it.")
        if not self._updates:
            raise ValueError("Updates are required. Use set() to add them.")

        return UpdateQuery(
            table=self._table,
            updates=self._updates.copy(),
            where=self._where
        )


# ============================================================================
# Director (Optional - for common query patterns)
# ============================================================================


class QueryDirector:
    """
    Director that constructs common query patterns using builders.

    The director encapsulates commonly-used query construction sequences,
    providing a higher-level interface for typical scenarios.
    """

    @staticmethod
    def build_paginated_user_list(page: int = 1, page_size: int = 10) -> SelectQuery:
        """
        Build a paginated user list query.

        Args:
            page: Page number (1-indexed)
            page_size: Number of items per page

        Returns:
            SelectQuery for paginated users
        """
        offset = (page - 1) * page_size
        return (SelectQueryBuilder()
                .select(["id", "name", "email", "created_at"])
                .from_table("users")
                .where("active = TRUE")
                .order_by(["created_at DESC"])
                .limit(page_size)
                .offset(offset)
                .build())

    @staticmethod
    def build_user_orders_report(user_id: int) -> SelectQuery:
        """
        Build a query for user orders with totals.

        Args:
            user_id: ID of the user

        Returns:
            SelectQuery joining users and orders
        """
        return (SelectQueryBuilder()
                .select(["users.name", "COUNT(orders.id) as order_count",
                        "SUM(orders.total) as total_spent"])
                .from_table("users")
                .join("INNER JOIN orders ON users.id = orders.user_id")
                .where(f"users.id = {user_id}")
                .group_by(["users.id", "users.name"])
                .build())

    @staticmethod
    def build_top_customers(limit: int = 10) -> SelectQuery:
        """
        Build a query for top customers by spending.

        Args:
            limit: Number of top customers to return

        Returns:
            SelectQuery for top customers
        """
        return (SelectQueryBuilder()
                .select(["users.id", "users.name", "SUM(orders.total) as total_spent"])
                .from_table("users")
                .join("INNER JOIN orders ON users.id = orders.user_id")
                .group_by(["users.id", "users.name"])
                .having("SUM(orders.total) > 1000")
                .order_by(["total_spent DESC"])
                .limit(limit)
                .build())


# ============================================================================
# Demonstration Functions
# ============================================================================


def demonstrate_basic_select():
    """Demonstrate basic SELECT query building."""
    print("=== Basic SELECT Query ===")

    query = (SelectQueryBuilder()
             .select(["id", "name", "email"])
             .from_table("users")
             .where("age > 18")
             .order_by(["name ASC"])
             .limit(10)
             .build())

    print(query.to_sql())
    print()


def demonstrate_complex_select():
    """Demonstrate complex SELECT with JOIN and GROUP BY."""
    print("=== Complex SELECT with JOIN and GROUP BY ===")

    query = (SelectQueryBuilder()
             .select(["users.name", "COUNT(orders.id) as order_count"])
             .from_table("users")
             .join("LEFT JOIN orders ON users.id = orders.user_id")
             .group_by(["users.id", "users.name"])
             .having("COUNT(orders.id) > 5")
             .order_by(["order_count DESC"])
             .limit(20)
             .build())

    print(query.to_sql())
    print()


def demonstrate_insert():
    """Demonstrate INSERT query building."""
    print("=== INSERT Query ===")

    query = (InsertQueryBuilder()
             .into("users")
             .columns(["name", "email", "age", "active"])
             .values(["John Doe", "john@example.com", 30, True])
             .build())

    print(query.to_sql())
    print()


def demonstrate_update():
    """Demonstrate UPDATE query building."""
    print("=== UPDATE Query ===")

    query = (UpdateQueryBuilder()
             .table("users")
             .set("name", "Jane Doe")
             .set("age", 31)
             .set("last_updated", "NOW()")
             .where("id = 1")
             .build())

    print(query.to_sql())
    print()


def demonstrate_update_multiple():
    """Demonstrate UPDATE with multiple values."""
    print("=== UPDATE with Multiple Values ===")

    updates = {
        "status": "active",
        "verified": True,
        "last_login": "2024-01-15"
    }

    query = (UpdateQueryBuilder()
             .table("users")
             .set_multiple(updates)
             .where("email = 'john@example.com'")
             .build())

    print(query.to_sql())
    print()


def demonstrate_director():
    """Demonstrate using the Director for common patterns."""
    print("=== Using Director for Common Patterns ===")

    print("--- Paginated User List (Page 2) ---")
    query = QueryDirector.build_paginated_user_list(page=2, page_size=20)
    print(query.to_sql())
    print()

    print("--- User Orders Report ---")
    query = QueryDirector.build_user_orders_report(user_id=42)
    print(query.to_sql())
    print()

    print("--- Top 5 Customers ---")
    query = QueryDirector.build_top_customers(limit=5)
    print(query.to_sql())
    print()


def demonstrate_validation():
    """Demonstrate validation and error handling."""
    print("=== Validation and Error Handling ===")

    # Test missing required field
    print("--- Missing Table Name ---")
    try:
        query = SelectQueryBuilder().select(["*"]).build()
    except ValueError as e:
        print(f"Error: {e}")
    print()

    # Test invalid limit
    print("--- Invalid Limit ---")
    try:
        query = (SelectQueryBuilder()
                .from_table("users")
                .limit(-5)
                .build())
    except ValueError as e:
        print(f"Error: {e}")
    print()

    # Test column-value mismatch in INSERT
    print("--- Column-Value Mismatch ---")
    try:
        query = (InsertQueryBuilder()
                .into("users")
                .columns(["name", "email"])
                .values(["John Doe"])  # Missing email value
                .build())
        print(query.to_sql())
    except ValueError as e:
        print(f"Error: {e}")
    print()


def demonstrate_immutability():
    """Demonstrate that built queries are immutable."""
    print("=== Query Immutability ===")

    query = (SelectQueryBuilder()
             .select(["name"])
             .from_table("users")
             .build())

    print("Original query:", query.to_sql())

    # Try to modify (this would raise an error with frozen dataclass)
    print("Queries are immutable - cannot modify after building")
    try:
        # This will raise FrozenInstanceError
        query.table = "customers"
    except Exception as e:
        print(f"Cannot modify: {type(e).__name__}")
    print()


def demonstrate_builder_reuse():
    """Demonstrate resetting and reusing a builder."""
    print("=== Builder Reuse with Reset ===")

    builder = SelectQueryBuilder()

    # Build first query
    query1 = (builder
              .select(["name"])
              .from_table("users")
              .where("active = TRUE")
              .build())
    print("Query 1:", query1.to_sql())

    # Reset and build second query
    query2 = (builder
              .reset()
              .select(["id", "email"])
              .from_table("customers")
              .where("verified = TRUE")
              .limit(50)
              .build())
    print("Query 2:", query2.to_sql())
    print()


# ============================================================================
# Main Function
# ============================================================================


def main():
    """Run all demonstrations of the Builder Pattern."""
    print("Builder Pattern Example: SQL Query Builder\n")

    demonstrate_basic_select()
    demonstrate_complex_select()
    demonstrate_insert()
    demonstrate_update()
    demonstrate_update_multiple()
    demonstrate_director()
    demonstrate_validation()
    demonstrate_immutability()
    demonstrate_builder_reuse()

    print("All demonstrations completed successfully!")


if __name__ == "__main__":
    main()
