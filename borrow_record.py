from datetime import datetime
from typing import Optional

class BorrowRecord:
    def __init__(self, member_id: str, book_id: str, borrow_date: datetime):
        self.member_id = member_id
        self.book_id = book_id
        self.borrow_date = borrow_date
        self.return_date: Optional[datetime] = None
    
    def __str__(self):
        status = "Returned" if self.return_date else "Borrowed"
        borrow_date_str = self.borrow_date.strftime("%Y-%m-%d %H:%M")
        return_date_str = self.return_date.strftime("%Y-%m-%d %H:%M") if self.return_date else "Not returned yet"
        return f"Status: {status}, Borrowed: {borrow_date_str}, Returned: {return_date_str}"