from typing import List
from borrow_record import BorrowRecord
from library_book import Librarybook

class Member:
    def __init__(self, member_id: str, name: str, email: str, phone: str):
        self.member_id = member_id
        self.name = name
        self.email = email
        self.phone = phone
        self.borrowed_books: List[Librarybook] = []
        self.borrow_history: List[BorrowRecord] = []
        self.waiting_for: List[str] = []

    def display_info(self) -> str:
        info = f"ID: {self.member_id}\nName: {self.name}\nEmail: {self.email}\nPhone: {self.phone}"
        if self.borrowed_books:
            info += "\n\nCurrently Borrowed Books:"
            for book in self.borrowed_books:
                info += f"\n- {book.title} (Due: {book.due_date.strftime('%Y-%m-%d')})"
        if self.waiting_for:
            info += "\n\nWaiting for Books:"
            for book_id in self.waiting_for:
                info += f"\n- {book_id}"
        return info