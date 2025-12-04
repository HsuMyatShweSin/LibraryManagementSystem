from datetime import datetime
from typing import List, Optional
from borrow_record import BorrowRecord
from genre import Genre
from rating import Rating

class Librarybook:
    def __init__(self, book_id: str, title: str, author: str, genre: Genre, rating: Rating, description: str):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.genre = genre
        self.rating = rating
        self.description = description
        self.is_borrowed = False
        self.current_borrower: Optional[str] = None
        self.borrow_date: Optional[datetime] = None
        self.due_date: Optional[datetime] = None
        self.borrow_history: List[BorrowRecord] = []
        self.waiting_list: List[str] = []
    
    def display_info(self) -> str:
        status = "Borrowed" if self.is_borrowed else "Available"
        info = f"ID: {self.book_id}\nTitle: {self.title}\nAuthor: {self.author}\nGenre: {self.genre.value}\n"
        info += f"Rating: {self.rating.value}\nStatus: {status}\nDescription: {self.description}"

        if self.is_borrowed and self.due_date:
            info += f"\nBorrowed by: {self.current_borrower}"
            info += f"\nDue Date: {self.due_date.strftime('%Y-%m-%d')}"
        if self.waiting_list:
            info += f"\nWaiting List: {len(self.waiting_list)} person(s)"
        return info