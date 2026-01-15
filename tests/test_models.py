"""
Tests for the models module.
Tests for TodoItem class, Priority and Status enums.
"""

import pytest
from datetime import datetime
from uuid import UUID
from src.models import TodoItem, Priority, Status


class TestPriorityEnum:
    """Test cases for Priority enum."""

    def test_priority_high_value(self):
        """Test that Priority.HIGH has correct value."""
        assert Priority.HIGH.value == "HIGH"

    def test_priority_mid_value(self):
        """Test that Priority.MID has correct value."""
        assert Priority.MID.value == "MID"

    def test_priority_low_value(self):
        """Test that Priority.LOW has correct value."""
        assert Priority.LOW.value == "LOW"

    def test_priority_enum_members(self):
        """Test that Priority enum has exactly 3 members."""
        assert len(Priority) == 3

    def test_priority_from_string(self):
        """Test creating Priority from string value."""
        assert Priority("HIGH") == Priority.HIGH
        assert Priority("MID") == Priority.MID
        assert Priority("LOW") == Priority.LOW

    def test_priority_invalid_value(self):
        """Test that invalid priority raises ValueError."""
        with pytest.raises(ValueError):
            Priority("INVALID")


class TestStatusEnum:
    """Test cases for Status enum."""

    def test_status_pending_value(self):
        """Test that Status.PENDING has correct value."""
        assert Status.PENDING.value == "PENDING"

    def test_status_completed_value(self):
        """Test that Status.COMPLETED has correct value."""
        assert Status.COMPLETED.value == "COMPLETED"

    def test_status_enum_members(self):
        """Test that Status enum has exactly 2 members."""
        assert len(Status) == 2

    def test_status_from_string(self):
        """Test creating Status from string value."""
        assert Status("PENDING") == Status.PENDING
        assert Status("COMPLETED") == Status.COMPLETED

    def test_status_invalid_value(self):
        """Test that invalid status raises ValueError."""
        with pytest.raises(ValueError):
            Status("INVALID")


class TestTodoItemDefaults:
    """Test cases for TodoItem default values."""

    def test_todo_item_default_creation(self):
        """Test that TodoItem can be created with default values."""
        todo = TodoItem()
        assert todo.title == ""
        assert todo.details == ""
        assert todo.priority == Priority.MID
        assert todo.status == Status.PENDING
        assert todo.owner == ""

    def test_todo_item_default_id_is_uuid(self):
        """Test that default id is a valid UUID string."""
        todo = TodoItem()
        # Should be able to parse as UUID
        UUID(todo.id)
        assert len(todo.id) == 36  # Standard UUID string length

    def test_todo_item_default_timestamps_are_iso_format(self):
        """Test that default timestamps are in ISO 8601 format."""
        todo = TodoItem()
        # Should be able to parse as ISO format
        datetime.fromisoformat(todo.created_at)
        datetime.fromisoformat(todo.updated_at)

    def test_todo_item_each_instance_has_unique_id(self):
        """Test that each TodoItem gets a unique ID."""
        todo1 = TodoItem()
        todo2 = TodoItem()
        assert todo1.id != todo2.id


class TestTodoItemConstruction:
    """Test cases for TodoItem constructor with parameters."""

    def test_todo_item_with_all_fields(self):
        """Test creating TodoItem with all fields specified."""
        todo = TodoItem(
            id="test-uuid-123",
            title="Test Task",
            details="Test Details",
            priority=Priority.HIGH,
            status=Status.COMPLETED,
            owner="john_doe",
            created_at="2024-01-01T00:00:00",
            updated_at="2024-01-02T00:00:00",
        )
        assert todo.id == "test-uuid-123"
        assert todo.title == "Test Task"
        assert todo.details == "Test Details"
        assert todo.priority == Priority.HIGH
        assert todo.status == Status.COMPLETED
        assert todo.owner == "john_doe"
        assert todo.created_at == "2024-01-01T00:00:00"
        assert todo.updated_at == "2024-01-02T00:00:00"

    def test_todo_item_with_partial_fields(self):
        """Test creating TodoItem with only some fields specified."""
        todo = TodoItem(title="My Task", owner="jane_doe")
        assert todo.title == "My Task"
        assert todo.owner == "jane_doe"
        assert todo.priority == Priority.MID  # default
        assert todo.status == Status.PENDING  # default


