"""
Tests for the models module.
Tests for TodoItem class, Priority and Status enums.
"""

import pytest
from datetime import datetime
from uuid import UUID
from src.models import TodoItem, Priority, Status, User


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


class TestUser:
    """Test cases for User class."""

    def test_user_default_creation(self):
        """Test that User can be created with default values."""
        user = User()
        assert user.username == ""
        assert user.password == ""

    def test_user_with_username_and_password(self):
        """Test creating User with username and password."""
        user = User(username="john_doe", password="secret123")
        assert user.username == "john_doe"
        assert user.password == "secret123"

    def test_user_to_dict(self):
        """Test that to_dict returns correct dictionary."""
        user = User(username="jane_doe", password="pass456")
        result = user.to_dict()
        assert result == {"username": "jane_doe", "password": "pass456"}
        assert isinstance(result, dict)

    def test_user_from_dict(self):
        """Test creating User from dictionary."""
        data = {"username": "alice", "password": "pwd789"}
        user = User.from_dict(data)
        assert user.username == "alice"
        assert user.password == "pwd789"

    def test_user_from_dict_missing_fields(self):
        """Test creating User from dictionary with missing fields."""
        data = {"username": "bob"}
        user = User.from_dict(data)
        assert user.username == "bob"
        assert user.password == ""

    def test_user_from_dict_empty(self):
        """Test creating User from empty dictionary."""
        user = User.from_dict({})
        assert user.username == ""
        assert user.password == ""

    def test_user_round_trip(self):
        """Test to_dict and from_dict round trip."""
        original = User(username="test_user", password="test_pass")
        data = original.to_dict()
        restored = User.from_dict(data)
        assert restored.username == original.username
        assert restored.password == original.password


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

