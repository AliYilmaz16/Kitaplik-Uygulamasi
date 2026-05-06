from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional
from urllib.parse import urljoin

import requests

from app.api.models import Book, BookInput, book_optional_from_json


class ApiError(RuntimeError):
    pass


@dataclass(frozen=True)
class BookApiClient:
    base_url: str
    timeout_s: float = 8.0

    def _url(self, path: str) -> str:
        base = self.base_url.rstrip("/") + "/"
        return urljoin(base, path.lstrip("/"))

    def list_books(self) -> List[Book]:
        url = self._url("/rest/api/book/list")
        try:
            resp = requests.get(url, timeout=self.timeout_s)
        except requests.RequestException as e:
            raise ApiError(f"Backend'e bağlanılamadı: {e}") from e

        if resp.status_code != 200:
            raise ApiError(f"Liste alınamadı (HTTP {resp.status_code}): {resp.text}")

        data = resp.json()
        if not isinstance(data, list):
            raise ApiError("Beklenmeyen cevap formatı (liste değil).")

        return [Book.from_json(item) for item in data]

    def find_book(
        self,
        *,
        book_id: Optional[int] = None,
        kitap_adi: Optional[str] = None,
        yazar: Optional[str] = None,
    ) -> Optional[Book]:
        url = self._url("/rest/api/book/find")
        params = {}
        if book_id is not None:
            params["id"] = book_id
        if kitap_adi:
            params["kitapAdi"] = kitap_adi
        if yazar:
            params["yazar"] = yazar

        try:
            resp = requests.get(url, params=params, timeout=self.timeout_s)
        except requests.RequestException as e:
            raise ApiError(f"Backend'e bağlanılamadı: {e}") from e

        if resp.status_code != 200:
            raise ApiError(f"Arama başarısız (HTTP {resp.status_code}): {resp.text}")

        data = resp.json()
        if data is None:
            return None
        if not isinstance(data, dict):
            raise ApiError("Beklenmeyen cevap formatı (object değil).")

        return book_optional_from_json(data)

    def create_book(self, book_in: BookInput) -> Book:
        url = self._url("/rest/api/book/save")
        try:
            resp = requests.post(url, json=book_in.to_json(), timeout=self.timeout_s)
        except requests.RequestException as e:
            raise ApiError(f"Backend'e bağlanılamadı: {e}") from e

        if resp.status_code != 200:
            raise ApiError(f"Kayıt başarısız (HTTP {resp.status_code}): {resp.text}")

        book = book_optional_from_json(resp.json())
        if book is None:
            raise ApiError("Kayıt başarısız: backend geçersiz/boş kitap döndürdü.")
        return book

    def update_book(self, book_id: int, book_in: BookInput) -> Optional[Book]:
        url = self._url(f"/rest/api/book/update/{book_id}")
        try:
            resp = requests.put(url, json=book_in.to_json(), timeout=self.timeout_s)
        except requests.RequestException as e:
            raise ApiError(f"Backend'e bağlanılamadı: {e}") from e

        if resp.status_code != 200:
            raise ApiError(f"Güncelleme başarısız (HTTP {resp.status_code}): {resp.text}")

        return book_optional_from_json(resp.json())

    def delete_book(self, book_id: int) -> bool:
        url = self._url(f"/rest/api/book/delete/{book_id}")
        try:
            resp = requests.delete(url, timeout=self.timeout_s)
        except requests.RequestException as e:
            raise ApiError(f"Backend'e bağlanılamadı: {e}") from e

        if resp.status_code != 200:
            raise ApiError(f"Silme başarısız (HTTP {resp.status_code}): {resp.text}")

        data = resp.json()
        return bool(data)

