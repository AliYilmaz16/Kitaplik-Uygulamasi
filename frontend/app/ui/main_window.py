from __future__ import annotations

from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QAbstractItemView,
    QApplication,
    QFormLayout,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QStatusBar,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from app.api.client import ApiError, BookApiClient
from app.api.models import Book, BookInput
from app.state.viewmodel import AppState


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Kutuphane - Desktop (PySide6)")
        self.resize(980, 620)

        self.state = AppState()

        root = QWidget()
        self.setCentralWidget(root)
        root_layout = QVBoxLayout(root)

        top_bar = QWidget()
        top_layout = QHBoxLayout(top_bar)
        top_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.addWidget(top_bar)

        top_layout.addWidget(QLabel("API Base URL:"))
        self.base_url_input = QLineEdit(self.state.base_url)
        self.base_url_input.setPlaceholderText("http://localhost:8080")
        top_layout.addWidget(self.base_url_input, 1)

        self.refresh_btn = QPushButton("Bağlan / Yenile")
        self.refresh_btn.clicked.connect(self.refresh_books)  # type: ignore[arg-type]
        top_layout.addWidget(self.refresh_btn)

        find_bar = QWidget()
        find_layout = QHBoxLayout(find_bar)
        find_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.addWidget(find_bar)

        find_layout.addWidget(QLabel("Bul (id / kitapAdi / yazar):"))
        self.find_id_input = QLineEdit()
        self.find_id_input.setPlaceholderText("id")
        self.find_id_input.setMaximumWidth(110)
        find_layout.addWidget(self.find_id_input)

        self.find_kitap_adi_input = QLineEdit()
        self.find_kitap_adi_input.setPlaceholderText("kitapAdi")
        find_layout.addWidget(self.find_kitap_adi_input, 1)

        self.find_yazar_input = QLineEdit()
        self.find_yazar_input.setPlaceholderText("yazar")
        find_layout.addWidget(self.find_yazar_input, 1)

        self.find_btn = QPushButton("Bul")
        self.find_btn.clicked.connect(self.find_book)  # type: ignore[arg-type]
        find_layout.addWidget(self.find_btn)

        self.show_all_btn = QPushButton("Tümünü Göster")
        self.show_all_btn.clicked.connect(self.refresh_books)  # type: ignore[arg-type]
        find_layout.addWidget(self.show_all_btn)

        content = QWidget()
        content_layout = QGridLayout(content)
        content_layout.setColumnStretch(0, 2)
        content_layout.setColumnStretch(1, 1)
        root_layout.addWidget(content, 1)

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["ID", "Kitap Adı", "Yazar", "Sayfa Sayısı"])
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.itemSelectionChanged.connect(self.on_row_selected)  # type: ignore[arg-type]
        content_layout.addWidget(self.table, 0, 0)

        form_box = QGroupBox("Kitap")
        form_layout = QVBoxLayout(form_box)
        content_layout.addWidget(form_box, 0, 1)

        form = QWidget()
        form_fields = QFormLayout(form)
        form_layout.addWidget(form)

        self.kitap_adi_input = QLineEdit()
        self.yazar_input = QLineEdit()
        self.sayfa_sayisi_input = QLineEdit()

        form_fields.addRow("Kitap Adı", self.kitap_adi_input)
        form_fields.addRow("Yazar", self.yazar_input)
        form_fields.addRow("Sayfa Sayısı", self.sayfa_sayisi_input)

        buttons = QWidget()
        btn_layout = QHBoxLayout(buttons)
        btn_layout.setContentsMargins(0, 0, 0, 0)
        form_layout.addWidget(buttons)

        self.create_btn = QPushButton("Yeni Kaydet")
        self.create_btn.clicked.connect(self.create_book)  # type: ignore[arg-type]
        btn_layout.addWidget(self.create_btn)

        self.update_btn = QPushButton("Seçileni Güncelle")
        self.update_btn.clicked.connect(self.update_book)  # type: ignore[arg-type]
        btn_layout.addWidget(self.update_btn)

        self.delete_btn = QPushButton("Seçileni Sil")
        self.delete_btn.clicked.connect(self.delete_book)  # type: ignore[arg-type]
        btn_layout.addWidget(self.delete_btn)

        self.clear_btn = QPushButton("Formu Temizle")
        self.clear_btn.clicked.connect(self.clear_form)  # type: ignore[arg-type]
        btn_layout.addWidget(self.clear_btn)

        self.status = QStatusBar()
        self.setStatusBar(self.status)
        self.set_status("Hazır.")

    def api(self) -> BookApiClient:
        base_url = self.base_url_input.text().strip() or "http://localhost:8080"
        self.state.base_url = base_url
        return BookApiClient(base_url=base_url)

    def set_status(self, message: str) -> None:
        self.state.status_message = message
        self.status.showMessage(message, 8000)

    def show_error(self, title: str, message: str) -> None:
        QMessageBox.critical(self, title, message)
        self.set_status(message)

    def show_info(self, title: str, message: str) -> None:
        QMessageBox.information(self, title, message)
        self.set_status(message)

    def current_input(self) -> BookInput:
        kitap_adi = self.kitap_adi_input.text().strip()
        yazar = self.yazar_input.text().strip()
        sayfa = self.sayfa_sayisi_input.text().strip()
        return BookInput(yazar=yazar, kitapAdi=kitap_adi, sayfaSayisi=sayfa)

    def validate_input(self, book_in: BookInput) -> Optional[str]:
        if not book_in.kitapAdi:
            return "Kitap adı boş olamaz."
        if not book_in.yazar:
            return "Yazar boş olamaz."
        if not book_in.sayfaSayisi:
            return "Sayfa sayısı boş olamaz."
        return None

    def refresh_books(self) -> None:
        try:
            books = self.api().list_books()
        except ApiError as e:
            self.show_error("Bağlantı Hatası", str(e))
            return
        except Exception as e:
            self.show_error("Hata", f"Beklenmeyen hata: {e}")
            return

        self.state.books = books
        self.populate_table()
        self.set_status(f"{len(books)} kitap yüklendi.")

    def find_book(self) -> None:
        raw_id = self.find_id_input.text().strip()
        kitap_adi = self.find_kitap_adi_input.text().strip()
        yazar = self.find_yazar_input.text().strip()

        book_id: Optional[int] = None
        if raw_id:
            try:
                book_id = int(raw_id)
            except ValueError:
                self.show_error("Doğrulama", "id sayısal olmalı.")
                return

        if book_id is None and not kitap_adi and not yazar:
            self.show_error("Doğrulama", "Aramak için en az bir alan doldurun (id / kitapAdi / yazar).")
            return

        try:
            books = self.api().list_books()
        except ApiError as e:
            self.show_error("Arama Hatası", str(e))
            return
        except Exception as e:
            self.show_error("Hata", f"Beklenmeyen hata: {e}")
            return

        def contains_ci(haystack: str, needle: str) -> bool:
            return needle.casefold() in haystack.casefold()

        filtered = books
        if book_id is not None:
            filtered = [b for b in filtered if b.id == book_id]
        if kitap_adi:
            filtered = [b for b in filtered if contains_ci(b.kitapAdi, kitap_adi)]
        if yazar:
            filtered = [b for b in filtered if contains_ci(b.yazar, yazar)]

        self.state.books = filtered
        self.populate_table()
        if not filtered:
            self.show_error("Bulunamadı", "Kriterlere uygun kitap bulunamadı.")
            return

        self.set_status(f"{len(filtered)} kayıt bulundu.")

    def populate_table(self) -> None:
        self.table.setRowCount(0)
        for b in self.state.books:
            self._append_book_row(b)
        self.table.resizeColumnsToContents()

    def _append_book_row(self, b: Book) -> None:
        row = self.table.rowCount()
        self.table.insertRow(row)

        id_item = QTableWidgetItem(str(b.id))
        id_item.setData(Qt.ItemDataRole.UserRole, b.id)
        self.table.setItem(row, 0, id_item)
        self.table.setItem(row, 1, QTableWidgetItem(b.kitapAdi))
        self.table.setItem(row, 2, QTableWidgetItem(b.yazar))
        self.table.setItem(row, 3, QTableWidgetItem(b.sayfaSayisi))

    def on_row_selected(self) -> None:
        items = self.table.selectedItems()
        if not items:
            self.state.selected_book_id = None
            return
        id_item = self.table.item(self.table.currentRow(), 0)
        if id_item is None:
            self.state.selected_book_id = None
            return
        book_id = id_item.data(Qt.ItemDataRole.UserRole)
        try:
            self.state.selected_book_id = int(book_id)
        except Exception:
            self.state.selected_book_id = None
            return

        book = next((x for x in self.state.books if x.id == self.state.selected_book_id), None)
        if not book:
            return

        self.kitap_adi_input.setText(book.kitapAdi)
        self.yazar_input.setText(book.yazar)
        self.sayfa_sayisi_input.setText(book.sayfaSayisi)

    def clear_form(self) -> None:
        self.state.selected_book_id = None
        self.table.clearSelection()
        self.kitap_adi_input.clear()
        self.yazar_input.clear()
        self.sayfa_sayisi_input.clear()
        self.set_status("Form temizlendi.")

    def create_book(self) -> None:
        book_in = self.current_input()
        err = self.validate_input(book_in)
        if err:
            self.show_error("Doğrulama", err)
            return

        try:
            created = self.api().create_book(book_in)
        except ApiError as e:
            self.show_error("Kayıt Hatası", str(e))
            return
        except Exception as e:
            self.show_error("Hata", f"Beklenmeyen hata: {e}")
            return

        self.show_info("Başarılı", f"Kitap kaydedildi (id={created.id}).")
        self.refresh_books()
        self.clear_form()

    def update_book(self) -> None:
        if self.state.selected_book_id is None:
            self.show_error("Seçim", "Güncellemek için tablodan bir kitap seçin.")
            return

        book_in = self.current_input()
        err = self.validate_input(book_in)
        if err:
            self.show_error("Doğrulama", err)
            return

        try:
            updated = self.api().update_book(self.state.selected_book_id, book_in)
        except ApiError as e:
            self.show_error("Güncelleme Hatası", str(e))
            return
        except Exception as e:
            self.show_error("Hata", f"Beklenmeyen hata: {e}")
            return

        if updated is None:
            self.show_error("Bulunamadı", "Seçili kitap bulunamadı (backend boş/idsiz DTO döndürdü).")
            self.refresh_books()
            return

        self.show_info("Başarılı", f"Kitap güncellendi (id={updated.id}).")
        self.refresh_books()

    def delete_book(self) -> None:
        if self.state.selected_book_id is None:
            self.show_error("Seçim", "Silmek için tablodan bir kitap seçin.")
            return

        book_id = self.state.selected_book_id
        confirm = QMessageBox.question(
            self,
            "Silme Onayı",
            f"Seçili kitabı silmek istiyor musunuz? (id={book_id})",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if confirm != QMessageBox.StandardButton.Yes:
            return

        try:
            ok = self.api().delete_book(book_id)
        except ApiError as e:
            self.show_error("Silme Hatası", str(e))
            return
        except Exception as e:
            self.show_error("Hata", f"Beklenmeyen hata: {e}")
            return

        if not ok:
            self.show_error("Bulunamadı", "Silinecek kitap bulunamadı (backend false döndürdü).")
            self.refresh_books()
            return

        self.show_info("Başarılı", f"Kitap silindi (id={book_id}).")
        self.refresh_books()
        self.clear_form()


def run_app() -> None:
    app = QApplication.instance() or QApplication([])
    win = MainWindow()
    win.show()
    app.exec()

