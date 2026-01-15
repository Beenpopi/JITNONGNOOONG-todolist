from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Any, Dict
import uuid
from datetime import datetime


class Priority(Enum):
    HIGH = "HIGH"
    MID = "MID"
    LOW = "LOW"


class Status(Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"


@dataclass
class User:
    username: str = ""
    password: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "User":
        return User(
            username=data.get("username", ""),
            password=data.get("password", ""),
        )


@dataclass
class TodoItem:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    title: str = ""
    details: str = ""
    priority: Priority = Priority.MID
    status: Status = Status.PENDING
    owner: str = ""
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["priority"] = self.priority.value
        d["status"] = self.status.value
        return d

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "TodoItem":
        return TodoItem(
            id=data.get("id", str(uuid.uuid4())),
            title=data.get("title", ""),
            details=data.get("details", ""),
            priority=Priority(data.get("priority", "MID")),
            status=Status(data.get("status", "PENDING")),
            owner=data.get("owner", ""),
            created_at=data.get("created_at", datetime.utcnow().isoformat()),
            updated_at=data.get("updated_at", datetime.utcnow().isoformat()),
        )
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    title: str = ""
    details: str = ""
    priority: Priority = Priority.MID
    status: Status = Status.PENDING
    owner: str = ""
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["priority"] = self.priority.value
        d["status"] = self.status.value
        return d

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "TodoItem":
        return TodoItem(
            id=data.get("id", str(uuid.uuid4())),
            title=data.get("title", ""),
            details=data.get("details", ""),
            priority=Priority(data.get("priority", "MID")),
            status=Status(data.get("status", "PENDING")),
            owner=data.get("owner", ""),
            created_at=data.get("created_at", datetime.utcnow().isoformat()),
            updated_at=data.get("updated_at", datetime.utcnow().isoformat()),
        )