class TestTodoItemToDict:
    """Test cases for TodoItem.to_dict() method."""

    def test_to_dict_converts_enums_to_strings(self):
        """Test that to_dict converts Priority and Status enums to their string values."""
        todo = TodoItem(
            title="Test",
            priority=Priority.HIGH,
            status=Status.COMPLETED,
        )
        result = todo.to_dict()
        assert isinstance(result["priority"], str)
        assert isinstance(result["status"], str)
        assert result["priority"] == "HIGH"
        assert result["status"] == "COMPLETED"

    def test_to_dict_includes_all_fields(self):
        """Test that to_dict includes all TodoItem fields."""
        todo = TodoItem(
            id="test-id",
            title="Test",
            details="Details",
            priority=Priority.MID,
            status=Status.PENDING,
            owner="user",
            created_at="2024-01-01T00:00:00",
            updated_at="2024-01-02T00:00:00",
        )
        result = todo.to_dict()
        assert "id" in result
        assert "title" in result
        assert "details" in result
        assert "priority" in result
        assert "status" in result
        assert "owner" in result
        assert "created_at" in result
        assert "updated_at" in result

    def test_to_dict_returns_dict_type(self):
        """Test that to_dict returns a dictionary."""
        todo = TodoItem(title="Test")
        result = todo.to_dict()
        assert isinstance(result, dict)


class TestTodoItemFromDict:
    """Test cases for TodoItem.from_dict() static method."""

    def test_from_dict_with_all_fields(self):
        """Test creating TodoItem from dictionary with all fields."""
        data = {
            "id": "test-uuid",
            "title": "Test Task",
            "details": "Test Details",
            "priority": "HIGH",
            "status": "COMPLETED",
            "owner": "john_doe",
            "created_at": "2024-01-01T00:00:00",
            "updated_at": "2024-01-02T00:00:00",
        }
        todo = TodoItem.from_dict(data)
        assert todo.id == "test-uuid"
        assert todo.title == "Test Task"
        assert todo.details == "Test Details"
        assert todo.priority == Priority.HIGH
        assert todo.status == Status.COMPLETED
        assert todo.owner == "john_doe"
        assert todo.created_at == "2024-01-01T00:00:00"
        assert todo.updated_at == "2024-01-02T00:00:00"

    def test_from_dict_with_missing_fields(self):
        """Test creating TodoItem from dictionary with missing fields."""
        data = {"title": "Test Task"}
        todo = TodoItem.from_dict(data)
        assert todo.title == "Test Task"
        assert todo.priority == Priority.MID  # default
        assert todo.status == Status.PENDING  # default
        assert todo.details == ""
        assert todo.owner == ""

    def test_from_dict_with_empty_dict(self):
        """Test creating TodoItem from empty dictionary."""
        todo = TodoItem.from_dict({})
        assert todo.title == ""
        assert todo.details == ""
        assert todo.priority == Priority.MID
        assert todo.status == Status.PENDING
        assert todo.owner == ""

    def test_from_dict_converts_string_to_enums(self):
        """Test that from_dict converts string priority and status to enums."""
        data = {
            "priority": "HIGH",
            "status": "COMPLETED",
        }
        todo = TodoItem.from_dict(data)
        assert isinstance(todo.priority, Priority)
        assert isinstance(todo.status, Status)
        assert todo.priority == Priority.HIGH
        assert todo.status == Status.COMPLETED


class TestTodoItemRoundTrip:
    """Test cases for TodoItem serialization/deserialization round trips."""

    def test_to_dict_from_dict_round_trip(self):
        """Test that to_dict and from_dict are inverse operations."""
        original = TodoItem(
            id="test-id",
            title="Test Task",
            details="Test Details",
            priority=Priority.HIGH,
            status=Status.COMPLETED,
            owner="john_doe",
            created_at="2024-01-01T00:00:00",
            updated_at="2024-01-02T00:00:00",
        )
        data = original.to_dict()
        restored = TodoItem.from_dict(data)

        assert restored.id == original.id
        assert restored.title == original.title
        assert restored.details == original.details
        assert restored.priority == original.priority
        assert restored.status == original.status
        assert restored.owner == original.owner
        assert restored.created_at == original.created_at
        assert restored.updated_at == original.updated_at

    def test_multiple_round_trips_preserve_data(self):
        """Test that multiple round trips preserve data integrity."""
        original = TodoItem(
            title="Multi-trip Task",
            priority=Priority.LOW,
            owner="user123",
        )
        # First round trip
        data1 = original.to_dict()
        todo1 = TodoItem.from_dict(data1)
        # Second round trip
        data2 = todo1.to_dict()
        todo2 = TodoItem.from_dict(data2)

        assert todo2.title == original.title
        assert todo2.priority == original.priority
        assert todo2.owner == original.owner