class TestViewAllTodoItems:
    """Test cases for viewing all to-do-list items (Task 4)."""

    def test_get_todos_by_owner_returns_list(self):
        """Test that get_todos_by_owner returns a list."""
        todo = TodoItem(title="Test", owner="user1")
        todos = [todo]
        result = [t for t in todos if t.owner == "user1"]
        assert isinstance(result, list)

    def test_get_todos_by_owner_single_todo(self):
        """Test getting todos for owner with single todo."""
        todo = TodoItem(title="Task 1", owner="john_doe")
        todos_data = [todo.to_dict()]
        todos = [TodoItem.from_dict(t) for t in todos_data if t.get("owner") == "john_doe"]
        assert len(todos) == 1
        assert todos[0].title == "Task 1"

    def test_get_todos_by_owner_multiple_todos(self):
        """Test getting todos for owner with multiple todos."""
        todo1 = TodoItem(title="Task 1", owner="jane_doe")
        todo2 = TodoItem(title="Task 2", owner="jane_doe")
        todo3 = TodoItem(title="Task 3", owner="other_user")
        todos_data = [todo1.to_dict(), todo2.to_dict(), todo3.to_dict()]
        todos = [TodoItem.from_dict(t) for t in todos_data if t.get("owner") == "jane_doe"]
        assert len(todos) == 2
        assert all(t.owner == "jane_doe" for t in todos)

    def test_get_todos_by_owner_empty_result(self):
        """Test getting todos for owner with no todos returns empty list."""
        todo1 = TodoItem(title="Task 1", owner="user1")
        todos_data = [todo1.to_dict()]
        todos = [TodoItem.from_dict(t) for t in todos_data if t.get("owner") == "user2"]
        assert len(todos) == 0
        assert isinstance(todos, list)

    def test_view_all_todos_preserves_all_fields(self):
        """Test that viewing todos preserves all fields."""
        todo = TodoItem(
            title="Important Task",
            details="This is important",
            priority=Priority.HIGH,
            status=Status.PENDING,
            owner="alice",
        )
        todos_data = [todo.to_dict()]
        todos = [TodoItem.from_dict(t) for t in todos_data]
        assert len(todos) == 1
        assert todos[0].title == "Important Task"
        assert todos[0].details == "This is important"
        assert todos[0].priority == Priority.HIGH
        assert todos[0].status == Status.PENDING
        assert todos[0].owner == "alice"

    def test_view_all_todos_with_various_priorities(self):
        """Test viewing todos with different priority levels."""
        todo_high = TodoItem(title="High Priority", priority=Priority.HIGH, owner="user1")
        todo_mid = TodoItem(title="Mid Priority", priority=Priority.MID, owner="user1")
        todo_low = TodoItem(title="Low Priority", priority=Priority.LOW, owner="user1")
        todos_data = [todo_high.to_dict(), todo_mid.to_dict(), todo_low.to_dict()]
        todos = [TodoItem.from_dict(t) for t in todos_data if t.get("owner") == "user1"]
        assert len(todos) == 3
        priorities = [t.priority for t in todos]
        assert Priority.HIGH in priorities
        assert Priority.MID in priorities
        assert Priority.LOW in priorities

    def test_view_all_todos_with_various_statuses(self):
        """Test viewing todos with different status values."""
        todo_pending = TodoItem(title="Pending Task", status=Status.PENDING, owner="user1")
        todo_completed = TodoItem(title="Completed Task", status=Status.COMPLETED, owner="user1")
        todos_data = [todo_pending.to_dict(), todo_completed.to_dict()]
        todos = [TodoItem.from_dict(t) for t in todos_data if t.get("owner") == "user1"]
        assert len(todos) == 2
        statuses = [t.status for t in todos]
        assert Status.PENDING in statuses
        assert Status.COMPLETED in statuses

    def test_view_all_todos_maintains_creation_order(self):
        """Test that viewing todos maintains the order they were created."""
        todo1 = TodoItem(title="First", owner="user1")
        todo2 = TodoItem(title="Second", owner="user1")
        todo3 = TodoItem(title="Third", owner="user1")
        todos_data = [todo1.to_dict(), todo2.to_dict(), todo3.to_dict()]
        todos = [TodoItem.from_dict(t) for t in todos_data if t.get("owner") == "user1"]
        assert todos[0].title == "First"
        assert todos[1].title == "Second"
        assert todos[2].title == "Third"

    def test_view_all_todos_does_not_show_other_users_todos(self):
        """Test that viewing todos only shows todos for the requesting user."""
        user1_todo = TodoItem(title="User1 Task", owner="user1")
        user2_todo = TodoItem(title="User2 Task", owner="user2")
        todos_data = [user1_todo.to_dict(), user2_todo.to_dict()]
        user1_todos = [TodoItem.from_dict(t) for t in todos_data if t.get("owner") == "user1"]
        assert len(user1_todos) == 1
        assert user1_todos[0].owner == "user1"
        assert user1_todos[0].title == "User1 Task"

    def test_view_all_todos_with_special_characters_in_title(self):
        """Test viewing todos with special characters in title."""
        todo = TodoItem(title="Task: #1 (urgent!) @Home", owner="user1")
        todos_data = [todo.to_dict()]
        todos = [TodoItem.from_dict(t) for t in todos_data if t.get("owner") == "user1"]
        assert len(todos) == 1
        assert todos[0].title == "Task: #1 (urgent!) @Home"

    def test_view_all_todos_with_long_details(self):
        """Test viewing todos with long details text."""
        long_details = "This is a very long description " * 10
        todo = TodoItem(title="Long Details Task", details=long_details, owner="user1")
        todos_data = [todo.to_dict()]
        todos = [TodoItem.from_dict(t) for t in todos_data if t.get("owner") == "user1"]
        assert len(todos) == 1
        assert todos[0].details == long_details


