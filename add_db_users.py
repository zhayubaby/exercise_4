import sqlite3

conn = sqlite3.connect("library.db")
cursor = conn.cursor()

# Function to add users to the database
def add_user():
    user_id = input("Enter UserID: ")
    name = input("Enter Name: ")
    email = input("Enter Email: ")
    
    cursor.execute("INSERT INTO Users VALUES (?, ?, ?)", (user_id, name, email))
    conn.commit()

add_user()
