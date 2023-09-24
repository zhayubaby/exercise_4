import sqlite3

# Create a SQLite database or connect to an existing one
conn = sqlite3.connect("library.db")
cursor = conn.cursor()

# Create tables if they don't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Books (
        BookID TEXT PRIMARY KEY,
        Title TEXT,
        Author TEXT,
        ISBN TEXT,
        Status TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
        UserID TEXT PRIMARY KEY,
        Name TEXT,
        Email TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Reservations (
        ReservationID TEXT PRIMARY KEY,
        BookID TEXT,
        UserID TEXT,
        ReservationDate TEXT,
        FOREIGN KEY (BookID) REFERENCES Books (BookID),
        FOREIGN KEY (UserID) REFERENCES Users (UserID)
    )
''')

conn.commit()

# Function to add a new book to the database
def add_book():
    book_id = input("Enter BookID: ")
    title = input("Enter Title: ")
    author = input("Enter Author: ")
    isbn = input("Enter ISBN: ")
    status = input("Enter status(Available or not) of the book: ")
    
    cursor.execute("INSERT INTO Books VALUES (?, ?, ?, ?, ?)", (book_id, title, author, isbn, status))
    conn.commit()

# Function to find a book's details based on BookID
def find_book_by_id():
    book_id = input("Enter BookID: ")

    cursor.execute('''
        SELECT 
            Books.BookID, Books.Title, Books.Author, Books.ISBN, Books.Status,
            Users.UserID, Users.Name, Users.Email, 
            Reservations.ReservationID, Reservations.BookID, Reservations.UserID, Reservations.ReservationDate
        FROM Books
        LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
        LEFT JOIN Users ON Reservations.UserID = Users.UserID
        WHERE Books.BookID = ?
    ''', (book_id,))
    
    result = cursor.fetchone()
    
    if result:
        book_id, title, author, isbn, status, user_id, user_name, user_email, reservation_id, reservation_book_id, reservation_user_id, reservation_date = result
        print("BookID:", book_id)
        print("Title:", title)
        print("Author:", author)
        print("ISBN:", isbn)
        print("Status:", status)

        if user_name:
            print("Reserved by:", user_name, "(" + user_id + ")" + " - " + user_email)
        if reservation_date:
            print("Reservation Status:", reservation_id + " - " + reservation_date + " - " + reservation_book_id + " - " + reservation_user_id)
        else:
            print("Not reserved")
    else:
        print("Book not found.")


# Function to find a book's reservation status based on various criteria
def find_reservation_status():
    query = input("Enter BookID, UserID, ReservationID, or Title: ")
    
    cursor.execute("SELECT * FROM Reservations WHERE BookID = ?", (query,))
    book_result = cursor.fetchone()
    
    cursor.execute("SELECT * FROM Reservations WHERE UserID = ?", (query,))
    user_result = cursor.fetchone()
    
    cursor.execute("SELECT * FROM Reservations WHERE ReservationID = ?", (query,))
    reservation_result = cursor.fetchone()

    cursor.execute('''SELECT Reservations.* 
    FROM Reservations 
    INNER JOIN Books ON Reservations.BookID = Books.BookID 
    WHERE Books.Title = ?
    ''', (query,))
    title_result = cursor.fetchone()
    
    if book_result:
        print("Reservation Details(by bookID):", book_result)
    elif user_result:
        print("Reservation Details(by userID):", user_result)
    elif reservation_result:
        print("Reservation Details(by resID):", reservation_result)
    elif title_result:
        print("Reservation Details(by title):", title_result)
    else:
        print("No matching records found.")

# Function to find all books in the database
def find_all_books():
    cursor.execute("SELECT Books.*, Users.*, Reservations.* FROM Books LEFT JOIN Reservations ON Books.BookID = Reservations.BookID LEFT JOIN Users ON Reservations.UserID = Users.UserID")
    results = cursor.fetchall()
    
    if results:
        for result in results:
            book_id, title, author, isbn, status, user_id, user_name, user_email, reservation_id, reservation_book_id, reservation_user_id, reservation_date = result
            print("BookID:", book_id)
            print("Title:", title)
            print("Author:", author)
            print("ISBN:", isbn)
            print("Status:", status)
            
            if user_name:
                print("Reserved by:", user_name, "(" + user_id + ")" + " - " + user_email)
            if reservation_date:
                print("Reservation Status:", reservation_id + " - " + reservation_date + " - " + reservation_book_id + " - " + reservation_user_id)
            else:
                print("Not reserved")
            print()
    else:
        print("No books found in the database.")

# Function to modify/update book details based on its BookID
def update_book():
    book_id = input("Enter BookID to update: ")
    
    cursor.execute("SELECT * FROM Books WHERE BookID = ?", (book_id,))
    book_result = cursor.fetchone()
    
    if book_result:
        new_status = input("Enter new status: ")
        cursor.execute("UPDATE Books SET Status = ? WHERE BookID = ?", (new_status, book_id))
        conn.commit()
        print("Book details updated.")
    else:
        print("Book not found.")

# Function to delete a book based on BookID
def delete_book():
    book_id = input("Enter BookID to delete: ")

    # Check if the book is reserved
    cursor.execute("SELECT * FROM Reservations WHERE BookID = ?", (book_id,))
    reservation_result = cursor.fetchone()

    if reservation_result:
        # If the book is reserved, delete the reservation first
        cursor.execute("DELETE FROM Reservations WHERE BookID = ?", (book_id,))
        conn.commit()

    # Delete the book from the Books table
    cursor.execute("DELETE FROM Books WHERE BookID = ?", (book_id,))
    conn.commit()

    print("Book deleted.")


# Main menu
while True:
    print("\nLibrary Management System")
    print("1. Add a new book")
    print("2. Find a book by BookID")
    print("3. Find reservation status")
    print("4. Find all books")
    print("5. Update book details")
    print("6. Delete a book")
    print("7. Exit")
    choice = input("Enter your choice: ")

    if choice == '1':
        add_book()
    elif choice == '2':
        find_book_by_id()
    elif choice == '3':
        find_reservation_status()
    elif choice == '4':
        find_all_books()
    elif choice == '5':
        update_book()
    elif choice == '6':
        delete_book()
    elif choice == '7':
        print("Goodbye!")
        conn.close()
        break
    else:
        print("Invalid choice. Please try again.")
