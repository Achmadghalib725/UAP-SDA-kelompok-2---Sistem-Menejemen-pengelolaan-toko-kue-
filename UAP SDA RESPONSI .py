import tkinter as tk
from tkinter import messagebox
import csv

class Library:
    def __init__(self):
        self.books = []
        self.transactions = []
        self.orders = []
        self.load_data()

    def load_data(self):
        try:
            with open('Promp csv.csv', 'r', newline='', encoding='utf-8-sig') as file:
                reader = csv.reader(file)
                self.books = list(reader)
        except FileNotFoundError:
            self.books = []

        try:
            with open('transactions.csv', 'r', newline='', encoding='utf-8-sig') as file:
                reader = csv.reader(file)
                self.transactions = list(reader)
        except FileNotFoundError:
            self.transactions = []

        try:
            with open('orders.csv', 'r', newline='', encoding='utf-8-sig') as file:
                reader = csv.reader(file)
                self.orders = list(reader)
        except FileNotFoundError:
            self.orders = []

    def save_data(self):
        with open('Promp csv.csv', 'w', newline='', encoding='utf-8-sig') as file:
            writer = csv.writer(file)
            writer.writerows(self.books)

        with open('transactions.csv', 'w', newline='', encoding='utf-8-sig') as file:
            writer = csv.writer(file)
            writer.writerows(self.transactions)

        with open('orders.csv', 'w', newline='', encoding='utf-8-sig') as file:
            writer = csv.writer(file)
            writer.writerows(self.orders)

    def add_book(self, book):
        self.books.append(book)
        self.save_data()

    def remove_book(self, book):
        if book in self.books:
            self.books.remove(book)
            self.save_data()
            return True
        else:
            return False

    def find_book(self, title):
        for book in self.books:
            if book[1].lower() == title.lower():  # Title is now the second element
                return book
        return None

    def order_book(self, book, user):
        self.orders.append([book, user])
        self.save_data()

    def process_order(self, book, user):
        if [book, user] in self.orders:
            self.orders.remove([book, user])
            self.transactions.append([book, user])
            self.save_data()
            return True
        else:
            return False

    def get_transactions(self):
        return self.transactions

    def get_orders(self):
        return self.orders

    def get_books(self):
        return self.books

    def sort_books(self):
        self.books.sort(key=lambda x: x[1].lower())  # Sort by title, which is the second element
        self.save_data()


