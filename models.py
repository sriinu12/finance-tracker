from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class Transaction:
    """Single financial transaction record."""

    date: str
    amount: float
    category: str
    description: str

    def __post_init__(self) -> None:
        self.date = self.date.strip()
        self.category = self.category.strip()
        self.description = self.description.strip()

        if not self.date:
            raise ValueError("date is required")
        if not self.category:
            raise ValueError("category is required")
        if not self.description:
            raise ValueError("description is required")

        self.amount = float(self.amount)

    def to_dict(self) -> dict[str, Any]:
        """Return a dictionary representation of the transaction."""
        return {
            "date": self.date,
            "amount": self.amount,
            "category": self.category,
            "description": self.description,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Transaction":
        """Create a Transaction from a dictionary payload."""
        return cls(
            date=str(data.get("date", "")),
            amount=float(data.get("amount", 0.0)),
            category=str(data.get("category", "")),
            description=str(data.get("description", "")),
        )