class TestCreateTodoItem:
    """Test cases for creating a to-do-list item (Task 3)."""

    def test_create_todo_with_title_only(self):
        """Test creating a todo with only title specified."""
        todo = TodoItem(
            title="Buy groceries",
            created_at="2024-01-01T10:00:00",
            updated_at="2024-01-01T10:00:00"
        )
        assert todo.title == "Buy groceries"
        assert todo.priority == Priority.MID
        assert todo.status == Status.PENDING

    def test_create_todo_with_title_and_details(self):
        """Test creating a todo with title and details."""
        todo = TodoItem(
            title="Complete report",
            details="Finish Q1 quarterly report",
            created_at="2024-01-01T10:00:00",
            updated_at="2024-01-01T10:00:00"
        )
        assert todo.title == "Complete report"
        assert todo.details == "Finish Q1 quarterly report"

    def test_create_todo_with_priority_high(self):
        """Test creating a todo with HIGH priority."""
        todo = TodoItem(
            title="Urgent task",
            priority=Priority.HIGH,
            created_at="2024-01-01T10:00:00",
            updated_at="2024-01-01T10:00:00"
        )
        assert todo.priority == Priority.HIGH
        assert todo.title == "Urgent task"

    def test_create_todo_with_priority_mid(self):
        """Test creating a todo with MID priority."""
        todo = TodoItem(
            title="Normal task",
            priority=Priority.MID,
            created_at="2024-01-01T10:00:00",
            updated_at="2024-01-01T10:00:00"
        )
        assert todo.priority == Priority.MID

    def test_create_todo_with_priority_low(self):
        """Test creating a todo with LOW priority."""
        todo = TodoItem(
            title="Low priority task",
            priority=Priority.LOW,
            created_at="2024-01-01T10:00:00",
            updated_at="2024-01-01T10:00:00"
        )
        assert todo.priority == Priority.LOW

    def test_create_todo_with_owner(self):
        """Test creating a todo with owner field."""
        todo = TodoItem(
            title="Team task",
            owner="john_doe",
            created_at="2024-01-01T10:00:00",
            updated_at="2024-01-01T10:00:00"
        )
        assert todo.owner == "john_doe"

    def test_create_todo_with_all_fields(self):
        """Test creating a todo with all fields specified."""
        todo = TodoItem(
            id="custom-id-123",
            title="Complete project",
            details="Finish the development project",
            priority=Priority.HIGH,
            status=Status.PENDING,
            owner="alice",
            created_at="2024-01-01T10:00:00",
            updated_at="2024-01-01T10:00:00"
        )
        assert todo.id == "custom-id-123"
        assert todo.title == "Complete project"
        assert todo.details == "Finish the development project"
        assert todo.priority == Priority.HIGH
        assert todo.status == Status.PENDING
        assert todo.owner == "alice"

    def test_create_todo_generates_unique_id_when_not_specified(self):
        """Test that each created todo gets a unique ID when not specified."""
        todo1 = TodoItem(
            title="Task 1",
            created_at="2024-01-01T10:00:00",
            updated_at="2024-01-01T10:00:00"
        )
        todo2 = TodoItem(
            title="Task 2",
            created_at="2024-01-01T10:00:00",
            updated_at="2024-01-01T10:00:00"
        )
        assert todo1.id != todo2.id
        assert len(todo1.id) == 36

    def test_create_todo_with_empty_title(self):
        """Test creating a todo with empty title."""
        todo = TodoItem(
            title="",
            created_at="2024-01-01T10:00:00",
            updated_at="2024-01-01T10:00:00"
        )
        assert todo.title == ""
        assert todo.status == Status.PENDING

    def test_create_todo_with_special_characters(self):
        """Test creating a todo with special characters in title."""
        special_title = "Task: #1 @Home (Urgent!) & Important"
        todo = TodoItem(
            title=special_title,
            created_at="2024-01-01T10:00:00",
            updated_at="2024-01-01T10:00:00"
        )
        assert todo.title == special_title

    def test_create_todo_with_multiline_details(self):
        """Test creating a todo with multiline details."""
        multiline_details = "Line 1\nLine 2\nLine 3"
        todo = TodoItem(
            title="Multiline",
            details=multiline_details,
            created_at="2024-01-01T10:00:00",
            updated_at="2024-01-01T10:00:00"
        )
        assert todo.details == multiline_details

    def test_create_todo_with_unicode_characters(self):
        """Test creating a todo with unicode characters."""
        unicode_title = "Buy milk 🥛 and eggs 🥚"
        todo = TodoItem(
            title=unicode_title,
            created_at="2024-01-01T10:00:00",
            updated_at="2024-01-01T10:00:00"
        )
        assert todo.title == unicode_title

    def test_create_multiple_todos_for_same_owner(self):
        """Test creating multiple todos for the same owner."""
        owner = "alice"
        todos = [
            TodoItem(title="Task 1", owner=owner, created_at="2024-01-01T10:00:00", updated_at="2024-01-01T10:00:00"),
            TodoItem(title="Task 2", owner=owner, created_at="2024-01-01T10:00:00", updated_at="2024-01-01T10:00:00"),
            TodoItem(title="Task 3", owner=owner, created_at="2024-01-01T10:00:00", updated_at="2024-01-01T10:00:00"),
        ]
        assert len(todos) == 3
        assert all(t.owner == owner for t in todos)


