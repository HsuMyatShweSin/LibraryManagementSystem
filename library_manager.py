from datetime import datetime, timedelta
import os
import pickle
from tkinter import messagebox
from typing import List, Optional
from borrow_record import BorrowRecord
from library_book import Librarybook
from library_event import LibraryEvent
from member import Member

class LibraryManager:
    def __init__(self):
        self.books: List[Librarybook] = []
        self.members: List[Member] = []
        self.events: List[LibraryEvent] = []
        self.load_data()

    def get_next_member_id(self) -> str:
        max_id = 0
        for member in self.members:
            try:
                if member.member_id.upper().startswith('M'):
                    num_part = member.member_id[1:]
                else:
                    num_part = member.member_id
                    
                current_id = int(num_part)
                if current_id > max_id:
                    max_id = current_id
            except ValueError:
                continue
                
        next_id = max_id + 1
        return f"M{next_id:03d}"

    def add_event(self, event_type: str, details: str):
        event = LibraryEvent(event_type, details, datetime.now())
        self.events.append(event)
        self.save_data()

    def borrow_book(self, borrower_id: str, book_id: str) -> tuple[bool, str]:
        book = self.find_book(book_id)
        if not book:
            return False, "Book not found"
        
        member = self.find_member(borrower_id)
        if not member:
            return False, "Member not found"

        if book.is_borrowed:
            if borrower_id not in book.waiting_list:
                book.waiting_list.append(borrower_id)
                member.waiting_for.append(book_id)
                self.add_event("Waiting List", f"{member.name} added to waiting list for {book.title}")
                return False, "Book is currently borrowed. Added to waiting list."
            return False, "Already in waiting list"

        if book.waiting_list and book.waiting_list[0] != borrower_id:
            return False, "Other members are waiting for this book"

        if borrower_id in book.waiting_list:
            book.waiting_list.remove(borrower_id)
            member.waiting_for.remove(book_id)

        borrow_date = datetime.now()
        record = BorrowRecord(borrower_id, book_id, borrow_date)
        
        book.is_borrowed = True
        book.current_borrower = member.name
        book.borrow_date = borrow_date
        book.due_date = borrow_date + timedelta(days=14)
        book.borrow_history.append(record)
        
        member.borrowed_books.append(book)
        member.borrow_history.append(record)
        
        self.add_event("Book Borrowed", f"{member.name} borrowed {book.title}")
        self.save_data()
        return True, "Book borrowed successfully"

    def return_book(self, member_id: str, book_id: str) -> tuple[bool, str]:
        member = self.find_member(member_id)
        if not member:
            return False, "Member not found"

        book = self.find_book(book_id)
        if not book:
            return False, "Book not found"

        if not book.is_borrowed:
            return False, "Book is not borrowed"

        if book not in member.borrowed_books:
            return False, "Book was not borrowed by this member"

        for record in book.borrow_history:
            if record.member_id == member_id and not record.return_date:
                record.return_date = datetime.now()
                break

        for record in member.borrow_history:
            if record.book_id == book_id and not record.return_date:
                record.return_date = datetime.now()
                break

        book.is_borrowed = False
        book.current_borrower = None
        book.borrow_date = None
        book.due_date = None
        member.borrowed_books.remove(book)

        self.add_event("Book Returned", f"{member.name} returned {book.title}")

        if book.waiting_list:
            next_member_id = book.waiting_list[0]
            next_member = self.find_member(next_member_id)
            if next_member:
                self.add_event("Waiting List", f"Book {book.title} is now available for {next_member.name}")

        self.save_data()
        return True, "Book returned successfully"

    def add_book(self, book: Librarybook) -> bool:
        if self.find_book(book.book_id) is None:
            self.books.append(book)
            self.add_event("Book Added", f"New book added: {book.title}")
            self.save_data()
            return True
        else:
            messagebox.showerror("Error", f"Book with ID {book.book_id} already exists.")
            return False

    def edit_book(self, book_id: str, new_book: Librarybook) -> bool:
        book = self.find_book(book_id)
        if book:
            self.books[self.books.index(book)] = new_book
            self.add_event("Book Edited", f"Book {book.title} was edited")
            self.save_data()
            return True
        return False

    def delete_book(self, book_id: str) -> bool:
        book = self.find_book(book_id)
        if book:
            self.books.remove(book)
            self.add_event("Book Deleted", f"Book {book.title} was deleted")
            self.save_data()
            return True
        return False
    
    def log_event(self, event: str):
        self.add_event("General Log", event)

    def add_member(self, member: Member) -> bool:
        # We only check for ID existence, as name (username) might be the same
        if self.find_member(member.member_id) is None: 
            self.members.append(member)
            self.add_event("Member Added", f"New member added: {member.name} (ID: {member.member_id})")
            self.save_data()
            return True
        else:
            messagebox.showerror("Error", f"Member with ID {member.member_id} already exists.")
            return False
        
    def edit_member(self, member_id: str, new_member: Member) -> bool:
        member = self.find_member(member_id)
        if member:
            self.members[self.members.index(member)] = new_member
            self.add_event("Member Edited", f"Member {member.name} was edited")
            self.save_data()
            return True
        return False

    def find_book(self, book_id: str) -> Optional[Librarybook]:
        return next((book for book in self.books if book.book_id == book_id), None)

    def find_member(self, member_id: str) -> Optional[Member]:
        return next((member for member in self.members if member.member_id == member_id), None)
    
    def search_members(self, query: str) -> List[Member]:
        query = query.lower()
        results = []
        for member in self.members:
            if (query in member.member_id.lower() or 
                query in member.name.lower()):
                results.append(member)
        return results

    def save_data(self):
        try:
            with open('library_data.pkl', 'wb') as file:
                pickle.dump((self.books, self.members, self.events), file)
        except Exception as e:
            print(f"Error saving data: {str(e)}")

    def load_data(self):
        try:
            if os.path.exists('library_data.pkl'):
                with open('library_data.pkl', 'rb') as file:
                    self.books, self.members, self.events = pickle.load(file)
            else:
                self.books = []
                self.members = []
                self.events = []
        except Exception as e:
            print(f"Error loading data: {str(e)}")
    
    def get_waiting_list_status(self):
        waiting_status = []
        for book in self.books:
            if book.waiting_list:
                waiting_status.append(f"{book.title}: {len(book.waiting_list)} person(s)")
        return "\n".join(waiting_status) if waiting_status else "No books have waiting lists"

    def get_overdue_books(self):
        overdue = []
        current_date = datetime.now()
        for book in self.books:
            if book.is_borrowed and book.due_date and current_date > book.due_date:
                days_overdue = (current_date - book.due_date).days
                overdue.append(f"{book.title} - Borrowed by {book.current_borrower} - {days_overdue} days overdue")
        return "\n".join(overdue) if overdue else "No overdue books"

    def search_books(self, query: str) -> List[Librarybook]:
        query = query.lower()
        results = []
        for book in self.books:
            if (query in book.title.lower() or 
                query in book.author.lower() or 
                query in book.genre.value.lower()):
                results.append(book)
        return results

    def get_member_statistics(self, member_id: str) -> Optional[str]:
        member = self.find_member(member_id)
        if not member:
            return None
        
        total_borrowed = len(member.borrow_history)
        currently_borrowed = len(member.borrowed_books)
        waiting_for = len(member.waiting_for)
        
        stats = f"Statistics for {member.name}\n"
        stats += f"Total books borrowed: {total_borrowed}\n"
        stats += f"Currently borrowed: {currently_borrowed}\n"
        stats += f"Books waiting for: {waiting_for}"
        return stats