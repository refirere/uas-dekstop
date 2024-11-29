import sqlite3
from tkinter import *
from tkinter import ttk, messagebox

# Setup database
def initialize_db():
    conn = sqlite3.connect("perpustakaan.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            year INTEGER NOT NULL,
            returned BOOLEAN DEFAULT 1
        )
    """)
    conn.commit()
    conn.close()

# Add book to database
def add_book():
    title = entry_title.get()
    author = entry_author.get()
    try:
        year = int(entry_year.get())
    except ValueError:
        messagebox.showerror("Input Error", "Tahun harus berupa angka.")
        return

    if title == "" or author == "":
        messagebox.showerror("Input Error", "Semua bidang harus diisi.")
        return

    conn = sqlite3.connect("perpustakaan.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO books (title, author, year) VALUES (?, ?, ?)",
                   (title, author, year))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Buku berhasil ditambahkan.")
    reset_form()
    show_books()

# Update book
def update_book():
    try:
        selected_item = table.selection()[0]
    except IndexError:
        messagebox.showerror("Selection Error", "Pilih buku yang ingin diubah.")
        return

    book_id = table.item(selected_item, "values")[0]
    title = entry_title.get()
    author = entry_author.get()
    try:
        year = int(entry_year.get())
    except ValueError:
        messagebox.showerror("Input Error", "Tahun harus berupa angka.")
        return

    conn = sqlite3.connect("perpustakaan.db")
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE books 
        SET title = ?, author = ?, year = ?
        WHERE id = ?
    """, (title, author, year, book_id))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Buku berhasil diperbarui.")
    reset_form()
    show_books()

# Delete book
def delete_book():
    try:
        selected_item = table.selection()[0]
    except IndexError:
        messagebox.showerror("Selection Error", "Pilih buku yang ingin dihapus.")
        return

    book_id = table.item(selected_item, "values")[0]
    conn = sqlite3.connect("perpustakaan.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Buku berhasil dihapus.")
    reset_form()
    show_books()

# Return book
def return_book():
    try:
        selected_item = table.selection()[0]
    except IndexError:
        messagebox.showerror("Selection Error", "Pilih buku yang ingin dikembalikan.")
        return

    book_id = table.item(selected_item, "values")[0]
    conn = sqlite3.connect("perpustakaan.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE books SET returned = 1 WHERE id = ?", (book_id,))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Buku berhasil dikembalikan.")
    show_books()

# Search book
def search_book():
    keyword = entry_search.get()
    conn = sqlite3.connect("perpustakaan.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM books 
        WHERE title LIKE ? OR author LIKE ?
    """, ('%' + keyword + '%', '%' + keyword + '%'))
    rows = cursor.fetchall()
    conn.close()
    update_table(rows)

# Show books in table
def show_books():
    conn = sqlite3.connect("perpustakaan.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books")
    rows = cursor.fetchall()
    conn.close()
    update_table(rows)

# Reset form
def reset_form():
    entry_title.delete(0, END)
    entry_author.delete(0, END)
    entry_year.delete(0, END)

# Update table
def update_table(rows):
    table.delete(*table.get_children())
    for row in rows:
        table.insert("", END, values=row)

# GUI setup
root = Tk()
root.title("Manajemen Perpustakaan Digital")  # Nama aplikasi
root.geometry("800x600")
root.configure(bg="#FFC0CB")  # Warna pink

# Title
Label(root, text="Manajemen Perpustakaan Digital", font=("Helvetica", 24, "bold"), bg="#FFC0CB", fg="white").pack(pady=5)

# Form
frame_form = Frame(root, bg="#FFC0CB")
frame_form.pack(pady=10)

Label(frame_form, text="Judul Buku", bg="#FFC0CB", fg="white", font=("Helvetica", 12)).grid(row=0, column=0, padx=10, pady=5)
entry_title = Entry(frame_form, width=25)
entry_title.grid(row=0, column=1, padx=10, pady=5)

Label(frame_form, text="Penulis", bg="#FFC0CB", fg="white", font=("Helvetica", 12)).grid(row=1, column=0, padx=10, pady=5)
entry_author = Entry(frame_form, width=25)
entry_author.grid(row=1, column=1, padx=10, pady=5)

Label(frame_form, text="Tahun Terbit", bg="#FFC0CB", fg="white", font=("Helvetica", 12)).grid(row=2, column=0, padx=10, pady=5)
entry_year = Entry(frame_form, width=25)
entry_year.grid(row=2, column=1, padx=10, pady=5)

Button(frame_form, text="Tambah Buku", command=add_book, bg="#ADD8E6", fg="black", width=15).grid(row=3, column=0, pady=10)
Button(frame_form, text="Perbarui Buku", command=update_book, bg="#ADD8E6", fg="black", width=15).grid(row=3, column=1, pady=10)
Button(frame_form, text="Hapus Buku", command=delete_book, bg="#ADD8E6", fg="black", width=15).grid(row=3, column=2, pady=10)

# Search
frame_search = Frame(root, bg="#FFC0CB")
frame_search.pack(pady=10)

Label(frame_search, text="Cari Buku", bg="#FFC0CB", fg="white", font=("Helvetica", 12)).grid(row=0, column=0, padx=10, pady=5)
entry_search = Entry(frame_search, width=30)
entry_search.grid(row=0, column=1, padx=10, pady=5)
Button(frame_search, text="Cari", command=search_book, bg="#ADD8E6", fg="black", width=15).grid(row=0, column=2, pady=10)

# Table
frame_table = Frame(root)
frame_table.pack(pady=10)

columns = ("ID", "Judul", "Penulis", "Tahun", "Dikembalikan")
table = ttk.Treeview(frame_table, columns=columns, show="headings", height=15)
table.pack()

for col in columns:
    table.heading(col, text=col)
    table.column(col, anchor="center")

# Additional buttons
frame_buttons = Frame(root, bg="#FFC0CB")
frame_buttons.pack(pady=10)

# Reset Button
Button(frame_buttons, text="Reset Form", command=reset_form, bg="#ADD8E6", fg="black", width=15).pack(side=LEFT, padx=10)

# Refresh Button
Button(frame_buttons, text="Segarkan Buku", command=show_books, bg="#ADD8E6", fg="black", width=15).pack(side=LEFT, padx=10)

# Return Book Button
Button(frame_buttons, text="Kembalikan Buku", command=return_book, bg="#ADD8E6", fg="black", width=15).pack(side=LEFT, padx=10)

# Run the app
initialize_db()
show_books()
root.mainloop()
