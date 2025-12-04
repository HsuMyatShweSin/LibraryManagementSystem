from typing import Optional
import customtkinter as ctk
import tkinter as tk
from datetime import datetime
from tkinter import messagebox
from genre import Genre
from library_book import Librarybook
from library_manager import LibraryManager
from member import Member
from rating import Rating

ctk.set_appearance_mode("white")
ctk.set_default_color_theme("dark-blue")

class LibraryApp(ctk.CTk):
    def __init__(self, role="admin", username="admin"):
        super().__init__()
        self.role = role 
        self.username = username
        self.title("Library Management System" if self.role=="admin" else "Library Member System")       
        self.create_sidebar()
        self.geometry("1200x700")        
        self.library = LibraryManager()         
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)       
        self.create_sidebar()
        self.create_main_content()
        
        self.member: Optional[Member] = None
        if self.role == "user":
            self.member = next((m for m in self.library.members if m.name == self.username), None)
            if self.member:
                self.title(f"Library Member System - Logged in as {self.member.name} (ID: {self.member.member_id})")

        self.show_home()
    
    def create_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        # rows
        for i in range(20):
            self.sidebar.grid_rowconfigure(i, weight=0)
        self.sidebar.grid_rowconfigure(20, weight=1)
        
        title_label = ctk.CTkLabel(self.sidebar, text="Library System",font=ctk.CTkFont(size=20, weight="bold"))
        title_label.grid(row=0, column=0, padx=20, pady=(20,10), sticky="w")
        current_row = 1
    
        self.btn_home = ctk.CTkButton(self.sidebar, text="Home", command=self.show_home)
        self.btn_home.grid(row=current_row, column=0, padx=20, pady=5, sticky="ew")
        current_row += 1 
    
        if self.role == "admin": #modes
            btn_books = ctk.CTkButton(self.sidebar, text="Books", command=self.show_books)
            btn_books.grid(row=current_row, column=0, padx=20, pady=5, sticky="ew")
            current_row += 1

            btn_members = ctk.CTkButton(self.sidebar, text="Members", command=self.show_members)
            btn_members.grid(row=current_row, column=0, padx=20, pady=5, sticky="ew")
            current_row += 1

            btn_reports = ctk.CTkButton(self.sidebar, text="Reports", command=self.show_reports)
            btn_reports.grid(row=current_row, column=0, padx=20, pady=5, sticky="ew")
            current_row += 1

            btn_events = ctk.CTkButton(self.sidebar, text="Event Log", command=self.show_events)
            btn_events.grid(row=current_row, column=0, padx=20, pady=5, sticky="ew")
            current_row += 1
        else:
            btn_borrow = ctk.CTkButton(self.sidebar, text="Borrow / Return", command=self.show_borrow_return)
            btn_borrow.grid(row=current_row, column=0, padx=20, pady=5, sticky="ew")
            current_row += 1

            btn_browse = ctk.CTkButton(self.sidebar, text="Browse Books", command=self.show_books)
            btn_browse.grid(row=current_row, column=0, padx=20, pady=5, sticky="ew")
            current_row += 1
  
    def create_main_content(self):
        self.main_frame = ctk.CTkFrame(self, corner_radius=0)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)
    
    def clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
    
    def get_selected_id(self, lb):
        sel = lb.curselection()
        if not sel:
            messagebox.showwarning("No selection", "Please select an item from the list.")
            return None
        text = lb.get(sel[0])
        return text.split("|")[0].strip()

    
    def show_home(self):
        self.clear_main_frame()

        title_text = "Welcome to Library Management System (Admin)" if self.role == "admin" else "Welcome to Library Member System"
        title = ctk.CTkLabel(self.main_frame, text=title_text, font=ctk.CTkFont(size=28, weight="bold"))
        title.grid(row=0, column=0, pady=20, sticky="w")
       
        stats_frame = ctk.CTkFrame(self.main_frame)
        stats_frame.grid(row=1, column=0, sticky="nsew", pady=10)
        stats_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        total_books = len(self.library.books)
        available_books = len([book for book in self.library.books if not book.is_borrowed])
        borrowed_books = total_books - available_books
        
        books_label = ctk.CTkLabel(stats_frame, text=f"Total Books\n{total_books}", font=ctk.CTkFont(size=20))
        books_label.grid(row=0, column=0, padx=20, pady=20)
        
        available_label = ctk.CTkLabel(stats_frame, text=f"Available\n{available_books}", font=ctk.CTkFont(size=20))
        available_label.grid(row=0, column=1, padx=20, pady=20)
        
        borrowed_label = ctk.CTkLabel(stats_frame, text=f"Borrowed\n{borrowed_books}", font=ctk.CTkFont(size=20))
        borrowed_label.grid(row=0, column=2, padx=20, pady=20)
        
        members_label = ctk.CTkLabel(stats_frame, text=f"Members\n{len(self.library.members)}", font=ctk.CTkFont(size=20))
        members_label.grid(row=1, column=0, padx=20, pady=20)
        
        events_label = ctk.CTkLabel(stats_frame, text=f"Events\n{len(self.library.events)}", font=ctk.CTkFont(size=20))
        events_label.grid(row=1, column=2, padx=20, pady=20)

    def show_books(self):
        self.clear_main_frame()

        top_frame = ctk.CTkFrame(self.main_frame)
        top_frame.grid(row=0, column=0, sticky="ew", pady=(0,10))
        top_frame.grid_columnconfigure(1, weight=1)

        title = ctk.CTkLabel(top_frame, text="Books", font=ctk.CTkFont(size=24, weight="bold"))
        title.grid(row=0, column=0, sticky="w", padx=10)

        search_var = tk.StringVar()
        search_entry = ctk.CTkEntry(top_frame, placeholder_text="Search by title/author/genre", textvariable=search_var)
        search_entry.grid(row=0, column=1, padx=10, sticky="ew")

        btn_search = ctk.CTkButton(top_frame, text="Search", command=lambda: populate_list(search_var.get()))
        btn_search.grid(row=0, column=2, padx=10)

        list_frame = ctk.CTkFrame(self.main_frame)
        list_frame.grid(row=1, column=0, sticky="nsew")
        list_frame.grid_rowconfigure(0, weight=1)
        list_frame.grid_columnconfigure(1, weight=1)

        lb = tk.Listbox(list_frame, exportselection=False)
        lb.grid(row=0, column=0, sticky="nsew", padx=(0,10), pady=5)
        info_text = tk.Text(list_frame, state="disabled", width=60)
        info_text.grid(row=0, column=1, sticky="nsew", padx=(0,10), pady=5)

        # Buttons frame (only shown if admin)
        btn_frame = ctk.CTkFrame(list_frame)
        btn_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=5)

        if self.role == "admin":
            add_btn = ctk.CTkButton(btn_frame, text="Add Book", command=lambda: self.add_book_popup())
            add_btn.grid(row=0, column=0, padx=5)
            edit_btn = ctk.CTkButton(btn_frame, text="Edit Selected", command=lambda: self.edit_book_popup(self.get_selected_id(lb)))
            edit_btn.grid(row=0, column=1, padx=5)
            delete_btn = ctk.CTkButton(btn_frame, text="Delete Selected", command=lambda: self.delete_book_action(self.get_selected_id(lb)))
            delete_btn.grid(row=0, column=2, padx=5)
        
        refresh_btn = ctk.CTkButton(btn_frame, text="Refresh", command=lambda: populate_list(search_var.get()))
        if self.role == "admin":
             refresh_btn.grid(row=0, column=3, padx=5)
        else:
             refresh_btn.grid(row=0, column=0, padx=5)

        def populate_list(query: str):
            lb.delete(0, tk.END)
            info_text.configure(state="normal")
            info_text.delete("1.0", tk.END)
            results = self.library.search_books(query) if query else self.library.books
            for book in results:
                lb.insert(tk.END, f"{book.book_id} | {book.title} | {book.author}")
            info_text.configure(state="disabled")

        def on_select(evt):
            sel = lb.curselection()
            if not sel:
                return
            book_id = lb.get(sel[0]).split("|")[0].strip()
            book = self.library.find_book(book_id)
            if book:
                info_text.configure(state="normal")
                info_text.delete("1.0", tk.END)
                info_text.insert(tk.END, book.display_info())
                info_text.configure(state="disabled")

        lb.bind("<<ListboxSelect>>", on_select)

        populate_list("")

    def add_book_popup(self):
        popup = ctk.CTkToplevel(self)
        popup.title("Add Book")
        popup.geometry("380x400")

        tk.Label(popup, text="ID:").pack(padx=10, pady=(10,0), anchor="w")
        id_entry = ctk.CTkEntry(popup)
        id_entry.pack(padx=10, pady=5, fill="x")

        tk.Label(popup, text="Title:").pack(padx=10, pady=(10,0), anchor="w")
        title_entry = ctk.CTkEntry(popup)
        title_entry.pack(padx=10, pady=5, fill="x")

        tk.Label(popup, text="Author:").pack(padx=10, pady=(10,0), anchor="w")
        author_entry = ctk.CTkEntry(popup)
        author_entry.pack(padx=10, pady=5, fill="x")

        tk.Label(popup, text="Genre:").pack(padx=10, pady=(10,0), anchor="w")
        genre_menu = ctk.CTkOptionMenu(popup, values=[g.value for g in Genre])
        genre_menu.pack(padx=10, pady=5, fill="x")

        tk.Label(popup, text="Rating:").pack(padx=10, pady=(10,0), anchor="w")
        rating_menu = ctk.CTkOptionMenu(popup, values=[r.value for r in Rating])
        rating_menu.pack(padx=10, pady=5, fill="x")
        
        tk.Label(popup, text="Description:").pack(padx=10, pady=(10,0), anchor="w")
        description_entry = ctk.CTkEntry(popup, height=30)
        description_entry.pack(padx=10, pady=5,fill = "x")

        def add_action():
            book_id = id_entry.get().strip()
            title = title_entry.get().strip()
            author = author_entry.get().strip()
            genre_val = genre_menu.get()
            rating_val = rating_menu.get()
            description = description_entry.get()
            if not (book_id and title and author and genre_val and rating_val and description):
                messagebox.showwarning("Missing fields", "Please fill all fields.")
                return
            new_book = Librarybook(book_id, title, author, Genre(genre_val), Rating(rating_val), description)
            if self.library.add_book(new_book):
                messagebox.showinfo("Success", "Book added.")
                popup.destroy()

        ctk.CTkButton(popup, text="Add", command=add_action).pack(pady=15)


    def edit_book_popup(self, book_id: Optional[str]):
        if not book_id:
            return
        book = self.library.find_book(book_id)
        if not book:
            messagebox.showerror("Not found", "Book not found.")
            return
        
        popup = ctk.CTkToplevel(self)
        popup.title("Edit Book")
        popup.geometry("400x360")

        tk.Label(popup, text="ID:").pack(padx=10, pady=(10,0), anchor="w")
        id_entry = ctk.CTkEntry(popup)
        id_entry.insert(0, book.book_id)
        id_entry.configure(state="disabled")
        id_entry.pack(padx=10, pady=5, fill="x")

        tk.Label(popup, text="Title:").pack(padx=10, pady=(10,0), anchor="w")
        title_entry = ctk.CTkEntry(popup)
        title_entry.insert(0, book.title)
        title_entry.pack(padx=10, pady=5, fill="x")

        tk.Label(popup, text="Author:").pack(padx=10, pady=(10,0), anchor="w")
        author_entry = ctk.CTkEntry(popup)
        author_entry.insert(0, book.author)
        author_entry.pack(padx=10, pady=5, fill="x")

        tk.Label(popup, text="Genre:").pack(padx=10, pady=(10,0), anchor="w")
        genre_menu = ctk.CTkOptionMenu(popup, values=[g.value for g in Genre])
        genre_menu.set(book.genre.value)
        genre_menu.pack(padx=10, pady=5, fill="x")

        tk.Label(popup, text="Rating:").pack(padx=10, pady=(10,0), anchor="w")
        rating_menu = ctk.CTkOptionMenu(popup, values=[r.value for r in Rating])
        rating_menu.set(book.rating.value)
        rating_menu.pack(padx=10, pady=5, fill="x")
        
        tk.Label(popup, text="Description:").pack(padx=10, pady=(10,0), anchor="w")
        description_entry = ctk.CTkEntry(popup, height=30)
        description_entry.pack(padx=10, pady=5,fill = "x")

        def save_action():
            new_title = title_entry.get().strip()
            new_author = author_entry.get().strip()
            new_genre = Genre(genre_menu.get())
            new_rating = Rating(rating_menu.get())
            new_description = description_entry.get().strip()
            new_book = Librarybook(book.book_id, new_title, new_author, new_genre, new_rating, new_description)
            new_book.is_borrowed = book.is_borrowed
            new_book.current_borrower = book.current_borrower
            new_book.borrow_date = book.borrow_date
            new_book.due_date = book.due_date
            new_book.borrow_history = book.borrow_history
            new_book.waiting_list = book.waiting_list
            if self.library.edit_book(book.book_id, new_book):
                messagebox.showinfo("Saved", "Book updated.")
                popup.destroy()
            else:
                messagebox.showerror("Error", "Could not update book.")

        save_btn = ctk.CTkButton(popup, text="Save", command=save_action)
        save_btn.pack(pady=15)

    def delete_book_action(self, book_id: Optional[str]):

        if not book_id:
            return
        book = self.library.find_book(book_id)
        if not book:
            messagebox.showerror("Not found", "Book not found.")
            return
        if messagebox.askyesno("Confirm Delete", f"Delete book '{book.title}'?"):
            if self.library.delete_book(book_id):
                messagebox.showinfo("Deleted", "Book deleted.")
            else:
                messagebox.showerror("Error", "Could not delete book.")

    def show_members(self):
        self.clear_main_frame()
        
        top_frame = ctk.CTkFrame(self.main_frame)
        top_frame.grid(row=0, column=0, sticky="ew", pady=(0,10))
        top_frame.grid_columnconfigure(1, weight=1)

        title = ctk.CTkLabel(top_frame, text="Members", font=ctk.CTkFont(size=24, weight="bold"))
        title.grid(row=0, column=0, sticky="w", padx=10)

        search_var = tk.StringVar()
        search_entry = ctk.CTkEntry(top_frame, placeholder_text="Search by ID or Name", textvariable=search_var)
        search_entry.grid(row=0, column=1, padx=10, sticky="ew")

        btn_search = ctk.CTkButton(top_frame, text="Search", command=lambda: populate_members(search_var.get()))
        btn_search.grid(row=0, column=2, padx=10)

        list_frame = ctk.CTkFrame(self.main_frame)
        list_frame.grid(row=1, column=0, sticky="nsew")
        list_frame.grid_rowconfigure(0, weight=1)
        list_frame.grid_columnconfigure(1, weight=1)

        lb = tk.Listbox(list_frame, exportselection=False)
        lb.grid(row=0, column=0, sticky="nsew", padx=(0,10), pady=5)
        info_text = tk.Text(list_frame, state="disabled", width=60)
        info_text.grid(row=0, column=1, sticky="nsew", padx=(0,10), pady=5)

        btn_frame = ctk.CTkFrame(list_frame)
        btn_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=5)
        add_btn = ctk.CTkButton(btn_frame, text="Add Member", command=lambda: self.add_member_popup())
        add_btn.grid(row=0, column=0, padx=5)
        edit_btn = ctk.CTkButton(btn_frame, text="Edit Selected", command=lambda: self.edit_member_popup(self.get_selected_id(lb)))
        edit_btn.grid(row=0, column=1, padx=5)
        refresh_btn = ctk.CTkButton(btn_frame, text="Refresh", command=lambda: populate_members(search_var.get()))
        refresh_btn.grid(row=0, column=3, padx=5)

        if self.role != "admin":
            add_btn.configure(state="disabled")
            edit_btn.configure(state="disabled")
                        
        def populate_members(query: str):
            lb.delete(0, tk.END)
            info_text.configure(state="normal")
            info_text.delete("1.0", tk.END)
            results = self.library.search_members(query) if query else self.library.members
            for member in results:
                lb.insert(tk.END, f"{member.member_id} | {member.name}")
            info_text.configure(state="disabled")

        def on_select(evt):
            sel = lb.curselection()
            if not sel:
                return
            member_id = lb.get(sel[0]).split("|")[0].strip()
            member = self.library.find_member(member_id)
            if member:
                info_text.configure(state="normal")
                info_text.delete("1.0", tk.END)
                info_text.insert(tk.END, member.display_info())
                info_text.configure(state="disabled")

        lb.bind("<<ListboxSelect>>", on_select)

        populate_members("")

    def add_member_popup(self):
        popup = ctk.CTkToplevel(self)
        popup.title("Add Member")
        popup.geometry("380x400")

        tk.Label(popup, text="Member ID:").pack(padx=10, pady=(10,0), anchor="w")
        id_entry = ctk.CTkEntry(popup)
        id_entry.pack(padx=10, pady=5, fill="x")

        tk.Label(popup, text="Name:").pack(padx=10, pady=(10,0), anchor="w")
        name_entry = ctk.CTkEntry(popup)
        name_entry.pack(padx=10, pady=5, fill="x")

        tk.Label(popup, text="Email:").pack(padx=10, pady=(10,0), anchor="w")
        email_entry = ctk.CTkEntry(popup)
        email_entry.pack(padx=10, pady=5, fill="x")

        tk.Label(popup, text="Phone:").pack(padx=10, pady=(10,0), anchor="w")
        phone_entry = ctk.CTkEntry(popup)
        phone_entry.pack(padx=10, pady=5, fill="x")

        def add_action():
            mid = id_entry.get().strip()
            name = name_entry.get().strip()
            email = email_entry.get().strip()
            phone = phone_entry.get().strip()
            if not (mid and name):
                messagebox.showwarning("Missing fields", "Please provide at least ID and name.")
                return
            new_member = Member(mid, name, email, phone)
            if self.library.add_member(new_member):
                messagebox.showinfo("Success", "Member added.")
                popup.destroy()

        ctk.CTkButton(popup, text="Add", command=add_action).pack(pady=15)

    def edit_member_popup(self, member_id: Optional[str]):
        if not member_id:
            return
        member = self.library.find_member(member_id)
        if not member:
            messagebox.showerror("Not found", "Member not found.")
            return
        
        popup = ctk.CTkToplevel(self)
        popup.title("Edit Member")
        popup.geometry("380x300")

        tk.Label(popup, text="Member ID:").pack(padx=10, pady=(10,0), anchor="w")
        id_entry = ctk.CTkEntry(popup)
        id_entry.insert(0, member.member_id)
        id_entry.configure(state="disabled")
        id_entry.pack(padx=10, pady=5, fill="x")

        tk.Label(popup, text="Name:").pack(padx=10, pady=(10,0), anchor="w")
        name_entry = ctk.CTkEntry(popup)
        name_entry.insert(0, member.name)
        name_entry.configure(state="disabled")
        name_entry.pack(padx=10, pady=5, fill="x")

        tk.Label(popup, text="Email:").pack(padx=10, pady=(10,0), anchor="w")
        email_entry = ctk.CTkEntry(popup)
        email_entry.insert(0, member.email)
        email_entry.pack(padx=10, pady=5, fill="x")

        tk.Label(popup, text="Phone:").pack(padx=10, pady=(10,0), anchor="w")
        phone_entry = ctk.CTkEntry(popup)
        phone_entry.insert(0, member.phone)
        phone_entry.pack(padx=10, pady=5, fill="x")

        def save_action():
            new_member = Member(member.member_id, name_entry.get().strip(), email_entry.get().strip(), phone_entry.get().strip())
            new_member.borrow_history = member.borrow_history
            new_member.borrowed_books = member.borrowed_books
            new_member.waiting_for = member.waiting_for
            if self.library.edit_member(member.member_id, new_member):
                messagebox.showinfo("Saved", "Member updated.")
                popup.destroy()
            else:
                messagebox.showerror("Error", "Could not update member.")

        save_btn = ctk.CTkButton(popup, text="Save", command=save_action)
        save_btn.pack(pady=15)

    def show_borrow_return(self):
        self.clear_main_frame()
        title = ctk.CTkLabel(self.main_frame, text="Borrow / Return", font=ctk.CTkFont(size=24, weight="bold"))
        title.grid(row=0, column=0, sticky="w", pady=(0,10))

        frame = ctk.CTkFrame(self.main_frame)
        frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        frame.grid_columnconfigure(1, weight=1)

        tk.Label(frame, text="Borrower ID (e.g., M001):").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        borrower_entry = ctk.CTkEntry(frame)
        borrower_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        tk.Label(frame, text="Book ID:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        book_entry = ctk.CTkEntry(frame)
        book_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

        def borrow_action():
            borrower_id = borrower_entry.get().strip()
            book_id = book_entry.get().strip()
            if not (borrower_id and book_id):
                messagebox.showwarning("Missing fields", "Please enter borrower ID and book ID.")
                return
            ok, msg = self.library.borrow_book(borrower_id, book_id)
            if ok:
                messagebox.showinfo("Success", msg)
            else:
                messagebox.showwarning("Failed", msg)

        def return_action():
            borrower_id = borrower_entry.get().strip()
            book_id = book_entry.get().strip()
            if not (borrower_id and book_id):
                messagebox.showwarning("Missing fields", "Please enter borrower ID and book ID.")
                return
            ok, msg = self.library.return_book(borrower_id, book_id)
            if ok:
                messagebox.showinfo("Success", msg)
            else:
                messagebox.showwarning("Failed", msg)

        borrow_btn = ctk.CTkButton(frame, text="Borrow", command=borrow_action)
        borrow_btn.grid(row=2, column=0, padx=5, pady=10)
        return_btn = ctk.CTkButton(frame, text="Return", command=return_action)
        return_btn.grid(row=2, column=1, padx=5, pady=10)

    def show_reports(self):
        self.clear_main_frame()
        title = ctk.CTkLabel(self.main_frame, text="Reports", font=ctk.CTkFont(size=24, weight="bold"))
        title.grid(row=0, column=0, sticky="w", pady=(0,10))

        frame = ctk.CTkFrame(self.main_frame)
        frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        frame.grid_columnconfigure(0, weight=1)

        waiting_label = ctk.CTkLabel(frame, text="Waiting Lists")
        waiting_label.grid(row=0, column=0, sticky="w", padx=5, pady=(5,0))
        waiting_text = tk.Text(frame, height=4)
        waiting_text.grid(row=1, column=0, sticky="ew", padx=5, pady=(0,10))
        waiting_text.insert(tk.END, self.library.get_waiting_list_status())
        waiting_text.configure(state="disabled")

        overdue_label = ctk.CTkLabel(frame, text="Overdue Books")
        overdue_label.grid(row=2, column=0, sticky="w", padx=5, pady=(5,0))
        overdue_text = tk.Text(frame, height=6)
        overdue_text.grid(row=3, column=0, sticky="ew", padx=5, pady=(0,10))
        overdue_text.insert(tk.END, self.library.get_overdue_books())
        overdue_text.configure(state="disabled")

        tk.Label(frame, text="Member Stats (enter Member ID):").grid(row=4, column=0, sticky="w", padx=5, pady=(5,0))
        mem_entry = ctk.CTkEntry(frame)
        mem_entry.grid(row=5, column=0, sticky="ew", padx=5, pady=5)

        mem_stats_text = tk.Text(frame, height=4)
        mem_stats_text.grid(row=6, column=0, sticky="ew", padx=5, pady=5)

        def get_stats():
            mid = mem_entry.get().strip()
            if not mid:
                messagebox.showwarning("Missing", "Enter a member ID.")
                return
            stats = self.library.get_member_statistics(mid)
            mem_stats_text.configure(state="normal")
            mem_stats_text.delete("1.0", tk.END)
            if stats:
                mem_stats_text.insert(tk.END, stats)
            else:
                mem_stats_text.insert(tk.END, "Member not found.")
            mem_stats_text.configure(state="disabled")

        stats_btn = ctk.CTkButton(frame, text="Get Stats", command=get_stats)
        stats_btn.grid(row=7, column=0, sticky="e", padx=5, pady=5)

    def show_events(self):
        self.clear_main_frame()
        title = ctk.CTkLabel(self.main_frame, text="Event Log", font=ctk.CTkFont(size=24, weight="bold"))
        title.grid(row=0, column=0, sticky="w", pady=(0,10))

        control_frame = ctk.CTkFrame(self.main_frame)
        control_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=(0,10))
        
        tk.Label(control_frame, text="Filter by:").grid(row=0, column=0, padx=5, pady=5)
        filter_var = tk.StringVar(value="All")
        filter_menu = ctk.CTkOptionMenu(control_frame, variable=filter_var, values=["All", "Books", "Members", "Borrowed", "Returned", "Failed"])
        filter_menu.grid(row=0, column=1, padx=5, pady=5)
        
        def clear_log():
            if messagebox.askyesno("Confirm", "Clear all event logs?"):
                self.library.events.clear()
                self.library.add_event("Event Log", "Event log cleared") 
                self.library.save_data() # Save the change
                update_display()
        
        clear_btn = ctk.CTkButton(control_frame, text="Clear Log", command=clear_log)
        clear_btn.grid(row=0, column=2, padx=5, pady=5)
        
        def export_log():
            try:
                filename = f"event_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                with open(filename, 'w') as f:
                    f.write("Library Management System - Event Log\n")
                    f.write("=" * 50 + "\n\n")
                    for ev in self.library.events:
                        f.write(str(ev) + "\n")
                messagebox.showinfo("Success", f"Event log exported to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export: {str(e)}")
        
        export_btn = ctk.CTkButton(control_frame, text="Export Log", command=export_log)
        export_btn.grid(row=0, column=3, padx=5, pady=5)
        
        refresh_btn = ctk.CTkButton(control_frame, text="Refresh", command=lambda: update_display())
        refresh_btn.grid(row=0, column=4, padx=5, pady=5)

        text_frame = ctk.CTkFrame(self.main_frame)
        text_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)
        text_frame.grid_rowconfigure(0, weight=1)
        text_frame.grid_columnconfigure(0, weight=1)
        
        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        text = tk.Text(text_frame, yscrollcommand=scrollbar.set, wrap=tk.WORD)
        text.grid(row=0, column=0, sticky="nsew")
        scrollbar.config(command=text.yview)
        
        def update_display():
            text.configure(state="normal")
            text.delete("1.0", tk.END)
            
            filter_value = filter_var.get()
            filtered_events = []
            
            for event in self.library.events:
                event_type = event.event_type.lower()
                
                if filter_value == "All":
                    filtered_events.append(event)
                elif filter_value == "Books" and ("book added" in event_type or "book edited" in event_type or "book deleted" in event_type):
                    filtered_events.append(event)
                elif filter_value == "Members" and ("member added" in event_type or "member edited" in event_type or "member deleted" in event_type):
                    filtered_events.append(event)
                elif filter_value == "Borrowed" and "book borrowed" in event_type:
                    filtered_events.append(event)
                elif filter_value == "Returned" and "book returned" in event_type:
                    filtered_events.append(event)
                elif filter_value == "Failed" and ("failed" in event.details.lower() or "waiting list" in event_type.lower()):
                     filtered_events.append(event)
            
            if not filtered_events:
                text.insert(tk.END, "No events to display.\n")
            else:
                text.insert(tk.END, f"Showing {len(filtered_events)} of {len(self.library.events)} events\n")
                text.insert(tk.END, "=" * 80 + "\n\n")
                for ev in reversed(filtered_events):  # Most recent first
                    text.insert(tk.END, str(ev) + "\n")
            
            text.configure(state="disabled")
        update_display()
        
        filter_var.trace('w', lambda *args: update_display())