
import sqlite3
import datetime

def init_db():
    conn = sqlite3.connect("credentials.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            first_name TEXT NOT NULL,
            last_name  TEXT NOT NULL,
            email  TEXT NOT NULL UNIQUE,
            zip_code INTEGER,
            password TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            book_name TEXT PRIMARY KEY,
            status TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS active_borrows (
            book_name TEXT NOT NULL,
            borrower_email TEXT NOT NULL,
            borrow_date TEXT,
            return_date TEXT,
            fine INTEGER
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS borrow_history (
            book_name TEXT NOT NULL,
            borrower_email TEXT NOT NULL,
            borrow_date TEXT,
            return_date TEXT
        )
    """)
    
    conn.commit()
    conn.close()

#  Students

def insert_student(fname, lname, email, zip_code, password):
    try:
        conn = sqlite3.connect("credentials.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO students VALUES (?, ?, ?, ?, ?)",
                       (fname, lname, email, zip_code, password))
        conn.commit()
        conn.close()
        return "Success"
    except sqlite3.IntegrityError:
        return "Error: Email already exists."
    except Exception as e:
        return f"Error: {e}"

def remove_student(email):
    conn = sqlite3.connect("credentials.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE email = ?", (email,))
    rows_affected = cursor.rowcount
    conn.commit()
    conn.close()
    if rows_affected > 0:
        return "Success"
    else:
        return "Error: User not found."

def check_login(email, password):
    conn = sqlite3.connect("credentials.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE email = ? AND password = ?", (email, password))
    user = cursor.fetchone()
    conn.close()
    return True if user else False

def get_student_details(email):
    conn = sqlite3.connect("credentials.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()
    return user

def get_all_students():
    conn = sqlite3.connect("credentials.db")
    cursor = conn.cursor()
    cursor.execute("SELECT first_name, last_name, email FROM students")
    data = cursor.fetchall()
    conn.close()
    return data

# Books database

def add_book(book_name):
    try:
        conn = sqlite3.connect("credentials.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO books VALUES (?, ?)", (book_name, "Available"))
        conn.commit()
        conn.close()
        return "Success"
    except sqlite3.IntegrityError:
        return "Error: Book already exists."

def remove_book(book_name):
    conn = sqlite3.connect("credentials.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM books WHERE book_name = ?", (book_name,))
    conn.commit()
    conn.close()
    return "Success"

def get_all_books():
    conn = sqlite3.connect("credentials.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books")
    data = cursor.fetchall()
    conn.close()
    return data

# Borrow and return

def borrow_book(book_name, user_email, due_date_str=None):
    conn = sqlite3.connect("credentials.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT status FROM books WHERE book_name = ?", (book_name,))
    result = cursor.fetchone()
    
    if not result:
        conn.close()
        return "Error: Book not found."
    if result[0] != "Available":
        conn.close()
        return "Error: Book is currently unavailable."

    cursor.execute("UPDATE books SET status = 'Borrowed' WHERE book_name = ?", (book_name,))

    today = datetime.date.today()
    
    # Logic for Due Date
    if due_date_str:
        due_date = due_date_str
    else:
        due_date = str(today + datetime.timedelta(days=7))
    
    cursor.execute("INSERT INTO active_borrows VALUES (?, ?, ?, ?, ?)", 
                   (book_name, user_email, str(today), due_date, 0))

    cursor.execute("INSERT INTO borrow_history VALUES (?, ?, ?, ?)", 
                   (book_name, user_email, str(today), due_date))
    
    conn.commit()
    conn.close()
    return "Success"

def return_book(book_name, user_email):
    conn = sqlite3.connect("credentials.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM active_borrows WHERE book_name = ? AND borrower_email = ?", (book_name, user_email))
    result = cursor.fetchone()
    
    if not result:
        conn.close()
        return "Error: No active borrow record found for this book and user."

    cursor.execute("UPDATE books SET status = 'Available' WHERE book_name = ?", (book_name,))
    cursor.execute("DELETE FROM active_borrows WHERE book_name = ? AND borrower_email = ?", (book_name, user_email))
    
    conn.commit()
    conn.close()
    return "Success"

# History and fines

def get_user_history(email):
    conn = sqlite3.connect("credentials.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM borrow_history WHERE borrower_email = ?", (email,))
    data = cursor.fetchall()
    conn.close()
    return data

def get_all_active_borrows():
    conn = sqlite3.connect("credentials.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM active_borrows")
    data = cursor.fetchall()
    conn.close()
    return data

def get_user_active_fines(email):
    conn = sqlite3.connect("credentials.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM active_borrows WHERE borrower_email = ? AND fine > 0", (email,))
    data = cursor.fetchall()
    conn.close()
    return data

def get_all_fines():
    conn = sqlite3.connect("credentials.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM active_borrows WHERE fine > 0")
    data = cursor.fetchall()
    conn.close()
    return data

def refresh_fines():
    conn = sqlite3.connect("credentials.db")
    cursor = conn.cursor()
    today = datetime.date.today()
    cursor.execute("SELECT rowid, return_date FROM active_borrows")
    borrows = cursor.fetchall()
    
    for row in borrows:
        row_id = row[0]
        due_date_str = row[1]
        try:
            due_date = datetime.datetime.strptime(due_date_str, "%Y-%m-%d").date()
            if today > due_date:
                overdue_days = (today - due_date).days
                fine_amount = overdue_days * 5
                cursor.execute("UPDATE active_borrows SET fine = ? WHERE rowid = ?", (fine_amount, row_id))
        except:
            pass
            
    conn.commit()
    conn.close()

init_db()