class LibraryGUI:
    def __init__(self, root):
        self.root = root
        self.root.title('Library Management System')
        self.root.geometry('800x600')  # Adjusted size to accommodate more columns

        self.library = Library()

        self.label_title = tk.Label(root, text='Library Management System', font=('Helvetica', 18, 'bold'))
        self.label_title.pack(pady=10)

        self.frame = tk.Frame(root)
        self.frame.pack(pady=20)

        self.label_instruction = tk.Label(self.frame, text='Enter book title:')
        self.label_instruction.grid(row=0, column=0, padx=10)

        self.entry_title = tk.Entry(self.frame, width=30)
        self.entry_title.grid(row=0, column=1, padx=10)

        self.button_search = tk.Button(self.frame, text='Search', command=self.search_book)
        self.button_search.grid(row=0, column=2, padx=10)

        self.label_books = tk.Label(root, text='Books:')
        self.label_books.pack()

        self.listbox_books = tk.Listbox(root, width=100, height=10)
        self.listbox_books.pack(pady=10)

        self.refresh_books()

        self.button_add = tk.Button(root, text='Add Book', command=self.add_book)
        self.button_add.pack()

        self.button_remove = tk.Button(root, text='Remove Book', command=self.remove_book)
        self.button_remove.pack()

        self.label_orders = tk.Label(root, text='Orders:')
        self.label_orders.pack()

        self.listbox_orders = tk.Listbox(root, width=100, height=5)
        self.listbox_orders.pack()

        self.refresh_orders()

        self.button_order = tk.Button(root, text='Order Book', command=self.order_book)
        self.button_order.pack()

        self.label_transactions = tk.Label(root, text='Transactions:')
        self.label_transactions.pack()

        self.listbox_transactions = tk.Listbox(root, width=100, height=5)
        self.listbox_transactions.pack()

        self.refresh_transactions()

        self.button_process = tk.Button(root, text='Process Order', command=self.process_order)
        self.button_process.pack()

        self.button_refresh = tk.Button(root, text='Refresh', command=self.refresh_all)
        self.button_refresh.pack(pady=10)

        self.button_sort = tk.Button(root, text='Sort Books', command=self.sort_books)
        self.button_sort.pack()

    def search_book(self):
        title = self.entry_title.get().strip()
        book = self.library.find_book(title)
        if book:
            messagebox.showinfo('Book Found', f'Book found: {book[1]} - {book[2]}, {book[3]}, {book[4]} per day')
        else:
            messagebox.showinfo('Book Not Found', f'Book with title "{title}" not found.')

    def add_book(self):
        title = self.entry_title.get().strip()
        if title:
            # Add input fields for genre, author, and price per day
            genre = 'Unknown'
            author = 'Unknown'
            price_per_day = '0'
            book_id = str(len(self.library.get_books()) + 1)
            book = [book_id, title, genre, author, price_per_day]
            self.library.add_book(book)
            self.refresh_books()
            messagebox.showinfo('Book Added', f'Book added successfully: {title}')
        else:
            messagebox.showwarning('Empty Field', 'Please enter a book title.')

    def remove_book(self):
        title = self.entry_title.get().strip()
        book = self.library.find_book(title)
        if book:
            self.library.remove_book(book)
            self.refresh_books()
            messagebox.showinfo('Book Removed', f'Book removed successfully: {title}')
        else:
            messagebox.showwarning('Book Not Found', f'Book with title "{title}" not found.')

    def order_book(self):
        title = self.entry_title.get().strip()
        if title:
            book = self.library.find_book(title)
            if book:
                self.library.order_book(title, 'User123')  # Hardcoded user for demonstration
                self.refresh_orders()
                messagebox.showinfo('Book Ordered', f'Book ordered successfully: {title}')
            else:
                messagebox.showwarning('Book Not Found', f'Book with title "{title}" not found.')
        else:
            messagebox.showwarning('Empty Field', 'Please enter a book title.')

    def process_order(self):
        title = self.entry_title.get().strip()
        if title:
            success = self.library.process_order(title, 'User123')  # Hardcoded user for demonstration
            if success:
                self.refresh_orders()
                self.refresh_transactions()
                messagebox.showinfo('Order Processed', f'Order processed successfully: {title}')
            else:
                messagebox.showwarning('Order Not Found', f'Order for book "{title}" not found.')
        else:
            messagebox.showwarning('Empty Field', 'Please enter a book title.')

    def refresh_books(self):
        self.listbox_books.delete(0, tk.END)
        for book in self.library.get_books():
            self.listbox_books.insert(tk.END, f'{book[0]} - {book[1]}, {book[2]}, {book[3]}, {book[4]} per day')

    def refresh_orders(self):
        self.listbox_orders.delete(0, tk.END)
        for order in self.library.get_orders():
            self.listbox_orders.insert(tk.END, f'{order[0]} - {order[1]}')

    def refresh_transactions(self):
        self.listbox_transactions.delete(0, tk.END)
        for transaction in self.library.get_transactions():
            self.listbox_transactions.insert(tk.END, f'{transaction[0]} - {transaction[1]}')

    def refresh_all(self):
        self.refresh_books()
        self.refresh_orders()
        self.refresh_transactions()

    def sort_books(self):
        self.library.sort_books()
        self.refresh_books()


if __name__ == '__main__':
    root = tk.Tk()
    app = LibraryGUI(root)
    root.mainloop()
