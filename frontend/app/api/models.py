from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class Book:
    id: int
    yazar: str
    kitapAdi: str
    sayfaSayisi: str

    @staticmethod
    def from_json(data: Dict[str, Any]) -> "Book":
        return Book(
            id=int(data.get("id")),
            yazar=str(data.get("yazar") or ""),
            kitapAdi=str(data.get("kitapAdi") or ""),
            sayfaSayisi=str(data.get("sayfaSayisi") or ""),
        )


@dataclass(frozen=True)
class BookInput:
    yazar: str
    kitapAdi: str
    sayfaSayisi: str

    def to_json(self) -> Dict[str, Any]:
        return {
            "yazar": self.yazar,
            "kitapAdi": self.kitapAdi,
            "sayfaSayisi": self.sayfaSayisi,
        }


def book_optional_from_json(data: Optional[Dict[str, Any]]) -> Optional[Book]:
    if not data:
        return None
    if data.get("id") is None:
        return None
    return Book.from_json(data)