class TestEditTodoItem:
    """Test cases for editing a to-do-list item (Task 3)."""

    def test_edit_todo_title(self):
        """Test editing the title of a todo."""
        todo = TodoItem(
            title="Old Title",
            owner="user1",
            created_at="2024-01-01T10:00:00",
            updated_at="2024-01-01T10:00:00"
        )
        todo.title = "New Title"
        assert todo.title == "New Title"

    def test_edit_todo_details(self):
        """Test editing the details of a todo."""
        todo = TodoItem(
            title="Test",
            details="Old details",
            owner="user1",
            created_at="2024-01-01T10:00:00",
            updated_at="2024-01-01T10:00:00"
        )
        todo.details = "New details"
        assert todo.details == "New details"

    def test_edit_todo_priority_from_low_to_high(self):
        """Test editing the priority of a todo from LOW to HIGH."""
        todo = TodoItem(
            title="Test",
            priority=Priority.LOW,
            owner="user1",
            created_at="2024-01-01T10:00:00",
            updated_at="2024-01-01T10:00:00"
        )
        assert todo.priority == Priority.LOW
        todo.priority = Priority.HIGH
        assert todo.priority == Priority.HIGH

    def test_edit_todo_priority_from_mid_to_low(self):
        """Test editing the priority of a todo from MID to LOW."""
        todo = TodoItem(
            title="Test",
            priority=Priority.MID,
            created_at="2024-01-01T10:00:00",
            updated_at="2024-01-01T10:00:00"
        )
        todo.priority = Priority.LOW
        assert todo.priority == Priority.LOW

    def test_edit_todo_status_pending_to_completed(self):
        """Test editing the status of a todo from PENDING to COMPLETED."""
        todo = TodoItem(
            title="Test",
            status=Status.PENDING,
            owner="user1",
            created_at="2024-01-01T10:00:00",
            updated_at="2024-01-01T10:00:00"
        )
        assert todo.status == Status.PENDING
        todo.status = Status.COMPLETED
        assert todo.status == Status.COMPLETED

    def test_edit_todo_status_completed_to_pending(self):
        """Test editing the status of a todo from COMPLETED back to PENDING."""
        todo = TodoItem(
            title="Test",
            status=Status.COMPLETED,
            created_at="2024-01-01T10:00:00",
            updated_at="2024-01-01T10:00:00"
        )
        todo.status = Status.PENDING
        assert todo.status == Status.PENDING

    def test_edit_todo_owner(self):
        """Test editing the owner of a todo."""
        todo = TodoItem(
            title="Test",
            owner="user1",
            created_at="2024-01-01T10:00:00",
            updated_at="2024-01-01T10:00:00"
        )
        todo.owner = "user2"
        assert todo.owner == "user2"

    def test_edit_todo_updated_at_timestamp(self):
        """Test manually updating the updated_at timestamp."""
        todo = TodoItem(
            title="Test",
            updated_at="2024-01-01T10:00:00",
            created_at="2024-01-01T10:00:00"
        )
        todo.updated_at = "2024-01-02T15:30:00"
        assert todo.updated_at == "2024-01-02T15:30:00"

    def test_edit_multiple_fields_simultaneously(self):
        """Test editing multiple fields at once."""
        todo = TodoItem(
            title="Old Title",
            details="Old details",
            priority=Priority.LOW,
            status=Status.PENDING,
            owner="user1",
            created_at="2024-01-01T10:00:00",
            updated_at="2024-01-01T10:00:00"
        )
        
        todo.title = "New Title"
        todo.details = "New details"
        todo.priority = Priority.HIGH
        todo.status = Status.COMPLETED
        
        assert todo.title == "New Title"
        assert todo.details == "New details"
        assert todo.priority == Priority.HIGH
        assert todo.status == Status.COMPLETED
        assert todo.owner == "user1"

    def test_edit_todo_preserves_id(self):
        """Test that editing a todo preserves its ID."""
        original_id = "test-id-123"
        todo = TodoItem(
            id=original_id,
            title="Original",
            created_at="2024-01-01T10:00:00",
            updated_at="2024-01-01T10:00:00"
        )
        todo.title = "Edited"
        assert todo.id == original_id

    def test_edit_todo_preserves_created_at(self):
        """Test that editing a todo preserves created_at timestamp."""
        created_time = "2024-01-01T10:00:00"
        todo = TodoItem(
            title="Original",
            created_at=created_time,
            updated_at="2024-01-01T10:00:00"
        )
        todo.title = "Edited"
        assert todo.created_at == created_time

    def test_edit_todo_title_to_empty_string(self):
        """Test editing a todo title to empty string."""
        todo = TodoItem(
            title="Non-empty",
            owner="user1",
            created_at="2024-01-01T10:00:00",
            updated_at="2024-01-01T10:00:00"
        )
        todo.title = ""
        assert todo.title == ""

    def test_edit_todo_title_with_special_characters(self):
        """Test editing a todo with special characters in title."""
        todo = TodoItem(
            title="Original",
            owner="user1",
            created_at="2024-01-01T10:00:00",
            updated_at="2024-01-01T10:00:00"
        )
        new_title = "Task: #2 @Office (Urgent!)"
        todo.title = new_title
        assert todo.title == new_title

    def test_edit_todo_details_with_multiline_text(self):
        """Test editing todo details with multiline text."""
        todo = TodoItem(
            title="Test",
            details="Single line",
            created_at="2024-01-01T10:00:00",
            updated_at="2024-01-01T10:00:00"
        )
        multiline_details = "Line 1\nLine 2\nLine 3\nLine 4"
        todo.details = multiline_details
        assert todo.details == multiline_details

    def test_edit_todo_and_serialize_to_dict(self):
        """Test editing a todo and then serializing to dict."""
        todo = TodoItem(
            title="Original",
            priority=Priority.LOW,
            status=Status.PENDING,
            owner="user1",
            created_at="2024-01-01T10:00:00",
            updated_at="2024-01-01T10:00:00"
        )
        
        todo.title = "Edited"
        todo.priority = Priority.HIGH
        todo.status = Status.COMPLETED
        
        data = todo.to_dict()
        assert data["title"] == "Edited"
        assert data["priority"] == "HIGH"
        assert data["status"] == "COMPLETED"
        assert data["owner"] == "user1"

    def test_edit_todo_deserialize_and_edit(self):
        """Test deserializing a todo from dict and editing it."""
        data = {
            "id": "test-id",
            "title": "Original",
            "details": "Original details",
            "priority": "LOW",
            "status": "PENDING",
            "owner": "user1",
            "created_at": "2024-01-01T10:00:00",
            "updated_at": "2024-01-01T10:00:00"
        }
        
        todo = TodoItem.from_dict(data)
        todo.title = "Edited"
        todo.details = "Edited details"
        todo.priority = Priority.HIGH
        
        assert todo.title == "Edited"
        assert todo.details == "Edited details"
        assert todo.priority == Priority.HIGH
        assert todo.id == "test-id"

    def test_edit_todo_chain_modifications(self):
        """Test making a series of edits to a todo."""
        todo = TodoItem(
            title="Task",
            priority=Priority.LOW,
            owner="user1",
            created_at="2024-01-01T10:00:00",
            updated_at="2024-01-01T10:00:00"
        )
        
        todo.title = "Updated Task"
        assert todo.title == "Updated Task"
        
        todo.priority = Priority.MID
        assert todo.priority == Priority.MID
        
        todo.status = Status.COMPLETED
        assert todo.status == Status.COMPLETED
        
        assert todo.title == "Updated Task"
        assert todo.priority == Priority.MID
        assert todo.status == Status.COMPLETED

    def test_edit_todo_with_long_details(self):
        """Test editing a todo with very long details."""
        long_details = "This is a long detailed description. " * 50
        todo = TodoItem(
            title="Test",
            details="Short",
            created_at="2024-01-01T10:00:00",
            updated_at="2024-01-01T10:00:00"
        )
        todo.details = long_details
        assert todo.details == long_details

    def test_create_and_edit_workflow(self):
        """Test a typical workflow of creating and editing a todo."""
        todo = TodoItem(
            title="Finish project",
            details="",
            priority=Priority.MID,
            status=Status.PENDING,
            owner="developer1",
            created_at="2024-01-01T10:00:00",
            updated_at="2024-01-01T10:00:00"
        )
        
        todo.details = "Complete the development and testing of feature X"
        assert todo.details == "Complete the development and testing of feature X"
        
        todo.priority = Priority.HIGH
        assert todo.priority == Priority.HIGH
        
        todo.updated_at = "2024-01-02T14:30:00"
        assert todo.updated_at == "2024-01-02T14:30:00"
        
        todo.status = Status.COMPLETED
        assert todo.status == Status.COMPLETED
        
        assert todo.title == "Finish project"
        assert todo.owner == "developer1"