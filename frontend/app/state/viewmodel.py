from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from app.api.models import Book


@dataclass
class AppState:
    base_url: str = "http://localhost:8080"
    books: List[Book] = None  # type: ignore[assignment]
    selected_book_id: Optional[int] = None
    status_message: str = ""

    def __post_init__(self) -> None:
        if self.books is None:
            self.books = []

